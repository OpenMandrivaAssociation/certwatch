Name:       certwatch
Version:    1.0
Release:    %mkrel 9
Summary:    SSL certificate monitoring
Source0:    %{name}-%{version}.tar.gz
Patch0:     %{name}-1.0-mdv.patch
Group:      System/Servers
License:    GPL
BuildRequires:  openssl-devel
BuildRequires:  xmlto
Conflicts:      apache-mod_ssl <= 2.2.4-7mdv2008.0
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
The  certwatch  program  is used to issue warning when an SSL certificate is
about to expire.

%prep
%setup -q
%patch0 -p 1

%build 
cc %optflags -Wall -Werror -I/usr/include/openssl \
   certwatch.c -o certwatch -lcrypto

xmlto man certwatch.xml

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily \
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}%{_mandir}/man1 \
         %{buildroot}%{_bindir}

# install certwatch
install -c -m 755 certwatch %{buildroot}%{_bindir}/certwatch
install -c -m 755 certwatch.cron \
   %{buildroot}%{_sysconfdir}/cron.daily/certwatch
install -c -m 644 certwatch.1 \
   %{buildroot}%{_mandir}/man1/certwatch.1

cat > %{buildroot}%{_sysconfdir}/sysconfig/%{name} <<EOF
# certwatch cron task options
CERTS_DIR=/etc/pki/tls/certs
CERTWATCH_OPTS=
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/cron.daily/certwatch
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man1/*
