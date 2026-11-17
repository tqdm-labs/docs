# The lab file

Every field a lab can use, what it does and the limits the platform enforces.
{: .lead }

A lab is a folder with one file, `lab.md`, plus optional pictures and init scripts. This page describes all of it. For a guided first lab, follow [Author a lab](authoring.md); for pushing and publishing, see [Build and publish a lab](publishing.md).

## The folder

```console
$ tree web-behind-a-proxy
web-behind-a-proxy
├── lab.md
├── scripts
│   └── init_10_setup.sh
└── static
    └── topology.png

3 directories, 3 files
```

| Path | Required | Holds |
|---|---|---|
| `lab.md` | yes | The manifest and the text the student reads. Keep this exact name. |
| `static/` | no | Pictures the text shows. |
| `scripts/` | no | Init scripts that prepare machines before the student arrives. |

`tqctl lab new <slug>` creates the folder with a working `lab.md`. `tqctl lab script new <name> --machine <machine>` adds an init script.

## Two halves

`lab.md` is split by two lines that are exactly `---`:

- **The manifest**, between the `---` lines, is YAML that describes the environment: machines, networks and the checks behind each task. The student never sees it.
- **The lab text**, after the second `---`, is Markdown the student reads beside the terminal, with blocks such as `::task` for each task.

Every manifest key on this page is checked. A key the platform does not know is refused with `manifest: unknown field "<key>"`, so a typo never goes unnoticed.

Here is a complete lab that uses most of the format. The sections below explain each part.

```markdown title="web-behind-a-proxy/lab.md" linenums="1"
---
kind: Lab
slug: web-behind-a-proxy
title: "Reach a web server through a proxy"
description: "Find why the web server is unreachable from the office network and fix the route."
topics: [linux, networking]
mode: lesson
ttl: 45m

commands:
  - run: ip route
    note: where this machine sends traffic
  - run: curl -sI http://10.20.0.10
    note: whether the web server answers

network:
  egress: ["*.debian.org", "github.com"]

networks:
  - name: office
    subnet: 10.10.0.0/24
  - name: dmz
    subnet: 10.20.0.0/24
    internet: false
    joins: [office]

machines:
  - name: workstation
    image: base:latest
    resources: {cpus: 1, mem: 512MiB}
    interfaces:
      - network: office
        address: 10.10.0.10
    persist:
      - path: /home/student/work
        size: 1GiB
  - name: web
    image: base:latest
    resources: {cpus: 1, mem: 512MiB}
    start_after: [workstation]
    interfaces:
      - network: dmz
        address: 10.20.0.10
    expose:
      - port: 80
        proto: http
        subdomain: site
  - name: grader
    image: base:latest
    resources: {cpus: 1, mem: 256MiB}
    hidden: true
    interfaces:
      - network: office

tasks:
  reach-web:
    machine: workstation
    timeout: 10
    auto: 5s
    script: |
      curl -sf -o /dev/null http://10.20.0.10
---

The office and the DMZ are two networks. Open [the workstation](tab:workstation)
and start from there.

![The two networks](static/topology.png "The office and the DMZ")

::note{kind="warning"}
The web server has no internet access on purpose.
::

::details{summary="How the networks are wired"}
The office is 10.10.0.0/24 and the DMZ is 10.20.0.0/24.
::

::task{id="reach-web" title="Reach the web server" passes_when="the workstation gets a 200 from http://10.20.0.10"}
Make **http://10.20.0.10** answer from the workstation.

    curl -sI http://10.20.0.10

::hint
Compare `ip route` on both machines.
::
::done
The server answers. Go back to [the task](task:reach-web) to read why.
::
::
```

Validation prints how the platform reads it, including the addresses it gave each machine:

```console
$ tqctl lab validate -f lab.md
ok: web-behind-a-proxy (3 machine(s), 1 task(s), ttl 45m0s)
network office 10.10.0.0/24, gateway 10.10.0.1
network dmz 10.20.0.0/24, gateway 10.20.0.1, joins office, no internet
  workstation  eth0 office 10.10.0.10
  web          eth0 dmz 10.20.0.10
  grader       eth0 office 10.10.0.2
overview: 170 bytes
commands: 2
conditions: 1 of 1 tasks
notes: 1
folds: 1
completed texts: 1 of 1 tasks
init script: scripts/init_10_setup.sh on web, timeout 60s
```

