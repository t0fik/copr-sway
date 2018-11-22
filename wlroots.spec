%global commit  0.1
%global gitdate %{nil}
%global gitrel  %{nil}
%global gitver  %{nil}
# Keep the below around for possible snapshot times (was a must prior to 0.1)
#global scommit #(c=#{commit}; echo ${c:0:7})
#global gitrel  .#{gitdate}git#{scommit}
#global gitver  -#{gitdate}git#{scommit}


%global api_ver 0


Name:           wlroots
Version:        0.1
Release:        2.1%{?gitrel}%{?dist}
Summary:        A modular Wayland compositor library

# All files in the sources are licensed as MIT, but
# - LGPL (v2.1 or later)
#   * protocol/idle.xml
#   * protocol/server-decoration.xml
# - NTP (legal disclaimer)
#   * protocol/gamma-control.xml
#   * protocol/text-input-unstable-v3.xml
#   * protocol/wlr-gamma-control-unstable-v1.xml
#   * protocol/wlr-input-inhibitor-unstable-v1.xml
#   * protocol/wlr-layer-shell-unstable-v1.xml

#
# Those files are processed to c-compilable files by the
# `wayland-scanner` binary during build and don't alter the
# main license of the binaries linking with them by the
# underlying licenses.
License:        MIT
URL:            https://github.com/swaywm/%{name}
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}%{?gitver}.tar.gz
Patch0:         %{url}/commit/be6210cf8216c08a91e085dac0ec11d0e34fb217.patch#/pkgconfig_version.patch

BuildRequires:  gcc
BuildRequires:  libcap-devel
BuildRequires:  libinput-devel
BuildRequires:  libpng
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  meson
BuildRequires:  pixman-devel
BuildRequires:  systemd-devel
BuildRequires:  wayland-devel >= 1.16
BuildRequires:  wayland-protocols-devel >= 1.15
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-wm-devel
# patch application
BuildRequires:  git

Requires: libwayland-client >= 1.16
Requires: libwayland-server >= 1.16
Requires: libwayland-egl >= 1.16


%description
%{summary}.


%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} == %{version}-%{release}
Requires:       libinput-devel%{?_isa}
Requires:       libxcb-devel%{?_isa}
Requires:       libxkbcommon-devel%{?_isa}
Requires:       mesa-libEGL-devel%{?_isa}
Requires:       pixman-devel%{?_isa}
Requires:       systemd-devel%{?_isa}
Requires:       wayland-devel%{?_isa} >= 1.16
Requires:       xcb-util-wm-devel%{?_isa}

%description    devel
Development files for %{name}.


%prep
%define __scm git_am
%autosetup -n %{name}-%{commit} -p 1


%build

# Needed since xcb-errors is not packaged (yet?)
%global __meson_auto_features auto

%ifarch %{arm} %{ix86}
export CFLAGS="%{optflags} -Wno-error=format="
export CXXFLAGS="%{optflags} -Wno-error=format="
%endif
%meson
%meson_build


%install
%meson_install

# %%doc && examples.
%{__mkdir} -p %{buildroot}%{_pkgdocdir}
%{__cp} -pr README.md examples %{buildroot}%{_pkgdocdir}

# Cleanup.
for f in '.*ignore*' meson.build; do
  %{_bindir}/find %{buildroot} -type f -name "$f" -print -delete
done


%check
%meson_test


# Needed only for < F28
%ldconfig_scriptlets


%files
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%license LICENSE
%{_libdir}/lib%{name}.so.%{api_ver}*


%files          devel
%doc %{_pkgdocdir}/examples
%{_includedir}/wlr
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Nov 22 2018 Jerzy Drozdz <rpmbuilder@jdsieci.pl> - 0.1-2.1
- Added dependecies for Fedora28

* Wed Nov 07 2018 Jan Pokorny <jpokorny+rpm-grim@fedoraproject.org> - 0.1-2
- Fix incorrect "pkgconfig" version

* Wed Oct 31 2018 Jan Pokorny <jpokorny+rpm-grim@fedoraproject.org> - 0.1-1
- Updated to historically first official release
- Turned off implicit enablement of all 'auto' build features under Meson,
  since xcb-errors is not available at this time
- Added BR: libpng
- Expanding spec comment on source files not covered with MIT license

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-0.9.20180106git03faf17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-0.8.20180106git03faf17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 13 2018 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.7.20180106git03faf17
- Updated snapshot

* Wed Jan 03 2018 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.6.20180102git767df15
- Initial import (#1529352)

* Wed Jan 03 2018 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.5.20180102git767df15
- Updated snapshot

* Sun Dec 31 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.4.20171229git80ed4d4
- Add licensing clarification
- Add BR: gcc

* Sat Dec 30 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.3.20171229git80ed4d4
- Updated snapshot

* Wed Dec 27 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.2.20171227giteeb7cd8
- Optimize spec-file

* Wed Dec 27 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.1.20171227giteeb7cd8
- Initial rpm release (#1529352)
