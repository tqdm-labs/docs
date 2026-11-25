$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/../docs/install.ps1"
function Get-TqctlTarget { 'windows_amd64' }
$root = Join-Path ([IO.Path]::GetTempPath()) ([Guid]::NewGuid().ToString())
$null = New-Item -ItemType Directory $root
$payload = [Text.Encoding]::UTF8.GetBytes('not executed by installer')
$hash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($payload)).ToLowerInvariant()
$script:manifest = "$hash  tqctl_v0.4.8_windows_amd64.exe"
$script:latest = "v0.4.8`n"
$script:latestRequests = 0
function Invoke-WebRequest($Uri) {
    if ($Uri -cne 'https://docs.tqdm.sh/releases/latest.txt') { throw "Unexpected URL: $Uri" }
    $script:latestRequests++
    @{ Content = $script:latest }
}
function Get-TqctlFile($Uri, $OutFile) {
    if ($Uri -cnotmatch '\Ahttps://docs\.tqdm\.sh/releases/v0\.4\.8/(SHA256SUMS|tqctl_v0\.4\.8_windows_amd64\.exe)\z') {
        throw "Unexpected URL: $Uri"
    }
    if ($Uri.EndsWith('/SHA256SUMS')) { [IO.File]::WriteAllText($OutFile, $script:manifest) }
    else { [IO.File]::WriteAllBytes($OutFile, $payload) }
}
function Assert($Condition, $Message) { if (-not $Condition) { throw $Message } }
try {
    $dest = Join-Path $root 'directory with spaces'
    $out = Install-Tqctl -Version v0.4.8 -InstallDir $dest
    Assert ($out[-1] -ceq 'Set up your shell (PATH and tab completion): https://docs.tqdm.sh/installation/#set-up-your-shell') 'final message missing shell setup link'
    Assert ($script:latestRequests -eq 0) 'pinned version requested latest'
    $binary = Join-Path $dest 'tqctl.exe'
    Assert ((Get-FileHash $binary).Hash.ToLowerInvariant() -eq $hash) 'successful installation failed'
    Install-Tqctl -Version '' -InstallDir $dest
    Assert ($script:latestRequests -eq 1) 'latest version was not requested'
    foreach ($bad in @('', '<html>unavailable</html>', '../bad', "v0.4.8`nv0.4.9", "v0.4.8`n../bad")) {
        $script:latest = $bad
        $failed = $false
        try { Install-Tqctl -Version '' -InstallDir $dest } catch { $failed = $true }
        Assert $failed 'invalid latest version accepted'
        Assert ((Get-FileHash $binary).Hash.ToLowerInvariant() -eq $hash) 'invalid latest changed binary'
    }
    foreach ($bad in @('invalid  tqctl_v0.4.8_windows_amd64.exe', "$script:manifest`n$script:manifest", "$hash  another.exe", "$('0' * 64)  tqctl_v0.4.8_windows_amd64.exe")) {
        $script:manifest = $bad
        $failed = $false
        try { Install-Tqctl -Version v0.4.8 -InstallDir $dest } catch { $failed = $true }
        Assert $failed 'bad checksum manifest accepted'
        Assert ((Get-FileHash $binary).Hash.ToLowerInvariant() -eq $hash) 'existing binary changed after failure'
    }
    $failed = $false
    try { Install-Tqctl -Version '../bad' -InstallDir $dest } catch { $failed = $true }
    Assert $failed 'invalid version accepted'
    function Get-TqctlFile { throw 'download failed' }
    $failed = $false
    try { Install-Tqctl -Version v0.4.8 -InstallDir $dest } catch { $failed = $true }
    Assert $failed 'download failure ignored'
    Assert ((Get-FileHash $binary).Hash.ToLowerInvariant() -eq $hash) 'download failure changed binary'
    Write-Output 'PowerShell installer checks passed.'
} finally { Remove-Item -LiteralPath $root -Recurse -Force }
