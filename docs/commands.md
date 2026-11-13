# Command reference

Use the help shipped with your installed version for the exact arguments and options:

```sh
tqctl --help
tqctl <command> --help
```

| Command | Use it to |
| --- | --- |
| `auth login` | Approve a CLI sign-in through your browser |
| `auth whoami` | Check the credential, account, and endpoint in use |
| `auth logout` | Revoke this CLI's sign-in |
| `auth token` | Create an API key, if your role permits it |
| `lab ls`, `lab describe` | Find and inspect labs |
| `lab new`, `lab validate`, `lab push` | Create, check, and upload lab definitions |
| `lab publish`, `lab unpublish` | Control lab availability, if your role permits it |
| `session create -f <manifest>`, `session ls`, `session describe` | Start a session from a local manifest, or inspect sessions |
| `session destroy` | End a session |
| `ssh` | Connect with your system SSH client |
| `ssh-proxy` | Provide a local port for SSH tools and editors |
| `port-forward` | Forward a local port to a lab machine |
| `exec` | Run a command on a lab machine |
| `task ls`, `task check` | Read tasks and run checks |
| `workspace ls`, `workspace delete`, `workspace release` | Manage retained workspaces |

## JSON output

Use `-o json` when processing output in a script:

```sh
tqctl lab ls -o json
tqctl session ls -o json
```

## Version

```sh
tqctl --version
```

Include your CLI version when reporting a problem. Do not include your token or configuration file.
