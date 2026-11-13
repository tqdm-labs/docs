#requires -Version 7.0
[CmdletBinding()]
param(
    [string]$Version = '',
    [string]$InstallDir = (Join-Path $HOME 'AppData/Local/tqctl/bin')
)
$ErrorActionPreference = 'Stop'

function Get-TqctlTarget {
    if (-not $IsWindows) { throw 'Use install.sh on macOS or Linux, including WSL.' }
    switch ([Runtime.InteropServices.RuntimeInformation]::OSArchitecture) {
        'X64' { 'windows_amd64' }
        'Arm64' { 'windows_arm64' }
        default { throw 'Supported Windows architectures are x86-64 and ARM64.' }
    }
}

function Get-TqctlFile([string]$Uri, [string]$OutFile) {
    Invoke-WebRequest -Uri $Uri -OutFile $OutFile -MaximumRedirection 5 -TimeoutSec 300
}

function Install-Tqctl([string]$Version, [string]$InstallDir) {
    $target = Get-TqctlTarget
    if (-not [IO.Path]::IsPathRooted($InstallDir)) { throw 'InstallDir must be an absolute path.' }
    $base = 'https://docs.tqdm.sh'
    if (-not $Version) {
        $response = Invoke-WebRequest -Uri "$base/releases/latest.txt" -MaximumRedirection 5 -TimeoutSec 120
        $Version = ([string]$response.Content).Trim()
    }
    if ($Version -cnotmatch '\Av[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z]+([.-][0-9A-Za-z]+)*)?\z') {
        throw 'Version must look like v0.4.8.'
    }
    $asset = "tqctl_${Version}_${target}.exe"
    $null = New-Item -ItemType Directory -Path $InstallDir -Force
    $destination = Join-Path $InstallDir 'tqctl.exe'
    if (Test-Path -LiteralPath $destination) {
        $item = Get-Item -LiteralPath $destination -Force
        if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw 'Destination must be a regular file, not a directory or link.'
        }
    }
    $work = Join-Path $InstallDir ('.tqctl-install-' + [Guid]::NewGuid().ToString())
    $null = New-Item -ItemType Directory -Path $work
    try {
        $binary = Join-Path $work $asset
        $manifest = Join-Path $work 'SHA256SUMS'
        Get-TqctlFile "$base/releases/$Version/$asset" $binary
        Get-TqctlFile "$base/releases/$Version/SHA256SUMS" $manifest
        $entries = @(Get-Content -LiteralPath $manifest | Where-Object {
            $parts = $_.Trim() -split '\s+'
            $parts.Count -ge 2 -and $parts[1] -ceq $asset
        })
        $pattern = '^([0-9a-fA-F]{64})\s+' + [regex]::Escape($asset) + '$'
        if ($entries.Count -ne 1 -or $entries[0] -cnotmatch $pattern) {
            throw 'Checksum manifest must contain exactly one valid entry for this binary.'
        }
        $expected = $Matches[1]
        if ((Get-FileHash -LiteralPath $binary -Algorithm SHA256).Hash -ine $expected) {
            throw 'SHA-256 mismatch. Your existing installation has not been changed.'
        }
        if (Test-Path -LiteralPath $destination) {
            $item = Get-Item -LiteralPath $destination -Force
            if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                throw 'Destination changed to a directory or link. Installation stopped.'
            }
        }
        [IO.File]::Move($binary, $destination, $true)
        Write-Output "Installed $destination"
        Write-Output "Ensure this directory is on your user Path: $InstallDir"
        Write-Output 'Then run: tqctl --version'
    } finally {
        Remove-Item -LiteralPath $work -Recurse -Force
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    Install-Tqctl -Version $Version -InstallDir $InstallDir
}
