# Command reference

This reference follows the latest `tqctl` release. Use the help shipped with your installed version for the exact arguments and options:

```console
$ tqctl --help
$ tqctl <command> --help
```

| Command | Use it to |
| --- | --- |
| `auth login` | Approve a CLI sign-in through your browser |
| `auth whoami` | Check the credential, account, and endpoint in use |
| `auth logout` | Revoke this CLI's sign-in |
| `auth token` | Create an API key, if your role permits it |
| `lab ls`, `lab describe` | Find and inspect labs. A lab can be named with or without its organisation's prefix |
| `lab new`, `lab script new`, `lab validate`, `lab push` | Create, check, and upload lab definitions <span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations</span> |
| `lab publish`, `lab unpublish` | Control lab availability, if your role permits it <span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations</span> |
| `image build`, `image push` | Build a machine image on your computer and push it to your organisation <span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations</span> |
| `image ls`, `image pushes`, `image rm` | List your organisation's images, quota, and pushes, or delete an image <span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations</span> |
| `session create -f <manifest>`, `session ls`, `session describe` | Start a session from a local manifest, or inspect sessions |
| `start <lab>` | Start a lab from the catalogue and print its web link and SSH command. Options: `--timeout`, `-q`. Exams are started in the browser |
| `session destroy` | End a session |
| `ssh` | Connect with your system SSH client |
| `ssh-key` | Place your SSH key in a lab machine |
| `ssh-proxy` | Provide a local port for SSH tools and editors |
| `port-forward` | Forward a local port to a lab machine |
| `exec` | Run a command on a lab machine |
| `task ls`, `task check` | Read tasks and run checks |
| `workspace ls`, `workspace delete`, `workspace release` | Manage retained workspaces |
| `update`, `update --check` | Install the latest release, or only say whether a newer one is out |

## JSON output

Use `-o json` when processing output in a script:

```console
$ tqctl lab ls -o json
$ tqctl session ls -o json
```

## Version

```console
$ tqctl --version
```

Include your CLI version when reporting a problem. Do not include your token or configuration file.

## Update check

tqctl checks for a newer release while a command runs and tells you at the end of the command. It stays silent in a pipe, offline, and for tab completion. Set `TQDM_NO_UPDATE=1` to turn the check off. It does not affect `tqctl update`.
