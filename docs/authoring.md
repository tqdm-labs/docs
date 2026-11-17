# Author a lab

<span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations only</span>

Write a lab as a file, try it in a real session, and push it to your organisation, all from the terminal.
{: .lead }

This walkthrough builds one small lab, from an empty folder to a published lesson. Every command shows the real output of `tqctl v0.6.0`, so you can compare your terminal with the page as you go.

The lab is called *Find what filled the disk*. A student gets one Linux machine whose disk is filling up: somewhere under `/var/log`, a service left a 400 MB debug log. The student has to find that file and delete it without deleting the service's live log beside it. The platform checks both conditions and marks the task done as soon as they hold.

## Before you start

You need:

- `tqctl` on your computer. See [Install tqctl](installation.md).
- A signed-in CLI. See [Sign in](authentication.md).
- An organisation account with permission to write labs. A personal account runs lessons and playgrounds but cannot author.

Run every command on this page in your own terminal, in the folder where you keep your labs.

## Scaffold the lab

`tqctl lab new` creates a folder named after the lab's slug, with a working example lab inside:

```console
$ tqctl lab new tqdm-find-a-full-disk
wrote tqdm-find-a-full-disk/lab.md and tqdm-find-a-full-disk/static/
validate it: tqctl lab validate -f tqdm-find-a-full-disk/lab.md
```

See what it made:

```console
$ tree tqdm-find-a-full-disk
tqdm-find-a-full-disk
├── lab.md
└── static

2 directories, 1 file
```

A lab is a folder, and the folder is everything the platform needs:

- `lab.md` holds the machines, the tasks and the text the student reads.
- `static/` holds pictures for that text. Put a png, jpeg, gif or webp in it and link it from `lab.md` as `static/<name>.png`.

The slug, `tqdm-find-a-full-disk`, is the lab's name inside your organisation. Pushing the same slug again makes a new version of the same lab, not a second lab.

## Read the scaffold

Open `lab.md`. The scaffold is already a complete lab with one task, so read it before you change it:

```markdown title="tqdm-find-a-full-disk/lab.md" linenums="1"
---
kind: Lab
slug: tqdm-find-a-full-disk
title: A new lab
ttl: 1h

# The useful-commands card, folded above the first task. Up to 20 entries.
# commands:
#   - run: ls /home/student
#     note: what the student starts with

network:
  egress: ["*"]

machines:
  - name: station
    image: base:latest
    resources: {cpus: 1, mem: 1024MiB}

# One entry per ::task block below, keyed by the block's id. A script runs in
# the guest as root under /bin/sh -ec, so every line is an assertion and the
# first failing line fails the task.
tasks:
  hello:
    machine: station
    auto: 10s
    timeout: 5
    script: test -s /home/student/hello.txt
---

Everything above the first ::task block is the lab's overview. Pictures live in
static/ beside this file: drop a png, jpeg, gif or webp in there and reference
it with markdown's image form, where the path is static/name.png and the title
is the caption the student reads under it.

::task{id="hello" title="Say hello"}
Write a line into **/home/student/hello.txt**, then read it back:

    cat /home/student/hello.txt

::hint
Any command that writes a file will do, shell redirection included.
::
::
```

The two `---` lines split the file in two.

**The manifest**, lines 1 to 29, describes the environment. The platform reads it; the student never sees it.

- `kind`, `slug` and `title` name the lab. Students see the title.
- `ttl` is how long a session lives before the platform ends it.
- `network.egress` lists the sites the machines may reach. `["*"]` allows any public site, and `[]` cuts the lab off from the internet.
- `machines` lists the machines a session gets, each with a name, an image, and its CPUs and memory.
- `tasks` holds one check per task, keyed by the task's id.

**The lab text**, from line 31, is Markdown the student reads beside the terminal.

- Everything before the first `::task` block is the overview.
- Each `::task{id="..." title="..."}` block is one task card. Its `id` matches a key under `tasks` in the manifest.
- An indented line inside a task shows as a command.
- A `::hint` block inside a task stays folded until the student opens it.

## Write your lab

Replace the whole of `lab.md` with this lab:

```markdown title="tqdm-find-a-full-disk/lab.md" linenums="1" hl_lines="17 30 31"
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

What changed from the scaffold:

- **Lines 4 to 8** describe the lab. `description` and `topics` appear on the lab's card in the catalog. `mode: lesson` makes it a guided lesson with tasks. The other modes are `playground`, a machine to explore with no tasks, and `exam`, graded once when the student submits. `ttl: 30m` is plenty for one task.
- **Lines 10 to 14** fill the useful-commands card, a short list the student can open above the first task. Each entry is a command and a note on what it tells you.
- **Line 17** closes the internet. This lab needs nothing from outside.
- **Line 22** gives the machine 512 MiB, enough for a shell and a few files.
- **Lines 24 to 31** are the check for the lab's one task, `free-space`. It runs on `station` as root. `auto: 5s` runs it every five seconds, so the task turns green on its own as soon as the student deletes the file. `timeout: 5` stops a single run after five seconds.

The check is two lines, and each line is an assertion. The first line that fails, fails the task:

- **Line 30**, `test ! -e /var/log/app/debug.log.1`, passes once the big file is gone.
- **Line 31**, `test -s /var/log/app/app.log`, passes while the live log exists and is not empty. A student who empties the whole folder fails here.

!!! warning "A line that starts with `!` never fails"
    Inside `test`, the `!` is an argument, so line 30 is safe. A line that *begins* with `!`, such as `! grep -q error app.log`, is exempt from the shell's stop-on-error rule and never fails the task. Write the negative as `if grep -q error app.log; then exit 1; fi` instead.

## Prepare the machine

The check expects a 400 MB file that does not exist yet. An init script creates it. An init script runs once per session, as root, after the machine boots and before the student gets it. Create one from the template:

```console
$ cd tqdm-find-a-full-disk
$ tqctl lab script new 10_fill_disk --machine station
wrote scripts/init_10_fill_disk.sh
fill in main, then validate the lab: tqctl lab validate -f lab.md
```

The lab now has a `scripts/` folder:

```console
$ tree .
.
├── lab.md
├── scripts
│   └── init_10_fill_disk.sh
└── static

