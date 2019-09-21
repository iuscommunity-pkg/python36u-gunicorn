%global upstream_name gunicorn
%global python python36

%bcond_with tests
%bcond_with docs

Name:           %{python}-%{upstream_name}
Version:        19.8.1
Release:        2%{?dist}
Summary:        Python WSGI application server
License:        MIT
URL:            http://gunicorn.org/
Source0:        https://files.pythonhosted.org/packages/source/g/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
# distro-specific, not upstreamable
Patch101:       0001-use-dev-log-for-syslog.patch
BuildArch:      noarch

BuildRequires:  %{python}-devel
BuildRequires:  %{python}-setuptools
%if %{with tests}
BuildRequires:  %{python}-pytest
BuildRequires:  %{python}-pytest-cov
BuildRequires:  %{python}-mock
%endif
%if %{with docs}
BuildRequires:  python%{?fedora:2}-sphinx
BuildRequires:  python%{?fedora:2}-sphinx_rtd_theme
%endif
Requires:       %{python}-setuptools

# Rename from python36u-gunicorn
Provides: python36u-gunicorn = %{version}-%{release}
Obsoletes: python36u-gunicorn < 19.8.1-2


%description
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It uses the
pre-fork worker model, ported from Ruby's Unicorn project. It supports WSGI and
Paster applications.


%if %{with docs}
%package doc
Summary:        Documentation for the %{name} package


%description doc
Documentation for the %{name} package.
%endif


%prep
%setup -q -n %{upstream_name}-%{version}
%patch101 -p1


%build
%py36_build
%{?with_docs:%{__python2} setup.py build_sphinx}


%install
%py36_install
# rename executables in /usr/bin so they don't collide
for executable in %{upstream_name} %{upstream_name}_paster ; do
    mv %{buildroot}%{_bindir}/$executable %{buildroot}%{_bindir}/$executable-%{python36_version}
done


%if %{with tests}
%check
%{__python36} setup.py test
%endif


%files
%license LICENSE
%doc NOTICE README.rst THANKS
%{python36_sitelib}/%{upstream_name}*
%{_bindir}/%{upstream_name}-%{python36_version}
%{_bindir}/%{upstream_name}_paster-%{python36_version}


%if %{with docs}
%files doc
%license LICENSE
%doc build/sphinx/html/*
%endif


%changelog
* Sat Sep 21 2019 Carl George <carl@george.computer> - 19.8.1-2
- Rename to python36-setuptools

* Fri May 04 2018 Carl George <carl@george.computer> - 19.8.1-1.ius
- Latest upstream

* Tue Apr 04 2017 Carl George <carl.george@rackspace.com> - 19.7.1-1.ius
- Port from Fedora to IUS
- Conditionalize tests
- Conditionalize docs

* Wed Mar 29 2017 Dan Callaghan <dcallagh@redhat.com> - 19.7.1-1
- upstream release 19.7.1: http://docs.gunicorn.org/en/19.7.1/news.html

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 19.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 19.6.0-3
- Rebuild for Python 3.6

* Mon Aug 15 2016 Dan Callaghan <dcallagh@redhat.com> - 19.6.0-2
- updated to latest Python guidelines

* Mon Aug 15 2016 Dan Callaghan <dcallagh@redhat.com> - 19.6.0-1
- upstream release 19.6.0: http://docs.gunicorn.org/en/19.6.0/news.html

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19.4.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 19.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Dan Callaghan <dcallagh@redhat.com> - 19.4.1-1
- upstream release 19.4.1: http://docs.gunicorn.org/en/19.4.1/news.html

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 05 2015 Dan Callaghan <dcallagh@redhat.com> - 19.3.0-3
- handle expected HaltServer exception in manage_workers (RHBZ#1200041)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 09 2015 Dan Callaghan <dcallagh@redhat.com> - 19.3.0-1
- upstream release 19.3.0: http://docs.gunicorn.org/en/19.3.0/news.html

* Tue Aug 19 2014 Dan Callaghan <dcallagh@redhat.com> - 19.1.1-2
- fixed build requirements, added -doc subpackage with HTML docs

* Tue Aug 19 2014 Dan Callaghan <dcallagh@redhat.com> - 19.1.1-1
- upstream release 19.1.1: http://docs.gunicorn.org/en/19.1.1/news.html

* Mon Jun 23 2014 Dan Callaghan <dcallagh@redhat.com> - 19.0.0-1
- upstream release 19.0: http://docs.gunicorn.org/en/19.0/news.html

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Sep 06 2013 Dan Callaghan <dcallagh@redhat.com> - 18.0-1
- upstream release 18.0: http://docs.gunicorn.org/en/latest/news.html

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Dan Callaghan <dcallagh@redhat.com> - 17.5-1
- upstream release 17.5: 
  http://docs.gunicorn.org/en/R17.5/2013-news.html#r17-5-2013-07-03 
  (version numbering scheme has changed to drop the initial 0)

* Tue Apr 30 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.4-1
- upstream release 0.17.4: http://docs.gunicorn.org/en/0.17.4/news.html

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.2-1
- upstream bug fix release 0.17.2

* Wed Jan 02 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.0-2
- patch to use /dev/log for syslog by default

* Wed Jan 02 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.0-1
- new upstream release 0.17.0

* Mon Nov 26 2012 Dan Callaghan <dcallagh@redhat.com> - 0.16.1-2
- fix test suite error with py.test on Python 3.3

* Mon Nov 26 2012 Dan Callaghan <dcallagh@redhat.com> - 0.16.1-1
- new upstream release 0.16.1 (with Python 3 support)

* Mon Oct 22 2012 Dan Callaghan <dcallagh@redhat.com> - 0.15.0-1
- new upstream release 0.15.0

* Mon Aug 20 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.6-2
- fix for LimitRequestLine test failure (upstream issue #390)

* Wed Aug 01 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.6-1
- upstream bugfix release 0.14.6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.5-1
- upstream bugfix release 0.14.5

* Thu Jun 07 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.3-1
- updated to upstream release 0.14.3

* Wed Feb 08 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-3
- renamed package to python-gunicorn, and other minor fixes

* Tue Jan 31 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-2
- patch for failing test (gunicorn issue #294)

* Mon Jan 30 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-1
- initial version
