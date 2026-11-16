# Repackaged upstream binary: no debuginfo, don't strip
%global debug_package %{nil}
%global __strip /bin/true
%global appid io.github.kukuruzka165.materialgram

Name:           materialgram
Version:        7.3.1.1
Release:        1%{?dist}
Summary:        Telegram Desktop fork with material icons and some improvements
License:        GPL-3.0-only
URL:            https://github.com/kukuruzka165/materialgram
Source0:        %{url}/releases/download/v%{version}/%{name}-v%{version}.tar.zst

ExclusiveArch:  x86_64

BuildRequires:  zstd
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme

%description
Telegram Desktop fork with Material Design and other improvements,
based on the Telegram API and the MTProto secure protocol.

%prep
%setup -q -c -n %{name}-v%{version}

%build
# prebuilt upstream binary, nothing to build

%install
install -Dpm 0755 usr/bin/%{name} %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_datadir}
cp -a usr/share/applications usr/share/dbus-1 usr/share/icons usr/share/metainfo \
      %{buildroot}%{_datadir}/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/icons/hicolor/*/apps/%{appid}*
%{_datadir}/metainfo/%{appid}.metainfo.xml

%changelog
* Mon Nov 16 2026 0n1cOn3 <0n1cOn3@gmx.ch> - 7.3.1.1-1
- Updated to version 7.3.1.1
- Switch Source0 to upstream .tar.zst
- Fix deps being swallowed by %%description, drop obsolete scriptlets
- Remove %%postun that killed processes and deleted user data
* Sat Oct 17 2026 Burhanverse <contact@burhanverse.eu.org> - 7.0.5.1-1
- Updated to version 7.0.5.1
* Sat Jul 25 2026 Burhanverse <contact@burhanverse.eu.org> - 6.7.7.1-1
- Updated to version 6.7.7.1
* Sun Jan 04 2026 Burhanverse <contact@burhanverse.eu.org> - 6.4.0.1-1
- Updated to version 6.4.0.1
* Mon Dec 29 2025 Burhanverse <contact@burhanverse.eu.org> - 6.3.10.1-1
- Updated to version 6.3.10.1
* Sun Oct 12 2025 Burhanverse <contact@burhanverse.eu.org> - 6.2.3.1-1
- Updated to version 6.2.3.1
* Sat Oct 11 2025 Burhanverse <contact@burhanverse.eu.org> - 6.2.2.1-1
- Updated to version 6.2.2.1
* Sun Aug 31 2025 Burhanverse <contact@burhanverse.eu.org> - 6.1.0.1-1
- Updated to version 6.1.0.1
* Thu Jul 31 2025 Burhanverse <contact@burhanverse.eu.org> - 6.0.0.1-1
- Updated to version 6.0.0.1
* Fri Jul 25 2025 Burhanverse <contact@burhanverse.eu.org> - 5.16.6.1-1
- Updated to version 5.16.6.1
* Tue Jul 15 2025 Burhanverse <contact@burhanverse.eu.org> - 5.16.4.1-2
- Updated to version 5.16.4.1