## About the lab

| Key | Required | Default | What it does |
|---|---|---|---|
| `kind` | yes | | Always `Lab`. |
| `slug` | yes | | The lab's name on the platform: 2 to 63 lowercase letters, digits and hyphens, starting with a letter or digit. |
| `title` | no | | The name students see. |
| `description` | no | | One line of at most 160 characters, shown on the lab's card. |
| `topics` | no | | Up to 8 tags such as `linux` or `kubernetes`: lowercase letters, digits and single hyphens, at most 32 characters each. |
| `mode` | no | `lesson` | `lesson`, `exam` or `playground`. See [Modes](#modes). |
| `ttl` | no | `2h` | How long a session lives, as a duration such as `30m`, `1h30m` or `2h`. At most `24h`. |

!!! warning "Lab names are unique across the whole platform"
    A slug belongs to the first organisation that pushes it. A push under a slug another organisation owns is refused with `lab "<slug>" is owned by another organisation`, so choose specific names, for example ones that start with your organisation's name.

### Modes

| Mode | What the student gets |
|---|---|
| `lesson` | Task cards checked as the student works, with hints, completed text and a "passes when" line. |
| `exam` | Tasks graded once, when the student submits. Hints, useful commands, completed text and `auto` are left out, and validation lists what it ignored. |
| `playground` | Machines to explore with the lab text as a guide. Completed text and "passes when" lines are left out. |

### Useful commands

`commands` fills the useful-commands card, a short list the student can open above the first task. The platform never runs these commands; they are reading material.

```yaml
commands:
  - run: df -h /
    note: how full the disk is
```

| Key | Limit |
|---|---|
| `run` | Required. One line, at most 200 characters. |
| `note` | Required. At most 120 characters. |

Up to 20 entries.

## Machines

`machines` lists the machines every session gets: 1 to 4 of them.

| Key | Required | What it does |
|---|---|---|
| `name` | yes | Lowercase letters, digits and hyphens, starting with a letter, up to 31 characters. Tasks, init scripts and `tab:` links use it. |
| `image` | yes | What the machine runs, written `name:tag`. See [Images](#images). |
| `resources.cpus` | yes | 1 to 8 CPUs. |
| `resources.mem` | yes | Memory as `<n>MiB` or `<n>GiB`, at least `128MiB`. |
| `address` | no | A fixed address on the lab's one network. See [Networks](#networks). |
| `interfaces` | no | Attach the machine to named networks. See [Networks](#networks). |
| `start_after` | no | Names of machines that must start before this one. |
| `expose` | no | Ports reachable from outside the session. See [Exposed ports](#exposed-ports). |
| `persist` | no | A disk that outlives the session. See [Persistent disk](#persistent-disk). |
| `hidden` | no | `true` runs the machine without ever showing it to the student, for graders and background services. At least one machine must stay visible. |

A lab uses at most 8 CPUs and 8 GiB of memory across all its machines. One CPU and 512 MiB is plenty for most single-machine tasks.

### Images

| Form | Example | What it is |
|---|---|---|
| `name:tag` | `base:latest` | A platform image. `base:latest` is a Debian machine with a shell, common tools and a `student` user. |
| `<org>/<name>:<tag>` | `acme/webapp:1.2` | An image your organisation built and pushed with `tqctl image build` and `tqctl image push`. Only your organisation's labs can use it, and your organisation needs image pushing enabled by the platform operator. |

An image the platform does not have is reported when you push, and a session that uses it fails to start.

## Networks

Every machine has a network connection. Without any network keys, the machines of a session share one network and the platform picks the addresses. Add network keys only when the lab is about networking.

### Internet access

`network.egress` decides which internet sites the machines may reach, on the web ports 80 and 443:

| Value | Meaning |
|---|---|
| left out | Any public site. |
| `[]` | No internet at all. |
| a list | Only these names. |

An entry in the list is one of:

- An exact name: `github.com`.
- Every name under a domain: `*.debian.org` matches `deb.debian.org` but not `debian.org` itself.
- A `*` inside one label: `api*.example.com` matches `api2.example.com`. It never crosses a dot.
- `*` alone: any public name, the same as leaving the key out.

Up to 64 entries. Machines only ever reach public addresses: never private networks or the platform's own hosts, whatever the list says.

### One network with fixed addresses

To choose the addresses, give the network a subnet and each machine an `address`:

```yaml
network:
  subnet: 192.168.50.0/24
machines:
  - name: client
    image: base:latest
    resources: {cpus: 1, mem: 512MiB}
    address: 192.168.50.10
  - name: server
    image: base:latest
    resources: {cpus: 1, mem: 512MiB}
    address: 192.168.50.20
```

- The subnet must sit inside `10.0.0.0/8` or `192.168.0.0/16`, with a prefix length from `/16` to `/28`.
- The gateway is the subnet's first address, here `192.168.50.1`.
- A machine without an `address` gets the lowest free one.

`172.16.0.0/12` belongs to the platform and is refused, even though it is a private range:

```{.console .fail}
$ tqctl lab validate -f lab.md
manifest: network.subnet "172.16.5.0/24" is inside 172.16.0.0/12, reserved for the platform; use 10.0.0.0/8 or 192.168.0.0/16
```

### Several networks

`networks` declares up to 4 named networks, and each machine attaches with `interfaces`. A machine's first interface is `eth0`, its second `eth1`, and so on.

| Key | Required | What it does |
|---|---|---|
| `name` | yes | Lowercase letters, digits and hyphens, starting with a letter. |
| `subnet` | yes | Same rules as above. Subnets may not overlap. |
| `gateway` | no | The router's address. Defaults to the subnet's first address. |
| `private` | no | `true` makes a network with no gateway and no way out, only the machines on it. |
| `internet` | no | `false` cuts off the internet for machines whose default route is this network. |
| `joins` | no | Other networks this one is routed to, inside the session. Name each pair once, from one side. |

Each entry in a machine's `interfaces` has a `network` and an optional `address`. A machine attaches to up to 4 networks, never the same one twice, and every declared network needs at least one machine. With `networks`, give addresses through `interfaces`, not `address`.

### Exposed ports

`expose` makes a port on a machine reachable from outside the session.

| Key | What it does |
|---|---|
| `port` | The port on the machine, 1 to 65535. |
| `proto` | `http`, `tcp` or `udp`. |
| `subdomain` | Required for `http`: the start of the address students open in a browser. Lowercase letters and digits, starting with a letter, up to 20 characters, unique in the lab. |
| `desktop` | `true` on one `http` exposure opens it as the session's Desktop tab, for labs built on a desktop image. |

The machine needs an interface on a network that is not `private`.

### Persistent disk

`persist` gives a machine one disk that outlives its sessions:

```yaml
persist:
  - path: /home/student/work
    size: 1GiB
```

- `path` is an absolute folder. It cannot be `/` or a system folder such as `/etc`, `/usr` or `/run`.
- `size` is from `128MiB` to `32GiB`.
- The disk is kept when a session is started with a workspace, for example `tqctl session create -f lab.md --workspace <name>`, and comes back in the next session with the same workspace.

## Checks

Each key under `tasks` is a task id, and its value is the check behind that task. Every check needs a `::task` block with the same id in the lab text, and every block needs a check.

```yaml
tasks:
  free-space:
    machine: station
    auto: 5s
    timeout: 5
    script: |
      test ! -e /var/log/app/debug.log.1
      test -s /var/log/app/app.log
```

| Key | Required | Default | What it does |
|---|---|---|---|
| `machine` | yes | | The machine the check runs on. |
| `script` | yes | | Shell lines run as root with `/bin/sh -ec`. Every line is an assertion: the first line that fails, fails the task. At most 32 KiB. |
| `timeout` | no | `30` | Seconds before one run of the check is stopped, 1 to 120. |
| `auto` | no | off | Run the check on its own at this interval, at least `1s`, so the task turns green without the student asking. |

Task ids are 2 to 63 lowercase letters, digits and hyphens. A lab has up to 20 tasks.

!!! warning "A line that starts with `!` never fails"
    A line that begins with `!`, such as `! grep -q error app.log`, is exempt from the shell's stop-on-error rule, so it never fails the task. Validation points these lines out. Write the negative as `if grep -q error app.log; then exit 1; fi`. Inside `test`, as in `test ! -e`, the `!` is safe.

## The lab text

Everything after the manifest is Markdown, with blocks that start with a line beginning `::`. A line that is exactly `::` closes the block that is open.

### The overview

The text before the first block is the overview: what the student reads before the tasks. Up to 8 KiB.

### Tasks

```markdown
::task{id="reach-web" title="Reach the web server" passes_when="the workstation gets a 200 from http://10.20.0.10"}
Make **http://10.20.0.10** answer from the workstation.

    curl -sI http://10.20.0.10

::hint
Compare `ip route` on both machines.
::
::done
The server answers.
::
::
```

| Property | Required | What it does |
|---|---|---|
| `id` | yes | Matches a key under `tasks` in the manifest. |
| `title` | no | The task card's title, up to 120 characters. |
| `passes_when` | no | One line, up to 200 characters, telling the student what the check looks for. |

Inside a task:

- The text up to the first inner block is the instructions, up to 8 KiB. An indented line shows as a command.
- `::hint` adds a hint that stays folded until the student opens it. Up to 5 per task, 2 KiB each.
- `::done` adds the text shown once the task passes. One per task, up to 2 KiB.

Property values go in double quotes and cannot contain a double quote.

### Notes and folds

Outside tasks, two more blocks shape the reading:

```markdown
::note{kind="warning"}
The web server has no internet access on purpose.
::

::details{summary="How the networks are wired"}
The office is 10.10.0.0/24 and the DMZ is 10.20.0.0/24.
::
```

- `::note` is a callout. `kind` is `info` (the default), `warning` or `error`.
- `::details` is a fold the student opens. `summary` is required and is the line they click.

Blocks do not nest, except `::hint` and `::done` inside a task. All the lab text together is at most 32 KiB.

### Links

| Link | Opens |
|---|---|
| `[the workstation](tab:workstation)` | That machine's terminal tab. |
| `[the task](task:reach-web)` | That task's card. |

A link to a machine or task the lab does not declare is refused.

### Pictures

Put pictures in `static/` and show them with Markdown's image form. The text in quotes is the caption under the picture:

```markdown
![The two networks](static/topology.png "The office and the DMZ")
```

- png, jpeg, gif or webp, recognised from the file's content. SVG is refused.
- File names use lowercase letters, digits, dots, hyphens and underscores, up to 64 characters.
- Up to 20 pictures, 1 MiB each and 8 MiB in total.
- A picture the text names but `static/` lacks is refused. A picture nothing names is pointed out.

## Init scripts

Init scripts prepare machines before the student arrives: they create files, start services or break something on purpose. Each script runs once per session, as root, after its machine boots.

```bash title="scripts/init_10_setup.sh"
#!/usr/bin/env bash
# machine: web
# timeout: 60

main() {
  echo "service started" | write_file /var/log/app/app.log root:root 644
  ok "wrote the live log"
}
```

- **Name:** `scripts/init_<name>`, such as `init_10_setup.sh`. Files that do not start with `init_` are left out, and validation says so.
- **Order:** a machine's scripts run one at a time, in name order. Pad the numbers to the same width: `init_10` sorts before `init_9`.
- **Header:** `# machine: <name>` once, naming one machine. `# timeout: <seconds>` from 1 to 300, default 60. A machine's scripts add up to at most 600 seconds.
- **Body:** starts with `#!`. Up to 64 KiB each, 20 scripts and 256 KiB in total.
- **Failure:** a non-zero exit or a timeout stops that machine's remaining scripts and fails the session, with the reason in the session's output.

`tqctl lab script new` writes the template with the header and helpers such as `ok`, `die`, `write_file`, `retry` and `as_student`. [Author a lab](authoring.md#prepare-the-machine) walks through one.

## Limits

| Thing | Limit |
|---|---|
| Machines | 1 to 4 |
| CPUs | 1 to 8 per machine, 8 per lab |
| Memory | at least 128 MiB per machine, 8 GiB per lab |
| Networks | up to 4, each machine on up to 4 |
| Internet entries | 64 |
| Session lifetime | up to 24 hours |
| Tasks | 20 |
| Check script | 32 KiB, 1 to 120 seconds |
| Hints | 5 per task, 2 KiB each |
| Overview | 8 KiB |
| Lab text | 32 KiB |
| Useful commands | 20 |
| Topics | 8 |
| Pictures | 20, 1 MiB each, 8 MiB in total |
| Init scripts | 20, 64 KiB each, 256 KiB in total |
| Persistent disk | one per machine, 128 MiB to 32 GiB |
