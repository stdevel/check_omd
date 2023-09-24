Name:           nagios-plugins-check_omd
Version:        1.3
Release:        0%{?dist}
Summary:        A Nagios / Icinga plugin for checking OMD sites.

Group:          Applications/System
License:        GPL
URL:            https://github.com/stdevel/check_omd
Source0:        nagios-plugins-check_omd-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:
Requires:       omd

%description
This package contains a Nagios / Icinga plugin for checking a OMD site's services.

Check out the GitHub page for further information: https://github.com/stdevel/check_omd

%prep
%setup -q

%build
#change /usr/lib64 to /usr/lib if we're on i686
%ifarch i686
sed -i -e "s/usr\/lib64/usr\/lib/" check_omd.cfg
%endif

%install
install -m 0755 -d %{buildroot}%{_libdir}/nagios/plugins/
install -m 0750 -d %{buildroot}%{_sysconfdir}/sudoers.d
install -m 0755 check_omd.py %{buildroot}%{_libdir}/nagios/plugins/check_omd.py
install -m 0440 check_omd-sudo-template %{_sysconfdir}/sudoers.d/check_omd-sudo-template
%if 0%{?el7}
        install -m 0755 -d %{buildroot}%{_sysconfdir}/nrpe.d/
        install -m 0755 check_omd.cfg  %{buildroot}%{_sysconfdir}/nrpe.d/check_omd.cfg
%else
        install -m 0755 -d %{buildroot}%{_sysconfdir}/nagios/plugins.d/
        install -m 0755 check_omd.cfg  %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_omd.cfg
%endif

%post
echo "NOTE: Don't forget to alter /etc/sudoers.d/check_omd-sudo-template to match your OMD installation"



%clean
rm -rf $RPM_BUILD_ROOT

%files
%if 0%{?el7}
        %config %{_sysconfdir}/nrpe.d/check_omd.cfg
%else
        %config %{_sysconfdir}/nagios/plugins.d/check_omd.cfg
%endif
%config %{_sysconfdir}/sudoers.d/check_omd-sudo-template
%{_libdir}/nagios/plugins/check_omd.py*


%changelog
* Sat Jul 16 2022 Christian Stankowic <info@cstan.io> - 1.3.0
- updates to upstream version 1.3.0

* Thu Apr 20 2021 Christian Stankowic <info@cstan.io> - 1.2.0
- updates to upstream version 1.2.0

* Thu May 31 2018 Christian Stankowic <info@cstan.io> - 1.1.1
- rebased to upstream version 1.1.1

* Mon Jun 27 2016 Christian Stankowic <info@stankowic-development.net> - 1.1.0
- updated to upstream version 1.1.0
- added -w / --warning option for excluding a service from generating critical states
- added hint when plugin executed as root

* Tue Jun 07 2016 Christian Stankowic <info@stankowic-development.net> - 1.0.1
- Initial release
