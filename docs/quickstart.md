# Get started with tqctl

Install [tqctl](installation.md), then sign in, find a lab, and start it.

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
LAB                                     MODE    MACHINES  TASKS  OWNER     VERSION  PUBLIC
watch-a-linux-service-recover           lesson  1         2      -         3        yes
put-a-web-page-live-with-docker-compose lesson  1         3      -         5        yes
intro-to-our-network                    lesson  2         4      acme      1        -
```

Every lab's full name starts with its organisation's name. `lab ls` leaves that prefix off, and a command that takes a lab accepts it with or without the prefix.

## Start a lab

```console
$ tqctl start watch-a-linux-service-recover
session 3f9a1c2e provisioning...
session 3f9a1c2e ready in 3.2s  (watch-a-linux-service-recover, 1 machine, ends in 30m)
  cockpit  https://labs.tqdm.sh/t/9c1f6b2e.../
  ssh      tqctl ssh 3f9a1c2e
  tasks    0/2 passed  (tqctl task ls 3f9a1c2e)
```

The cockpit line is the lab's web link. The ssh line appears when the lab's machine takes SSH.

Exams are started in the browser. `tqctl start` refuses an exam and prints its page.

To see your running sessions:

```console
$ tqctl session ls
$ tqctl session describe <session-id>
```

Replace `<session-id>` with an identifier from the output.

If you author labs, `tqctl session create -f path/to/lab.yaml` starts a session from a local manifest instead.

## Connect

Open the cockpit link in your browser, or use the session identifier:

```console
$ tqctl ssh <session-id>
```

SSH requires an SSH client on your computer and a lab machine that supports SSH.

## End a session

When you no longer need the session:

```console
$ tqctl session destroy <session-id>
```

Ending a session stops its machines. Save any files you need before ending it.

Continue with [lab sessions](labs.md) or [SSH and port forwarding](connections.md).
