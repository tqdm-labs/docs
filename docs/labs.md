# Work with labs

A lab defines the environment. A session is a running instance of that lab. The commands available to you depend on your organisation and role.

## Browse available labs

```console
$ tqctl lab ls
$ tqctl lab describe <lab-slug>
```

## Start or inspect a session

To launch a published lab, run `tqctl start <lab>` or use the tqdm.sh web interface. Exams are started in the browser. Then inspect your session from the CLI:

```console
$ tqctl session ls
$ tqctl session describe <session-id>
```

Authors with a local manifest can start a session from that file:

```console
$ tqctl session create -f path/to/lab.yaml
```

This command validates and submits a local definition. It does not accept a catalog lab identifier. Your account must have permission to create the session.

## Check your tasks

```console
$ tqctl task ls <session-id>
$ tqctl task check <session-id>
```

To run a single task's check, add `--task <task-id>`. Use the lab's instructions to decide when to run a check.

## Run a command

```console
$ tqctl exec <session-id> -- uname -a
```

For a lab with several machines, select one with `-m`:

```console
$ tqctl exec <session-id> -m <machine-name> -- uname -a
```

## End a session

```console
$ tqctl session destroy <session-id>
```

Save your work first. Ending a session stops its machines. To take an exam, use the web interface and follow your instructor's instructions.

## Author a lab

<span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations</span>

To write your own lab, test it in a session, and push it to your organisation, follow [Author a lab](authoring.md).
