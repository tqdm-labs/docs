# Build and publish a lab

<span class="org-badge"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>Organisations only</span>

Take a lab folder from your computer to your organisation's members, and keep it up to date afterwards.
{: .lead }

This page is the reference for a lab's life after you write it: validating, pushing versions, trying them, publishing and updating. For a first lab from start to finish, follow [Author a lab](authoring.md). For every field in the lab file, see [The lab file](lab-file.md).

## The lifecycle

A lab moves through the same steps every time you change it:

1. **Validate** the folder on your computer. Nothing leaves your machine.
2. **Push** it to your organisation. Each push is a new version, and a new lab starts as a draft.
3. **Try** a version in a real session and solve it as a student would.
4. **Publish** it, once, to put it in front of your organisation's members.
5. **Update** it by editing the folder and pushing again. A published lab stays published.

!!! note "A lab never leaves your organisation"
    Nobody outside your organisation ever sees your labs: not other organisations, not the public, whatever state the lab is in. Inside your organisation, a draft is for owners only, and publishing shows the lab to your members.

Pushing and publishing need your organisation's publishing permission, which the platform operator grants. Without it, both are refused with "publishing is granted by the platform operator". Starting a session from a local file pushes it first, so it needs the permission too. Validating and unpublishing never do.

## Validate

Run validation from the lab folder:

```console
$ tqctl lab validate -f lab.md
ok: find-a-full-disk (1 machine(s), 1 task(s), ttl 30m0s)
overview: 110 bytes
commands: 2
init script: scripts/init_10_fill_disk.sh on station, timeout 60s
```

Validation runs the same checks as the platform, so a lab that passes here is accepted on push. It reads `lab.md`, the pictures in `static/` and the init scripts in `scripts/`. A mistake names the field at fault and exits with status 1, which makes `tqctl lab validate` a good check to run before every commit or in CI:

```{.console .fail}
$ tqctl lab validate -f lab.md
tasks: task "free-space" checks unknown machine "stationn"
```

!!! note "Always pass `-f lab.md`"
    `lab validate`, `lab push` and `session create` look for `lab.yaml` when you leave out `-f`. Name the file you mean.

## Push a version

Push uploads the folder to your organisation without starting anything:

```console
$ tqctl lab push -f lab.md
lab find-a-full-disk v1
init script: scripts/init_10_fill_disk.sh on station, timeout 60s
```

What a push does:

- It validates first, so a broken folder never reaches the platform.
- It uploads `lab.md`, its pictures and its init scripts together, as one version.
- The first push of a slug creates the lab as a draft. Every later push replaces its content and counts up the version: `v2`, `v3` and so on. The platform keeps the latest version only, so keep your lab folder in version control.
- A push never changes whether the lab is published.

!!! warning "Lab names are unique across the whole platform"
    A slug belongs to the first organisation that pushes it. If another organisation already owns a slug, your push is refused with `lab "<slug>" is owned by another organisation`. Pick a more specific slug, such as one that starts with your organisation's name, and push again.

## Try a version in a session

`tqctl session create` starts a session from your local file. It uploads the file as the next version first, so you always try exactly what is on your disk:

```console
$ tqctl session create -f lab.md
lab find-a-full-disk v2
session 1738d24a provisioning...
session 1738d24a ready in 2.56s  (find-a-full-disk, 1 machine, ends in 29m)
  cockpit  <cockpit-link>
  student  <student-token>
  ssh      tqctl ssh 1738d24a
  tasks    0/1 passed  (tqctl task ls 1738d24a)
  init     station init_10_fill_disk.sh succeeded, exit 0, 111ms
             13:45:39 init_10_fill_disk.sh: ok: filled /var/log/app
             init_10_fill_disk.sh: ok in 0s
```

Two options help when you script it:

- `--timeout <duration>` waits longer for the session to be ready. The default is one minute.
- `-q` prints only the session id once it is ready, for use in a script.

Then test the lab the way a student would meet it:

```console
$ tqctl task check <session-id>
$ tqctl exec <session-id> -- <command>
$ tqctl session destroy <session-id>
```

Check that every task fails before you solve it: a check that passes at the start lets every student through. [Work with labs](labs.md) and [Connect to a machine](connections.md) cover the session commands in full.

## See your labs

List the labs you can run, and look inside one:

```console
$ tqctl lab ls
$ tqctl lab describe find-a-full-disk
```

`lab describe` shows a lab's machines and its tasks as the platform stored them, which is a quick way to confirm what a push changed.

## Publish

A draft is for your organisation's owners: members do not see it. Publishing puts the lab in front of your organisation's members, who can then start it:

```console
$ tqctl lab publish find-a-full-disk
```

- Publishing takes the slug, not a file. It publishes whatever you last pushed.
- Publishing is not a version. Running it twice is harmless.
- From then on, every push updates the published lab directly. Try a change in a session before you push it.

Check your organisation's review process before you publish.

## Unpublish

Unpublishing returns the lab to a draft:

```console
$ tqctl lab unpublish find-a-full-disk
```

- The lab leaves your members' lists and stays visible to your organisation's owners.
- Sessions that are already running are not touched. Students finish what they started.
- The lab and its latest version are kept. Publish again whenever you are ready.

## Update a published lab

Updating is the same loop as writing:

```console
$ tqctl lab validate -f lab.md
$ tqctl session create -f lab.md
$ tqctl lab push -f lab.md
```

Validate the change, try it in a session, then push. The push becomes the version students get, and the lab stays published.

## In the browser

The same steps also work in **Studio** in the web app. Studio edits a lab with a live preview, and its **Labs** page publishes and unpublishes. Labs you push from the CLI appear there too, so you can mix both.

## Next steps

- Look up every field a lab can use in [The lab file](lab-file.md).
- Use your own machine image: `tqctl image build` and `tqctl image push`, then name it as `image: <org>/<name>:<tag>`. See `tqctl image --help`.
- Find every option in the [command reference](commands.md).
