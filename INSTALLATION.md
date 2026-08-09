# Installation

materialgram RPMs from this repository are published as **GitHub Release assets**, not through a Copr or any other `dnf` repository. Installation and updates are manual.

<!-- TODO: state the target Fedora release(s) and architecture the runner builds for -->

---

## Requirements

- Fedora (or an RHEL-compatible distribution) matching the `dist` tag of the RPM you download
- `dnf`
- The runtime dependencies are pulled automatically from your enabled repositories:
  - `hicolor-icon-theme`
  - `desktop-file-utils`
  - `shared-mime-info`

Check what your system is before downloading:

```bash
rpm --eval '%{dist} %{_arch}'
```

If that prints `.fc42 x86_64`, take the `*.fc42.x86_64.rpm` asset. Installing a package built for a different Fedora release generally works but is unsupported here — dependency versions may not line up.

---

## Install

### Via browser

1. Open the [Releases](../../releases) page.
2. Download the `materialgram-<version>-<release>.<dist>.<arch>.rpm` asset.
3. Install it:

```bash
sudo dnf install ./materialgram-*.rpm
```

### Via `curl`

```bash
VERSION=7.0.5.1
curl -LO "https://github.com/0n1cOn3/materialgram-rpm/releases/download/v${VERSION}/materialgram-${VERSION}-2.fc42.x86_64.rpm"
sudo dnf install ./materialgram-${VERSION}-2.fc42.x86_64.rpm
```

Adjust release, dist tag and arch to match the asset actually published.

### Via `gh`

```bash
gh release download --repo 0n1cOn3/materialgram-rpm --pattern '*.rpm'
sudo dnf install ./materialgram-*.rpm
```

---

## Signature verification

<!-- TODO: if releases are signed, document the public key and the rpm --checksig / --import steps here -->

The RPMs are currently unsigned. `dnf` will install them without a GPG check. If you did not build these yourself, verify the download against the checksum published with the release before installing.

---

## Updating

There is no repository metadata behind these releases, so `dnf update` will **not** find new versions. Watch this repository for releases, then install the new RPM over the old one:

```bash
sudo dnf install ./materialgram-<newversion>.rpm
```

`dnf install` on a higher version upgrades in place; the existing package is replaced, and user data under `~/.local/share/materialgram` is left untouched.

### Optional: turn the releases into a real repository

If you want `dnf update` to work, generate repository metadata over the RPMs and serve them (e.g. via GitHub Pages):

```bash
mkdir -p repo && cp materialgram-*.rpm repo/
createrepo_c repo/
```

```ini
# /etc/yum.repos.d/materialgram.repo
[materialgram]
name=materialgram (0n1cOn3)
baseurl=https://<your-pages-host>/materialgram-rpm/
enabled=1
gpgcheck=0
```

Set `gpgcheck=1` and point `gpgkey=` at your public key once the RPMs are signed.

---

## Downgrading

```bash
sudo dnf downgrade ./materialgram-<oldversion>.rpm
```

If `dnf` refuses because the older package is not in any repository, remove and reinstall — but read the removal warning below first, because removal deletes local application data.

---

## Removal

```bash
sudo dnf remove materialgram
```

**Warning:** the `%postun` scriptlet terminates any running `materialgram` process and deletes `~/.local/share/materialgram` on full removal. This wipes cache and session state — you will have to sign in again.

Back it up first if that matters:

```bash
cp -a ~/.local/share/materialgram ~/materialgram-data-backup
```

The scriptlet resolves the home directory via `${SUDO_USER:-$USER}`. Under `pkexec`, `doas`, non-`/home` home directories, or on multi-user systems it may target the wrong path — or none at all. Do not rely on it either way.

---

## Troubleshooting

**`Error: Problem: conflicting requests` / unresolved dependencies**
The RPM was likely built for a different Fedora release. Compare `rpm --eval '%{dist}'` with the dist tag in the filename.

**`Error: Package ... is already installed`**
Same version already present. Use `sudo dnf reinstall ./materialgram-*.rpm` if you want to force it.

**Desktop entry or icons missing after install**
The `%post` scriptlet refreshes the caches, but some sessions need a restart to pick them up. Force it manually:

```bash
sudo gtk-update-icon-cache /usr/share/icons/hicolor
sudo update-desktop-database
```

**Application will not start**
Run it from a terminal to see the error:

```bash
materialgram
```

Missing shared libraries mean the prebuilt upstream tarball expects a library version your system does not ship. Check with:

```bash
ldd /usr/bin/materialgram | grep 'not found'
```

That is an upstream packaging limitation, not something this spec can fix — the binary is repackaged, not rebuilt.
