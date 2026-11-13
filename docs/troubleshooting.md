# Troubleshooting

## `tqctl: command not found`

Check that the installation directory is on your PATH. On macOS, Linux, and WSL:

```sh
export PATH="$HOME/.local/bin:$PATH"
tqctl --version
```

On native Windows, use the PowerShell PATH command in [installation](installation.md#__tabbed_1_2). Open a new terminal after changing your user Path.

## The checksum does not match

Do not run the downloaded file. Delete it and download the binary and checksum manifest again from the same release. If the problem persists, stop and report the release version and filename. The installer does not replace your current binary when verification fails.

## The installer cannot download a release

Check your network connection and whether your organisation permits access to `docs.tqdm.sh`. Do not disable TLS certificate verification. If a proxy or private certificate authority is required, use your organisation's approved configuration.

## The operating system blocks the binary

Follow your organisation's software approval process. A SHA-256 match checks the download against the manifest; it does not mean the binary has Apple notarization or a Windows code signature. Do not disable system protections to install it.

## Sign-in uses the wrong organisation

Run `tqctl auth whoami`. Check whether `TQDM_TOKEN` or `TQDM_API` is set. Select the intended organisation in the browser, then run `tqctl auth login` again.

## Browser approval expired

Start `tqctl auth login` again. Approvals expire after ten minutes. Match the new code shown in your terminal before approving.

## SSH or port forwarding fails

Check that your session is still running and you selected the right machine. The service must be listening on the requested port. See [connection instructions](connections.md). For an exam, return to the browser.

## Report a problem

Include your operating system, CPU architecture, `tqctl --version`, the command you ran, and the error text. Remove tokens, personal information, and lab content you are not permitted to share. Use the support channel provided by your organisation.
