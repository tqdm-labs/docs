# Get started with tqctl

Install [tqctl](installation.md), then sign in and find a lab available to your organisation.

## Sign in

```console
$ tqctl auth login
```

Your browser opens an approval page. Check that the code in your terminal matches the page, confirm the account and organisation, then approve the sign-in.

```console
$ tqctl auth whoami
```

This shows the account, organisation, and API endpoint the CLI is using.

## Find a lab

```console
$ tqctl lab ls
```

To start a published lab, open it in the tqdm.sh web interface and follow its instructions. Then list your running sessions:

```console
$ tqctl session ls
$ tqctl session describe <session-id>
```

Replace `<session-id>` with an identifier from the output.

If you author labs and have a local manifest, you can start a session with `tqctl session create -f path/to/lab.yaml`. This command takes a manifest file, not a catalog lab identifier.

## Connect

Use the session identifier returned by the previous command:

```console
$ tqctl ssh <session-id>
```

SSH requires an SSH client on your computer and a lab machine that supports SSH. You can also open the session in the tqdm.sh web interface. Exams are taken in the browser.

## End a session

When you no longer need the session:

```console
$ tqctl session destroy <session-id>
```

Ending a session stops its machines. Save any files you need before ending it.

Continue with [lab sessions](labs.md) or [SSH and port forwarding](connections.md).
