<h1><img src="docs/assets/brand/favicon.svg" width="32" height="32" alt=""> tqdm.sh documentation</h1>

[docs.tqdm.sh](https://docs.tqdm.sh/)

[![CI](https://github.com/tqdm-labs/docs/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/tqdm-labs/docs/actions/workflows/check.yml)
[![Docs build and deployment](https://github.com/tqdm-labs/docs/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/tqdm-labs/docs/actions/workflows/publish.yml)

Documentation for `tqctl`, the command-line tool for [tqdm.sh](https://tqdm.sh).

- [Install tqctl](docs/installation.md)
- [Quickstart](docs/quickstart.md)
- [Downloads and checksums](docs/downloads.md)
- [Command reference](docs/commands.md)

## Preview locally

Install [uv](https://docs.astral.sh/uv/), then run:

```sh
uv sync --frozen
uv run zensical serve --dev-addr 127.0.0.1:8000
```

Open <http://127.0.0.1:8000>. The project uses Python 3.14, selected by `.python-version`.

## Build and check

```sh
uv run zensical build
uv run python -m unittest discover -s tests
```

The public binaries are built and placed by the release pipeline of the private repository. `releases/latest/` always serves the newest stable release. After publishing this site, copy `docs/install.sh` and `docs/install.ps1` to the downloads host by hand, because that host serves `/install.sh` and `/install.ps1` itself.

CI also checks the shell and PowerShell installers and provides a downloadable site preview. Deployment is manual.

Built with [Zensical](https://zensical.org). Fonts are self-hosted with their licenses in [docs/assets/fonts](docs/assets/fonts/).
