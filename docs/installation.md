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
    ```

=== "Windows"

    PowerShell 7+, on x86-64 or ARM64.

    ```powershell
    # Download the script; review it before running
    Invoke-WebRequest https://docs.tqdm.sh/install.ps1 -OutFile install.ps1

    # Verify SHA-256 and install for your user
    pwsh -File ./install.ps1
    ```

    If scripts are restricted, use [manual installation](downloads.md#verify-on-windows) and follow your organisation's policy.

=== "Windows / WSL"

    Already have WSL? Open your Linux terminal and use the **macOS / Linux** commands.

    ```powershell
    # First-time setup only: run in an administrator PowerShell
    wsl --install
    ```

    Restart if prompted, open Ubuntu, and finish its user setup. Install `tqctl` inside Ubuntu using the Linux instructions. [WSL setup help](https://learn.microsoft.com/en-us/windows/wsl/install).

## Set up your shell

Run once. It puts tqctl on your PATH and turns on tab completion in every new terminal.

=== "zsh"

    ```sh
    # Add PATH and completion to ~/.zshrc, once
    grep -qs 'tqctl completion zsh' ~/.zshrc || cat >> ~/.zshrc <<'EOF'
    # tqctl
    export PATH="$HOME/.local/bin:$PATH"
    autoload -U compinit && compinit
    source <(tqctl completion zsh)
    EOF

    # Load it in this terminal and check the version
    source ~/.zshrc
    tqctl --version
    ```

=== "bash"

    ```sh
    # Add PATH and completion to ~/.bashrc, once
    grep -qs 'tqctl completion bash' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
    # tqctl
    export PATH="$HOME/.local/bin:$PATH"
    eval "$(tqctl completion bash)"
    EOF

    # Load it in this terminal and check the version
    source ~/.bashrc
    tqctl --version
    ```

    Completion in bash needs the `bash-completion` package.

=== "PowerShell"

    ```powershell
    # Add tqctl to your user Path and completion to your profile, once
    $bin = "$HOME\AppData\Local\tqctl\bin"
    [Environment]::SetEnvironmentVariable('Path', "$bin;" + [Environment]::GetEnvironmentVariable('Path', 'User'), 'User')
    Add-Content $PROFILE "`ntqctl completion powershell | Out-String | Invoke-Expression"

    # Open a new terminal, then check the version
    tqctl --version
    ```

## Update

```sh
tqctl update          # Install the latest stable release
tqctl update --check  # Only say whether a newer one is out
```

tqctl also checks on every run and tells you at the end of a command when a newer release is out. Set `TQDM_NO_UPDATE=1` to turn that off.

To pin a version, run the installer again with `--version` (`-Version` on Windows). A failed download or checksum check preserves your current installation.

=== "macOS / Linux / WSL"

    ```sh
    sh install.sh --version <version> # A specific release

    # Optional: choose a user-owned directory
    sh install.sh --install-dir "$HOME/.local/bin"
    ```

=== "Windows"

    ```powershell
    pwsh -File ./install.ps1 -Version <version> # A specific release

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
