# Sign in

`tqctl` signs you in through your browser. Each installation has its own CLI session, which you can revoke without signing out your other devices.

```sh
tqctl auth login
```

Check the approval code, account, and organisation before you approve. The approval expires after ten minutes.

## Sign in without opening a browser

```sh
tqctl auth login --no-browser
```

Open the printed URL in a browser where you can sign in. Approve only a request you started, and match its code to your terminal.

## Check your account

```sh
tqctl auth whoami
```

Your CLI remains bound to the organisation selected when you approved it. Switching organisation in the browser does not switch the CLI. Run `tqctl auth login` again to choose a different organisation.

## Sign out

```sh
tqctl auth logout
```

This revokes the CLI session and removes its stored sign-in. It does not end your running lab sessions.

## Credentials and configuration

The default API endpoint is `https://tqdm.sh`. Configuration is stored in `~/.config/tqctl/config.yaml`, or under `$XDG_CONFIG_HOME/tqctl` when that variable is set. Treat the file as a credential: do not share it or commit it.

`TQDM_API` overrides the configured endpoint. `TQDM_TOKEN` overrides the stored credential. If the CLI appears to use an unexpected account or endpoint, run `tqctl auth whoami` and check those environment variables.

## Use tqctl in automation

Use an API key supplied by your organisation rather than copying your personal CLI credential into a pipeline. Store it in your CI secret manager and expose it as `TQDM_TOKEN`. A key acts as its issuing account and uses that account's lab hours. Key permissions depend on that account and organisation.

Avoid putting tokens directly in commands, logs, screenshots, or shared shell history.
