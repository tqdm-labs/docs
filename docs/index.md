# From your terminal to your lab.

Find your labs, connect to a machine, and check your work with `tqctl`.
{: .lead }

[Install tqctl](installation.md){ .md-button .md-button--primary }
[Download a binary](downloads.md){ .md-button }

<figure class="connection-diagram" aria-label="Three steps to connect to a lab">
<ol class="connection-steps">
<li><span class="step-number" aria-hidden="true">1</span><strong>Sign in</strong><span>Approve your CLI sign-in in the browser.</span></li>
<li><span class="step-number" aria-hidden="true">2</span><strong>Start a lab</strong><span>Choose and launch a lab on tqdm.sh.</span></li>
<li><span class="step-number" aria-hidden="true">3</span><strong>Connect</strong><span>Find your session and open SSH with tqctl.</span></li>
</ol>
</figure>

## Your first connection

```sh
# Sign in through your browser
tqctl auth login

# Start a lab in the web interface, then find its session
tqctl session ls

# Connect using a session ID from the output
tqctl ssh <session-id>
```

Launch a published lab from the tqdm.sh web interface, then use the CLI to connect. You need an account and access to an organisation. [Follow the quickstart](quickstart.md).

## Explore the guides

| Task | Guide |
| --- | --- |
| Sign in or switch organisation | [Your account](authentication.md) |
| Inspect sessions and run task checks | [Work with labs](labs.md) |
| Open SSH or forward an application port | [Connect to a machine](connections.md) |
| Find an option or command | [Command reference](commands.md) |
| Resolve an installation or connection error | [Troubleshooting](troubleshooting.md) |

For exams, follow your instructor's instructions in the browser.
