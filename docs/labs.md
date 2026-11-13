# Work with labs

A lab defines the environment. A session is a running instance of that lab. The commands available to you depend on your organisation and role.

## Browse available labs

```sh
tqctl lab ls
tqctl lab describe <lab-slug>
```

## Start or inspect a session

To launch a published lab, use the tqdm.sh web interface and follow the lab's instructions. Then inspect your session from the CLI:

```sh
tqctl session ls
tqctl session describe <session-id>
```

Authors with a local manifest can start a session from that file:

```sh
tqctl session create -f path/to/lab.yaml
```

This command validates and submits a local definition. It does not accept a catalog lab identifier. Your account must have permission to create the session.

## Check your tasks

```sh
tqctl task ls <session-id>
tqctl task check <session-id>
```

To run a single task's check, add `--task <task-id>`. Use the lab's instructions to decide when to run a check.

## Run a command

```sh
tqctl exec <session-id> -- uname -a
```

For a lab with several machines, select one with `-m`:

```sh
tqctl exec <session-id> -m <machine-name> -- uname -a
```

## End a session

```sh
tqctl session destroy <session-id>
```

Save your work first. Ending a session stops its machines. To take an exam, use the web interface and follow your instructor's instructions.

## Author a lab

If your role permits authoring, use the CLI's help to create, validate, and push a lab:

```sh
tqctl lab new --help
tqctl lab validate --help
tqctl lab push --help
```

Validation checks a local lab definition. Pushing uploads a lab to your organisation. Check your organisation's review process before pushing or publishing.
