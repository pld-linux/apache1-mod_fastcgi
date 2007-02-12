%define		mod_name	fastcgi
%define 	apxs		/usr/sbin/apxs1
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl.UTF-8):	Obsługa protokołu FastCGI dla serwera apache
Summary(ru.UTF-8):	FastCGI - более быстрая версия CGI
Summary(uk.UTF-8):	FastCGI - більш швидка версія CGI
Name:		apache1-mod_%{mod_name}
# NOTE: remember about apache-mod_fastcgi.spec when messing here
Version:	2.4.2
Release:	4
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e994414304b535cb99e10b7d1cad1d1e
Patch0:		%{name}-allow-uid-gid.patch
Patch1:		%{name}-socketdir.patch
URL:		http://www.FastCGI.com/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)
%define		_socketdir	/var/run/apache/fastcgi

%description
This 3rd party module provides support for the FastCGI protocol.
FastCGI is a language independent, scalable, open extension to CGI
that provides high performance and persistence without the limitations
of server specific APIs.

%description -l pl.UTF-8
To jest moduł apache dodający obsługę protokołu FastCGI. FastCGI jest
niezależnym od języka, skalowalnym, otwartym rozszerzeniem CGI dającym
dużą wydajność bez ograniczania API specyficznego dla serwera.

%description -l ru.UTF-8
FastCGI - расширение CGI, которое предоставляет возможность создавать
высокопроизводительные Internet-приложения без необходимости
использовать специфические для каждого web-сервера API.

Скорость API web-серверов со всеми преимуществами CGI.

%description -l uk.UTF-8
FastCGI - розширення CGI, яке надає можливість створювати
високопродуктивні Internet-програми без необхідності використання
специфічних для кожного web-серверу API.

Швидкість API web-серверів зі всіма перевагами CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{apxs} -S CC="%{__cc}" -o mod_%{mod_name}.so -c *.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d,%{_socketdir}/dynamic}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc docs/LICENSE.TERMS CHANGES docs/*.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%dir %attr(770,root,http) %{_socketdir}
%dir %attr(770,root,http) %{_socketdir}/dynamic
