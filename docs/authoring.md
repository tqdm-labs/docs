# Author a lab

<span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations only</span>

Write a lab as a file, try it in a real session, and push it to your organisation, all from the terminal.
{: .lead }

Authoring needs an organisation account with permission to write labs. A personal account runs lessons and playgrounds but cannot author. This walkthrough builds a small lab, *Find what filled the disk*, and shows the real output of `tqctl v0.6.0` at each step.

## Scaffold the lab

```sh
tqctl lab new tqdm-find-a-full-disk
```

```text
wrote tqdm-find-a-full-disk/lab.md and tqdm-find-a-full-disk/static/
validate it: tqctl lab validate -f tqdm-find-a-full-disk/lab.md
```

A lab is a folder. `lab.md` holds the machines, the tasks and the text the student reads. Pictures go in `static/`.

## Describe the machine and the task

Replace the scaffold's contents with your lab. The part between the `---` lines is the manifest; everything after it is what the student reads, with one `::task` block per task.

```markdown title="tqdm-find-a-full-disk/lab.md"
---
kind: Lab
slug: tqdm-find-a-full-disk
title: "Find what filled the disk"
description: "Track down the file eating a machine's disk and remove it without touching the live log."
topics: [linux, storage]
mode: lesson
ttl: 30m

commands:
  - run: df -h /
    note: how full the disk is
  - run: du -sh /var/log/* | sort -h
    note: which folder is the biggest

network:
  egress: []

machines:
  - name: station
    image: base:latest
    resources: {cpus: 1, mem: 512MiB}

tasks:
  free-space:
    machine: station
    auto: 5s
    timeout: 5
    script: |
      test ! -e /var/log/app/debug.log.1
      test -s /var/log/app/app.log
---

Something on **station** wrote a huge debug log. Find it and free the space,
but keep the service's live log.

::task{id="free-space" title="Free the disk"}
Find the biggest file under **/var/log** and delete it. Leave
**/var/log/app/app.log** where it is.

    # list the folders by size, biggest last
    sudo du -sh /var/log/* | sort -h

::hint
Look inside the biggest folder with `ls -lh`.
::
::
```

A task's `script` runs on the machine as root. Every line is an assertion: the first line that fails, fails the task. `auto: 5s` re-checks the task every five seconds, so the student sees it pass without asking.

## Prepare the machine

An init script runs once per session, before the student gets the machine. Create one from the template:

```sh
cd tqdm-find-a-full-disk
tqctl lab script new 10_fill_disk --machine station
```

```text
wrote scripts/init_10_fill_disk.sh
fill in main, then validate the lab: tqctl lab validate -f lab.md
```

The template comes with helpers such as `write_file`, `retry` and `ok`. Replace its `main` with this lab's setup:

```bash title="scripts/init_10_fill_disk.sh"
main() {
  mkdir -p /var/log/app
  fallocate -l 400M /var/log/app/debug.log.1
  echo "service started" | write_file /var/log/app/app.log root:root 644
  ok "filled /var/log/app"
}
```

## Validate

```sh
tqctl lab validate -f lab.md
```

```text
ok: tqdm-find-a-full-disk (1 machine(s), 1 task(s), ttl 30m0s)
overview: 110 bytes
commands: 2
init script: scripts/init_10_fill_disk.sh on station, timeout 60s
```

Validation runs the same checks as the platform, so a lab that passes here is accepted on push. A mistake names the field at fault and exits 1. Here a task points at a machine that does not exist:

```text
tasks: task "free-space" checks unknown machine "stationn"
```

## Push

Push uploads the lab to your organisation without starting a session. Each push is a new version:

```sh
tqctl lab push -f lab.md
```

```text
lab tqdm-find-a-full-disk v1
init script: scripts/init_10_fill_disk.sh on station, timeout 60s
```

## Try it in a session

Start a session from your local copy. The command uploads it as the next version, boots its machines and runs the init script:

```sh
tqctl session create -f lab.md
```

```text
lab tqdm-find-a-full-disk v2
session 1738d24a provisioning...
session 1738d24a ready in 2.56s  (tqdm-find-a-full-disk, 1 machine, ends in 29m)
  cockpit  <cockpit-link>
  student  <student-token>
  ssh      tqctl ssh 1738d24a
  tasks    0/1 passed  (tqctl task ls 1738d24a)
  init     station init_10_fill_disk.sh succeeded, exit 0, 111ms
             13:45:39 init_10_fill_disk.sh: ok: filled /var/log/app
             init_10_fill_disk.sh: ok in 0s
```

Open the cockpit link in your browser to see the lab as a student does. Treat the link and the student token like passwords: anyone holding them can use the session.

## Solve it as a student would

Check that the task fails before you solve it. A check that passes at the start lets every student through.

```sh
tqctl task check 1738d24a
```

```text
FAIL  free-space (exit 1)
1/1 checks failed
```

Work through the lab from the terminal:

```sh
tqctl exec 1738d24a -- sh -c 'du -sh /var/log/* | sort -h | tail -3'
```

```text
68K	/var/log/dpkg.log
8.1M	/var/log/journal
401M	/var/log/app
```

```sh
tqctl exec 1738d24a -- ls -lh /var/log/app
```

```text
total 401M
-rw-r--r-- 1 root root   16 Nov 15 13:45 app.log
-rw-r--r-- 1 root root 400M Nov 15 13:45 debug.log.1
```

```sh
tqctl exec 1738d24a -- sudo rm /var/log/app/debug.log.1
tqctl task check 1738d24a
```

```text
PASS  free-space (exit 0)
all 1 checks passed
```

```sh
tqctl task ls 1738d24a
```

```text
STATE  TASK        MACHINE  TITLE
ok     free-space  station  Free the disk
1/1 passed
```

When you are done, end the session:

```sh
tqctl session destroy 1738d24a
```

```text
session 1738d24a tearing down
```

## Publish

A pushed lab is a draft that only your organisation sees. When it is ready for students, put it in your catalog:

```sh
tqctl lab publish tqdm-find-a-full-disk
```

`tqctl lab unpublish tqdm-find-a-full-disk` takes it back out as a draft. Check your organisation's review process before you publish.

## Next steps

- Use your own machine image: `tqctl image build` and `tqctl image push`, then name it as `image: <org>/<name>:<tag>`. See `tqctl image --help`.
- Find every option in the [command reference](commands.md).
