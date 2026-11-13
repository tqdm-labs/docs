# Downloads

Download a standalone `tqctl` binary for your operating system and CPU. Each release includes a `SHA256SUMS` file. No installer is required.

## Direct downloads

| Operating system | CPU | Binary |
| --- | --- | --- |
| macOS | Apple Silicon (ARM64) | [tqctl_v0.4.8_darwin_arm64](https://docs.tqdm.sh/releases/v0.4.8/tqctl_v0.4.8_darwin_arm64) |
| macOS | Intel (x86-64) | [tqctl_v0.4.8_darwin_amd64](https://docs.tqdm.sh/releases/v0.4.8/tqctl_v0.4.8_darwin_amd64) |
| Linux / WSL | x86-64 | [tqctl_v0.4.8_linux_amd64](https://docs.tqdm.sh/releases/v0.4.8/tqctl_v0.4.8_linux_amd64) |
| Linux / WSL | ARM64 | [tqctl_v0.4.8_linux_arm64](https://docs.tqdm.sh/releases/v0.4.8/tqctl_v0.4.8_linux_arm64) |
| Windows | x86-64 | [tqctl_v0.4.8_windows_amd64.exe](https://docs.tqdm.sh/releases/v0.4.8/tqctl_v0.4.8_windows_amd64.exe) |
| Windows | ARM64 | [tqctl_v0.4.8_windows_arm64.exe](https://docs.tqdm.sh/releases/v0.4.8/tqctl_v0.4.8_windows_arm64.exe) |

[Download SHA256SUMS](https://docs.tqdm.sh/releases/v0.4.8/SHA256SUMS)

[Release details](https://docs.tqdm.sh/releases/v0.4.8/release.json)

On macOS or Linux, run `uname -m`: `arm64` or `aarch64` means ARM64; `x86_64` means x86-64. For native Windows, check **Settings → System → About → System type**. In WSL, choose the Linux binary matching `uname -m` inside WSL.

## Verify on macOS or Linux

Download the binary and `SHA256SUMS` from the same release into an empty directory. For example, on an Apple Silicon Mac:

```sh
curl --proto '=https' --tlsv1.2 -fL -O https://docs.tqdm.sh/releases/v0.4.8/tqctl_v0.4.8_darwin_arm64
curl --proto '=https' --tlsv1.2 -fL -O https://docs.tqdm.sh/releases/v0.4.8/SHA256SUMS
shasum -a 256 tqctl_v0.4.8_darwin_arm64
```

On Linux, use `sha256sum` instead of `shasum -a 256`. Compare the entire hash with the line for the **exact filename** in `SHA256SUMS`. If they differ, do not run the binary.

After the hash matches, rename and install the binary:

```sh
mkdir -p "$HOME/.local/bin"
install -m 755 tqctl_v0.4.8_darwin_arm64 "$HOME/.local/bin/tqctl"
export PATH="$HOME/.local/bin:$PATH"
tqctl --version
```

For another platform, replace the filename in each command with the matching filename from the table.

## Verify on Windows

Download the Windows `.exe` and `SHA256SUMS` from the same release. In PowerShell, from your download directory:

```powershell
Get-FileHash ./tqctl_v0.4.8_windows_amd64.exe -Algorithm SHA256
Get-Content ./SHA256SUMS
```

Compare the entire hash, ignoring letter case, with the entry for the exact filename. If it matches, move the executable into a directory you control, rename it `tqctl.exe`, and add that directory to your user Path. Use the ARM64 filename on Windows ARM64.

## What the checksum tells you

A matching SHA-256 hash confirms that the file matches the release manifest. The binary and manifest are distributed together; this check does not independently prove who published them. These initial binaries are not code-signed or notarized. Follow your organisation's software approval process where required.

To review the installer before using it, download [install.sh](install.sh) or [install.ps1](install.ps1). For version selection and updates, see [installation](installation.md).
