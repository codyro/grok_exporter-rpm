%global debug_package %{nil}

Name:           grok_exporter
Version:        1.0.0.RC5
Release:        1%{?dist}
Summary:        A simple hierarchical database supporting plugin data sources

License:        Apache-2.0
URL:            https://github.com/fstab/%{name}

Source0:        https://github.com/fstab/%{name}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.service
Source2:        config.yml

BuildRequires:  git
BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

Provides:       %{name} = %{version}

%description
Export Prometheus metrics from arbitrary unstructured log data.

%prep
%autosetup

%build
make

%pre
useradd \
       --system --user-group --shell /sbin/nologin \
       --home-dir /var/lib/%{name} \
       --comment "Prometheus Grok Exporter" %{name}
exit 0

%install
install -Dpm 0755 %{name}-%{version} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 config.yml %{buildroot}%{_sysconfdir}/%{name}config.yml
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
go test -v ./...

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/usr/sbin/userdel %{name}

%files
# Binary
%{_bindir}/%{name}

# Configuration
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.yml

# systemD
%{_unitdir}/%{name}.service

%license LICENSE


%changelog
* Tue Nov 07 2023 Cody Robertson <cody@nerdymuffin.com> - 1.0.0.RC5-1
- Initial build
