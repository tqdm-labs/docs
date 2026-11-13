# Connect to a machine

`tqctl` connects to machines in sessions you can access. You do not need to expose a machine's SSH port to the internet.

## SSH

Install an SSH client on your computer, then run:

```sh
tqctl ssh <session-id>
```

For a lab with more than one machine:

```sh
tqctl ssh <session-id> -m <machine-name>
```

The CLI places a public key on the selected machine and starts your system SSH client. On first use it creates a local Ed25519 key if you have not supplied one. Keep private keys private.

To use an existing public key:

```sh
tqctl ssh <session-id> --key "$HOME/.ssh/id_ed25519.pub"
```

## Connect from an editor

Start a local SSH proxy and leave that terminal open:

```sh
tqctl ssh-proxy <session-id> --address 127.0.0.1:2222
```

Follow the connection details printed by the CLI. For an editor such as VS Code Remote SSH, use the printed host, port, user, and identity file. Stop the proxy with Ctrl+C when finished.

## Forward a port

For an application listening on port 80 in the lab machine:

```sh
tqctl port-forward <session-id> -L 8080:80
```

Open `http://127.0.0.1:8080` on your computer. The forward is bound to loopback by default. Leave the terminal open while using it, then press Ctrl+C to stop.

## If a connection is refused

The machine must be running and listening on the requested port. Check the session and machine name with `tqctl session describe <session-id>`. SSH access depends on the lab's image and settings. Exams use the browser instead of CLI machine access.
