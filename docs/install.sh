#!/bin/sh
set -eu

fail() { printf 'tqctl: %s\n' "$*" >&2; exit 1; }
version=''
install_dir=${HOME:?HOME must be set}/.local/bin
while [ "$#" -gt 0 ]; do
    case "$1" in
        --version|--install-dir)
            [ "$#" -ge 2 ] || fail "missing value for $1"
            case "$1" in --version) version=$2;; --install-dir) install_dir=$2;; esac
            shift 2;;
        --help|-h)
            printf 'Usage: sh install.sh [--version vX.Y.Z] [--install-dir PATH]\n'
            exit 0;;
        *) fail "unknown option: $1";;
    esac
done
case "$install_dir" in /*) ;; *) fail 'installation directory must be an absolute path';; esac
case "$(uname -s)" in
    Darwin) os=darwin;;
    Linux) os=linux;;
    *) fail 'unsupported OS; use install.ps1 on Windows, or run this script inside WSL';;
esac
case "$(uname -m)" in
    x86_64|amd64) arch=amd64;;
    arm64|aarch64) arch=arm64;;
    *) fail 'unsupported CPU; supported architectures are x86-64 and ARM64';;
esac
command -v curl >/dev/null 2>&1 || fail 'curl is required'
if command -v sha256sum >/dev/null 2>&1; then
    hash_tool=sha256sum
elif command -v shasum >/dev/null 2>&1; then
    hash_tool=shasum
else
    fail 'sha256sum or shasum is required'
fi
base=https://docs.tqdm.sh
if [ -z "$version" ]; then
    version=$(curl --proto '=https' --proto-redir '=https' --tlsv1.2 -fsSL \
        --connect-timeout 15 --max-time 120 "$base/releases/latest.txt")
fi
case "$version" in ''|*[!0-9A-Za-z.-]*) fail 'version must look like v0.4.8';; esac
printf '%s\n' "$version" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z]+([.-][0-9A-Za-z]+)*)?$' \
    || fail 'version must look like v0.4.8'
asset=tqctl_${version}_${os}_${arch}
url=$base/releases/$version
mkdir -p "$install_dir"
destination=$install_dir/tqctl
[ ! -L "$destination" ] || fail 'destination is a symlink; choose another installation directory'
[ ! -e "$destination" ] || [ -f "$destination" ] || fail 'destination is not a regular file'
work=$(mktemp -d "$install_dir/.tqctl-install.XXXXXXXX")
trap 'rm -rf "$work"' EXIT
trap 'exit 1' HUP INT TERM
printf 'Downloading tqctl %s for %s/%s…\n' "$version" "$os" "$arch"
for file in "$asset" SHA256SUMS; do
    curl --proto '=https' --proto-redir '=https' --tlsv1.2 -fsSL \
        --connect-timeout 15 --max-time 300 "$url/$file" -o "$work/$file"
done
expected=$(awk -v name="$asset" '
    $2 == name { count++; digest=$1; if (NF != 2 || length($1) != 64 || $1 ~ /[^0-9a-fA-F]/) bad=1 }
    END { if (count != 1 || bad) exit 1; print tolower(digest) }
' "$work/SHA256SUMS") || fail 'checksum manifest must contain exactly one valid entry for this binary'
if [ "$hash_tool" = sha256sum ]; then
    actual=$(sha256sum "$work/$asset" | cut -d ' ' -f 1)
else
    actual=$(shasum -a 256 "$work/$asset" | cut -d ' ' -f 1)
fi
[ "$actual" = "$expected" ] || fail 'SHA-256 mismatch; the existing installation has not been changed'
chmod 755 "$work/$asset"
[ ! -L "$destination" ] || fail 'destination became a symlink; installation stopped'
[ ! -e "$destination" ] || [ -f "$destination" ] || fail 'destination is not a regular file'
mv -f "$work/$asset" "$destination"
printf 'Installed %s\nEnsure this directory is on your PATH: %s\nThen run: tqctl --version\n' "$destination" "$install_dir"
