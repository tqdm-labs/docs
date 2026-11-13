#!/usr/bin/env python3
"""Build customer-only artifacts from an exact private source tag. Never publishes."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

TARGETS = [(system, arch) for system in ('darwin', 'linux', 'windows')
           for arch in ('amd64', 'arm64')]


def run(*args, cwd=None, env=None):
    return subprocess.check_output(args, cwd=cwd, env=env, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'v\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?', args.version):
        parser.error('version must look like v0.4.8')
    source = args.source.resolve()
    output = args.output.resolve()
    if output == source or source in output.parents:
        parser.error('output must be outside the private source checkout')
    commit = run('git', 'rev-parse', '--verify', f'refs/tags/{args.version}^{{commit}}', cwd=source)
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        parser.error('output directory must be empty')
    with tempfile.TemporaryDirectory(prefix='tqctl-source-') as temp:
        checkout = Path(temp) / 'source'
        run('git', 'clone', '--quiet', '--no-hardlinks', '--no-checkout', str(source), str(checkout))
        run('git', 'checkout', '--quiet', '--detach', args.version, cwd=checkout)
        if run('git', 'rev-parse', 'HEAD', cwd=checkout) != commit:
            raise RuntimeError('checkout does not match requested release')
        for system, arch in TARGETS:
            suffix = '.exe' if system == 'windows' else ''
            name = f'tqctl_{args.version}_{system}_{arch}{suffix}'
            env = dict(os.environ, CGO_ENABLED='0', GOOS=system, GOARCH=arch, GOWORK='off')
            subprocess.run(['go', 'build', '-trimpath', '-o', str(output / name), './cmd/tqctl'],
                           cwd=checkout, env=env, check=True)
            metadata = run('go', 'version', '-m', str(output / name))
            for expected in (f'mod\tgithub.com/zAbuQasem/tqdm-labs\t{args.version}\t',
                             f'GOOS={system}', f'GOARCH={arch}', 'CGO_ENABLED=0',
                             f'vcs.revision={commit}', 'vcs.modified=false'):
                if expected not in metadata:
                    raise RuntimeError(f'{name}: missing build metadata {expected!r}')
            print(f'Built and inspected {name}', flush=True)
    sums = ""
    for path in sorted(output.glob("tqctl_*")):
        with path.open("rb") as binary:
            digest = hashlib.file_digest(binary, "sha256").hexdigest()
        sums += f"{digest}  {path.name}\n"
    (output / 'SHA256SUMS').write_text(sums)
    (output / 'release.json').write_text(json.dumps({
        'version': args.version, 'commit': commit,
        'targets': [f'{system}/{arch}' for system, arch in TARGETS],
    }, indent=2) + '\n')
    print(f'Release prepared in {output}. Nothing has been published.')


if __name__ == '__main__':
    main()