3 directories, 2 files
```

When a machine has several init scripts, they run in name order, which is what the `10_` prefix is for. `--machine station` wrote the target machine into the script's header, beside its timeout in seconds:

```bash title="scripts/init_10_fill_disk.sh"
#!/usr/bin/env bash
# machine: station
# timeout: 60
```

Below the header, the template brings helpers so you do not write them yourself. The ones you will use most:

| Helper | What it does |
|---|---|
| `ok <message>` | Logs a step that worked. The session's output shows it. |
| `die <message>` | Stops the script with a reason, which fails the session. |
| `write_file <path> <owner> <mode>` | Writes what it reads on stdin to a file in one step, with its owner and mode. |
| `retry <attempts> <delay> <command>` | Runs a command until it works, waiting twice as long after each failure. |
| `as_student <command>` | Runs a command as the student, in their home folder. |

The template's comments carry a few rules worth knowing early:

- A non-zero exit fails the session, and the script's last lines become the reason.
- Keep it fast. Install packages in the image, not here.
- A student with `sudo` can read every file on the machine, so never leave an answer in a file.

At the bottom of the template is an empty `main`. Replace it with this lab's setup:

```bash title="scripts/init_10_fill_disk.sh" linenums="1"
main() {
  mkdir -p /var/log/app
  fallocate -l 400M /var/log/app/debug.log.1
  echo "service started" | write_file /var/log/app/app.log root:root 644
  ok "filled /var/log/app"
}
```

- **Line 3** makes the 400 MB file. `fallocate` reserves the space at once, without writing 400 MB of data.
- **Line 4** writes the live log the student must keep, owned by root and readable by everyone.
- **Line 5** logs a line you will see when the session starts.

## Validate

Validation runs the same checks as the platform, so a lab that passes here is accepted on push:

```console
$ tqctl lab validate -f lab.md
ok: tqdm-find-a-full-disk (1 machine(s), 1 task(s), ttl 30m0s)
overview: 110 bytes
commands: 2
init script: scripts/init_10_fill_disk.sh on station, timeout 60s
```

Each line confirms one part of the lab: one machine and one task with a 30-minute lifetime, the overview text, the two useful commands, and the init script on `station`.

A mistake names the field at fault and exits with status 1. Here line 26 says `stationn`, a machine that does not exist:

```{.console .fail}
$ tqctl lab validate -f lab.md
tasks: task "free-space" checks unknown machine "stationn"
```

Fix it and validate again before you go on.

## Push

Push uploads the lab to your organisation without starting a session. Each push is a new version:

```console
$ tqctl lab push -f lab.md
lab tqdm-find-a-full-disk v1
init script: scripts/init_10_fill_disk.sh on station, timeout 60s
```

The lab is now a draft. Only your organisation sees it until you publish it.

## Try it in a session

Start a session from your local copy. The command uploads it as the next version, boots its machines and runs the init script:

```console
$ tqctl session create -f lab.md
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

Read it from the top:

- `v2` is the version this session runs. The push made `v1`, and creating the session from the file made `v2`.
- `1738d24a` is the session's id. Every command below takes it.
- `cockpit` opens the lab in a browser as a student sees it.
- `student` is the token that lets a student in.
- `init` shows your script ran on `station` and passed, with the `ok` line from `main`.

Open the cockpit link to see the lab as a student does. Treat the link and the student token like passwords: anyone holding them can use the session.

## Solve it as a student would

First check that the task fails before anyone solves it. A check that passes at the start lets every student through:

```console
$ tqctl task check 1738d24a
FAIL  free-space (exit 1)
1/1 checks failed
```

Now work through the lab. `tqctl exec` runs a command on the session's machine from your terminal. Find the biggest folder:

```console
$ tqctl exec 1738d24a -- sh -c 'du -sh /var/log/* | sort -h | tail -3'
68K	/var/log/dpkg.log
8.1M	/var/log/journal
401M	/var/log/app
```

Look inside it:

```console
$ tqctl exec 1738d24a -- ls -lh /var/log/app
total 401M
-rw-r--r-- 1 root root   16 Nov 15 13:45 app.log
-rw-r--r-- 1 root root 400M Nov 15 13:45 debug.log.1
```

Delete the debug log and check again:

```console
$ tqctl exec 1738d24a -- sudo rm /var/log/app/debug.log.1
$ tqctl task check 1738d24a
PASS  free-space (exit 0)
all 1 checks passed
```

The task list agrees:

```console
$ tqctl task ls 1738d24a
STATE  TASK        MACHINE  TITLE
ok     free-space  station  Free the disk
1/1 passed
```

When you are done, end the session:

```console
$ tqctl session destroy 1738d24a
session 1738d24a tearing down
```

## Publish

A pushed lab is a draft that only your organisation sees. When it is ready for students, put it in your catalog:

```console
$ tqctl lab publish tqdm-find-a-full-disk
```

`tqctl lab unpublish tqdm-find-a-full-disk` takes it back out as a draft. Check your organisation's review process before you publish.

## Next steps

- Use your own machine image: `tqctl image build` and `tqctl image push`, then name it as `image: <org>/<name>:<tag>`. See `tqctl image --help`.
- Find every option in the [command reference](commands.md).
