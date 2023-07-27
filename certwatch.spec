Summary:	SSL certificate monitoring
Name:		certwatch
Version:	1.2
Release:	1
License:	GPLv2+
Group:		System/Servers
Source0:	https://github.com/notroj/certwatch/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
BuildRequires:	pkgconfig(openssl)

%description
The certwatch  program  is used to issue warning when an SSL certificate is
about to expire.

%files
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/cron.daily/certwatch
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%{__cc} %{optflags} -Wall -I/usr/include/openssl \
	certwatch.c -o certwatch -lcrypto

xmlto man certwatch.xml

%install
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

