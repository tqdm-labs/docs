# Install tqctl

Choose your system. Both installers verify SHA-256 before installing, without administrator access.

[Prefer a direct download?](downloads.md) Get the binary and verify it yourself.

## Choose your system

<span id="macos-and-linux"></span><span id="windows"></span>

=== "macOS / Linux"

    Apple Silicon, Intel, and Linux ARM64 or x86-64. Requires `curl` and `shasum` or `sha256sum`.

    ```sh
    # Download the script; review it before running
    curl --proto '=https' --tlsv1.2 -fsSL \
      https://docs.tqdm.sh/install.sh -o install.sh

    # Detect your system, verify SHA-256, install to ~/.local/bin
    sh install.sh

    # Add to PATH for this terminal and check the version
    export PATH="$HOME/.local/bin:$PATH"
    tqctl --version
    ```

    To keep PATH across terminals, add the export line to `~/.zshrc` or `~/.bashrc`.

=== "Windows"

    PowerShell 7+, on x86-64 or ARM64.

    ```powershell
    # Download the script; review it before running
    Invoke-WebRequest https://docs.tqdm.sh/install.ps1 -OutFile install.ps1

    # Verify SHA-256 and install for your user
    pwsh -File ./install.ps1

    # Add to PATH for this terminal and check the version
    $env:Path = "$HOME\AppData\Local\tqctl\bin;$env:Path"
    tqctl --version
    ```

    For future terminals, add `%USERPROFILE%\AppData\Local\tqctl\bin` to your **user Path** in Windows Environment Variables. If scripts are restricted, use [manual installation](downloads.md#verify-on-windows) and follow your organisation's policy.

=== "Windows / WSL"

    Already have WSL? Open your Linux terminal and use the **macOS / Linux** commands.

    ```powershell
    # First-time setup only: run in an administrator PowerShell
    wsl --install
    ```

    Restart if prompted, open Ubuntu, and finish its user setup. Install `tqctl` inside Ubuntu using the Linux instructions. [WSL setup help](https://learn.microsoft.com/en-us/windows/wsl/install).

## Update or pin a version

Run the installer again to get the latest stable release. A failed download or checksum check preserves your current installation.

=== "macOS / Linux / WSL"

    ```sh
    sh install.sh                  # Latest stable version
    sh install.sh --version v0.4.8 # A specific release

    # Optional: choose a user-owned directory
    sh install.sh --install-dir "$HOME/.local/bin"
    ```

=== "Windows"

    ```powershell
    pwsh -File ./install.ps1                 # Latest stable version
    pwsh -File ./install.ps1 -Version v0.4.8 # A specific release

    # Optional: choose a user-owned directory
    pwsh -File ./install.ps1 -InstallDir "$HOME\tools\bin"
    ```

## Next: sign in

```sh
tqctl auth login  # Approve the matching code in your browser
tqctl auth whoami # Confirm your account and organisation
```

[Continue to the quickstart](quickstart.md).

## Uninstall

Run `tqctl auth logout` to revoke this CLI's sign-in, then remove the binary from its installation directory. Removing the binary alone does not revoke the credential.
