import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / 'tools'
        self.bin.mkdir()
        self.dest = self.root / 'install with spaces'
        self.fixture = self.root / 'fixture'
        self.fixture.mkdir()
        self.env = dict(os.environ, PATH=f'{self.bin}:{os.environ["PATH"]}',
                        HOME=str(self.root), FIXTURE=str(self.fixture),
                        TEST_OS='Linux', TEST_ARCH='x86_64')
        self.tool('uname', '#!/bin/sh\ncase "$1" in -s) echo "$TEST_OS";; -m) echo "$TEST_ARCH";; esac\n')
        self.tool('curl', '''#!/bin/sh
printf '%s\\n' "$*" >> "$FIXTURE/requests"
[ "${DOWNLOAD_FAIL:-0}" = 0 ] || exit 22
out=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    -o) out=$2; shift 2;;
    https://*) url=$1; shift;;
    *) shift;;
  esac
done
case "$url" in
  https://docs.tqdm.sh/releases/latest.txt) cat "$FIXTURE/latest.txt";;
  https://docs.tqdm.sh/releases/v0.4.8/SHA256SUMS) cp "$FIXTURE/SHA256SUMS" "$out";;
  https://docs.tqdm.sh/releases/v0.4.8/tqctl_*) cp "$FIXTURE/payload" "$out";;
  *) exit 22;;
esac
''')
        self.payload = b'#!/bin/sh\necho installed\n'
        (self.fixture / 'payload').write_bytes(self.payload)
        self.manifest()
        (self.fixture / 'latest.txt').write_text('v0.4.8\n')

    def tool(self, name, content):
        path = self.bin / name
        path.write_text(content)
        path.chmod(0o755)

    def manifest(self, name='tqctl_v0.4.8_linux_amd64', digest=None):
        digest = digest or hashlib.sha256(self.payload).hexdigest()
        (self.fixture / 'SHA256SUMS').write_text(f'{digest}  {name}\n')

    def run_install(self, *args):
        return subprocess.run(['sh', str(ROOT / 'docs/install.sh'),
                               '--install-dir', str(self.dest), *args],
                              env=self.env, text=True, capture_output=True)

    def test_platform_matrix(self):
        for system, arch, target in [('Linux', 'x86_64', 'linux_amd64'),
                                      ('Linux', 'aarch64', 'linux_arm64'),
                                      ('Darwin', 'x86_64', 'darwin_amd64'),
                                      ('Darwin', 'arm64', 'darwin_arm64')]:
            with self.subTest(system=system, arch=arch):
                self.env.update(TEST_OS=system, TEST_ARCH=arch)
                self.manifest(f'tqctl_v0.4.8_{target}')
                result = self.run_install()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((self.dest / 'tqctl').read_bytes(), self.payload)
                self.assertTrue((self.dest / 'tqctl').stat().st_mode & 0o111)

    def test_final_message_points_at_shell_setup(self):
        result = self.run_install()
        self.assertEqual(result.stdout.splitlines()[-2:], [
            f'Installed {self.dest}/tqctl',
            'Set up your shell (PATH and tab completion): https://docs.tqdm.sh/installation/#set-up-your-shell'])

    def test_invalid_latest_preserves_binary(self):
        self.dest.mkdir()
        (self.dest / 'tqctl').write_bytes(b'old')
        for latest in ['', '<html>unavailable</html>', '../bad', 'v0.4.8\nv0.4.9', 'v0.4.8\n../bad']:
            with self.subTest(latest=latest):
                (self.fixture / 'latest.txt').write_text(latest)
                (self.fixture / 'requests').unlink(missing_ok=True)
                self.assertNotEqual(self.run_install().returncode, 0)
                self.assertEqual((self.dest / 'tqctl').read_bytes(), b'old')
                self.assertEqual(len((self.fixture / 'requests').read_text().splitlines()), 1)

    def test_pinned_version_skips_latest(self):
        (self.fixture / 'latest.txt').unlink()
        result = self.run_install('--version', 'v0.4.8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('/latest.txt', (self.fixture / 'requests').read_text())

    def test_bad_manifests_preserve_old_binary(self):
        self.dest.mkdir()
        installed = self.dest / 'tqctl'
        installed.write_bytes(b'old')
        valid = (self.fixture / 'SHA256SUMS').read_text()
        for contents in ['0' * 64 + '  tqctl_v0.4.8_linux_amd64\n',
                         valid + valid, valid.replace('linux_amd64', 'linux_arm64'),
                         'invalid  tqctl_v0.4.8_linux_amd64\n']:
            with self.subTest(contents=contents):
                (self.fixture / 'SHA256SUMS').write_text(contents)
                result = self.run_install('--version', 'v0.4.8')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(installed.read_bytes(), b'old')

    def test_unsupported_platform_and_bad_version_do_not_download(self):
        for env, args in [({'TEST_OS': 'FreeBSD'}, []),
                          ({'TEST_ARCH': 'riscv64'}, []),
                          ({}, ['--version', '../bad']),
                          ({}, ['--version', 'v1.2.3;id']),
                          ({}, ['--version', 'v0.4.8\n../bad']),
                          ({}, ['--version'])]:
            with self.subTest(env=env, args=args):
                self.env.update(TEST_OS='Linux', TEST_ARCH='x86_64')
                self.env.update(env)
                result = self.run_install(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.fixture / 'requests').exists())

    def test_download_failure_preserves_binary(self):
        self.dest.mkdir()
        (self.dest / 'tqctl').write_bytes(b'old')
        self.env['DOWNLOAD_FAIL'] = '1'
        self.assertNotEqual(self.run_install().returncode, 0)
        self.assertEqual((self.dest / 'tqctl').read_bytes(), b'old')

    def test_symlink_is_rejected(self):
        self.dest.mkdir()
        target = self.root / 'untouched'
        target.write_bytes(b'old')
        (self.dest / 'tqctl').symlink_to(target)
        self.assertNotEqual(self.run_install().returncode, 0)
        self.assertEqual(target.read_bytes(), b'old')

    def test_directory_destination_is_rejected(self):
        (self.dest / 'tqctl').mkdir(parents=True)
        self.assertNotEqual(self.run_install().returncode, 0)
        self.assertEqual(list((self.dest / 'tqctl').iterdir()), [])


if __name__ == '__main__':
    unittest.main()
