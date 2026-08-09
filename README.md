# materialgram-rpm

RPM packaging for [materialgram](https://github.com/kukuruzka165/materialgram) — a Telegram Desktop fork with Material Design icons and UI improvements.

This fork builds the package on a **self-hosted runner** and publishes the resulting RPM to **GitHub Releases**. It is a fork of [burhancodes/materialgram-rpm](https://github.com/burhancodes/materialgram-rpm).

---

## Why this fork exists

The upstream repository publishes to the Copr project [`burhanverse/materialgram`](https://copr.fedorainfracloud.org/coprs/burhanverse/materialgram/). When its build pipeline broke, updated packages stopped arriving. This fork exists to keep a current materialgram RPM available independently of that pipeline — built here, released here.

It is **not** a Copr repository. There is no `dnf copr enable` step, and no automatic update path. See [INSTALLATION.md](INSTALLATION.md).

---

## What this is (and is not)

This is a **repackaging** spec, not a from-source build. `%prep` unpacks the prebuilt `materialgram-vX.Y.Z.tar.zst` release tarball published by upstream, `%install` relocates its contents into the buildroot, and `%build` is intentionally empty. No compilation happens here.

If you need a from-source build — for reproducibility, hardening flags, or a non-x86_64 arch — this spec is not the right starting point.

| | |
|---|---|
| Package | `materialgram` |
| Current version | `7.0.5.1` |
| License | GPLv3 |
| Upstream | <https://github.com/kukuruzka165/materialgram> |
| Source | `materialgram-v%{version}.tar.zst` (upstream release asset) |
| Distribution | GitHub Releases (this repository) |

---

## Installation

Download the RPM from the [Releases](../../releases) page and install it:

```bash
sudo dnf install ./materialgram-*.rpm
```

Full instructions — dist/arch matching, updating, downgrading, removal caveats and troubleshooting — are in **[INSTALLATION.md](INSTALLATION.md)**.

---

## Building locally

```bash
sudo dnf install rpm-build rpmdevtools tar sed
rpmdev-setuptree

VERSION=7.0.5.1
curl -L -o ~/rpmbuild/SOURCES/materialgram-v${VERSION}.tar.zst \
  "https://github.com/kukuruzka165/materialgram/releases/download/v${VERSION}/materialgram-v${VERSION}.tar.zst"

rpmbuild -ba materialgram.spec
```

The resulting RPM lands in `~/rpmbuild/RPMS/x86_64/`.

> `%prep` extracts into `%{_sourcedir}` rather than `%{_builddir}`. Repeated local builds leave artifacts in your SOURCES tree — clean it between runs when switching versions.

---

## Package contents

| Path | Purpose |
|---|---|
| `/usr/bin/materialgram` | Application binary |
| `/usr/share/applications/` | Desktop entry |
| `/usr/share/dbus-1/` | D-Bus service definition |
| `/usr/share/icons/` | hicolor icon theme assets |
| `/usr/share/metainfo/` | AppStream metadata |

**Runtime requires:** `hicolor-icon-theme`, `desktop-file-utils`, `shared-mime-info`
**Build requires:** `tar`, `sed`

---

## Scriptlet behaviour

Worth reading before installing this on a machine you care about:

- `%post` / `%posttrans` — refresh the hicolor icon cache and the desktop database.
- `%postun` — the same, plus **on full removal only** (`$1 -eq 0`): terminates any running `materialgram` process and deletes `~/.local/share/materialgram`.

That last step is destructive: uninstalling removes local application data (cache, session state) for the invoking user. The home directory is resolved via `${SUDO_USER:-$USER}`, so under `pkexec`, `doas`, non-`/home` home directories, or on multi-user systems, the wrong path may be targeted — or none at all. Back up `~/.local/share/materialgram` before removing the package if that data matters.

---

## Release pipeline

Builds run on a self-hosted runner; workflow definitions live in `.github/workflows/`. The produced RPM is attached to a GitHub Release in this repository.

<!-- TODO: document workflow file name, trigger (tag push / manual dispatch), runner label, and target Fedora release / arch -->

### Cutting a new version

1. Bump `Version:` in `materialgram.spec` and reset `Release:` to `1%{?dist}`.
2. Add a `%changelog` entry — date, packager, `version-release`, one line describing the change.
3. Confirm the upstream release actually ships a `materialgram-vX.Y.Z.tar.zst` asset.
4. Lint: `rpmlint materialgram.spec`.
5. Commit, push, and trigger the workflow.

Keep `Release:` and the top `%changelog` entry consistent — a mismatch makes the RPM's own changelog lie about which build it belongs to.

---

## Credits

- **materialgram** — [kukuruzka165](https://github.com/kukuruzka165)
- **Original spec and packaging** — Burhanverse ([burhancodes](https://github.com/burhancodes))
- **This fork** — [0n1cOn3](https://github.com/0n1cOn3)

## License

The packaging in this repository follows the license of the packaged software: **GPLv3**.

Materialgram is an unofficial Telegram client, not affiliated with or endorsed by Telegram FZ-LLC.
