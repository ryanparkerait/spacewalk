%{!?perlgen:%define perlgen 5.8}
Summary: Set-Crontab Perl module
Name: perl-Set-Crontab
Version: 1.00
Release: 22{?dist}
License: GPL or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/Set-Crontab/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%if "%{perlgen}" == "5.8"
BuildRequires: perl >= 2:5.8.0
%else
BuildRequires: perl >= 1:5.6.0
%endif


Requires: %(perl -MConfig -le 'if (defined $Config{useithreads}) { print "perl(:WITH_ITHREADS)" } else { print "perl(:WITHOUT_ITHREADS)" }')
Requires: %(perl -MConfig -le 'if (defined $Config{usethreads}) { print "perl(:WITH_THREADS)" } else { print "perl(:WITHOUT_THREADS)" }')
Requires: %(perl -MConfig -le 'if (defined $Config{uselargefiles}) { print "perl(:WITH_LARGEFILES)" } else { print "perl(:WITHOUT_LARGEFILES)" }')
Source0: Set-Crontab-1.00.tar.gz

%description
%{summary}.

%prep
%setup -q -n Set-Crontab-%{version}

%build
%if "%{perlgen}" == "5.8"
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=$RPM_BUILD_ROOT%{_prefix} < /dev/null
%else
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL < /dev/null
%endif

make OPTIMIZE="$RPM_OPT_FLAGS"
make test

%install
rm -rf $RPM_BUILD_ROOT
eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT$installarchlib
%if "%{perlgen}" == "5.8"
make install
%else
make install PREFIX=$RPM_BUILD_ROOT%{_prefix}
%endif

rm -f `find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist`

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT%{_prefix} -type f -print | \
	sed "s@^$RPM_BUILD_ROOT@@g" > %{name}-%{version}-%{release}-filelist
if [ "$(cat %{name}-%{version}-%{release}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root,-)
%doc Changes README

%changelog
* Wed Aug 27 2008 Mike McCune 1.00-22
- Cleanup spec file to work in fedora and our new Makefile structure

* Wed Mar 19 2003 Chip Turner <cturner@redhat.com> - 1.00-1.8x
- Specfile autogenerated.

