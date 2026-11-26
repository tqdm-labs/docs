# Connect to a machine

`tqctl` connects to machines in sessions you can access. You do not need to expose a machine's SSH port to the internet.

## SSH

Install an SSH client on your computer, then run:

```console
$ tqctl ssh <session-id>
```

For a lab with more than one machine:

```console
$ tqctl ssh <session-id> -m <machine-name>
```

The CLI places a public key on the selected machine and starts your system SSH client. On first use it creates a local Ed25519 key if you have not supplied one. Keep private keys private.

To use an existing public key:

```console
$ tqctl ssh <session-id> --key "$HOME/.ssh/id_ed25519.pub"
```

## Connect from an editor

Start a local SSH proxy and leave that terminal open:

```console
$ tqctl ssh-proxy <session-id> --address 127.0.0.1:2222
```

Follow the connection details printed by the CLI. For an editor such as VS Code Remote SSH, use the printed host, port, user, and identity file. Stop the proxy with Ctrl+C when finished.

## Forward a port

For an application listening on port 80 in the lab machine:

```console
$ tqctl port-forward <session-id> -L 8080:80
```

Open `http://127.0.0.1:8080` on your computer. The forward is bound to loopback by default. Leave the terminal open while using it, then press Ctrl+C to stop.

## Open a port in your browser

You can also open an app from the lab page itself, without `tqctl`. Select the Ports button at the right end of the terminal's tab strip. The Ports panel opens under the terminal and lists every port you can open, including the ones the lab provides, which are marked `lab`.

To add one, choose the machine, enter the port your app listens on, and optionally a name. The name becomes the start of the link, for example `https://grafana-3fa1c2d9.preview.tqdm.sh`. Select Forward, then open the link from its row.

- **Private** (the default): the link opens only for you, your teacher, and your organisation's owners. Anyone else sees a page asking them to sign in.
- **Public**: anyone with the link can open it.

Select a forward's Private or Public label to switch it, or its bin icon to stop it. A session holds up to ten forwards, and they all end with the session.

The app must listen on all addresses (`0.0.0.0`), not only on `127.0.0.1`. For example, `python3 -m http.server 8000 --bind 0.0.0.0`. Exams have no Ports panel.

## If a connection is refused

The machine must be running and listening on the requested port. Check the session and machine name with `tqctl session describe <session-id>`. SSH access depends on the lab's image and settings. Exams use the browser instead of CLI machine access.
