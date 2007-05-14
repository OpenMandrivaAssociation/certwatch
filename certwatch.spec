Name:       certwatch
Version:    1.0
Release:    %mkrel 1
Summary:    SSL certificate monitoring
Source0:    %{name}-%{version}.tar.gz
Patch0:     %{name}-1.0-mdv.patch
Group:      Applications/System
License:    GPL
BuildRequires:  openssl-devel
BuildRequires:  xmlto
Conflicts:      apache-mod_ssl <= 2.2.4-7mdv2008.0
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
The  certwatch  program  is used to issue warning when an SSL certificate is
about to expire.

This is a redhat utility, modified to be output-agnostic.

%prep
%setup -q -c
%patch

%build 
cc $RPM_OPT_FLAGS -Wall -Werror -I/usr/include/openssl \
   $RPM_SOURCE_DIR/certwatch.c -o certwatch -lcrypto

xmlto man $RPM_SOURCE_DIR/certwatch.xml

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily \
         %{buildroot}%{_mandir}/man1 \
         %{buildroot}%{_bindir}

# install certwatch
install -c -m 755 certwatch %{buildroot}%{_bindir}/certwatch
install -c -m 755 $RPM_SOURCE_DIR/certwatch.cron \
   %{buildroot}%{_sysconfdir}/cron.daily/certwatch
install -c -m 644 certwatch.1 \
   %{buildroot}%{_mandir}/man1/certwatch.1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sysconfdir}/cron.daily/certwatch
%{_mandir}/man1/*

