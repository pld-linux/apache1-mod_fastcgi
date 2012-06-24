%define		mod_name	fastcgi
%define 	apxs		/usr/sbin/apxs1
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	Obs�uga protoko�u FastCGI dla serwera apache
Summary(ru):	FastCGI - ����� ������� ������ CGI
Summary(uk):	FastCGI - ¦��� ������ ���Ӧ� CGI
Name:		apache1-mod_%{mod_name}
# NOTE: remember about apache-mod_fastcgi.spec when messing here
Version:	2.4.2
Release:	1.1
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e994414304b535cb99e10b7d1cad1d1e
Patch0:		%{name}-allow-uid-gid.patch
URL:		http://www.FastCGI.com/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	libtool
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This 3rd party module provides support for the FastCGI protocol.
FastCGI is a language independent, scalable, open extension to CGI
that provides high performance and persistence without the limitations
of server specific APIs.

%description -l pl
To jest modu� apache dodaj�cy obs�ug� protoko�u FastCGI. FastCGI jest
niezale�nym od j�zyka, skalowalnym, otwartym rozszerzeniem CGI daj�cym
du�� wydajno�� bez ograniczania API specyficznego dla serwera.

%description -l ru
FastCGI - ���������� CGI, ������� ������������� ����������� ���������
���������������������� Internet-���������� ��� �������������
������������ ������������� ��� ������� web-������� API.

�������� API web-�������� �� ����� �������������� CGI.

%description -l uk
FastCGI - ���������� CGI, ��� ����� �����צ��� ����������
���������������Φ Internet-�������� ��� ����Ȧ����Ԧ ������������
�����Ʀ���� ��� ������� web-������� API.

����˦��� API web-�����Ҧ� ڦ �Ӧ�� ���������� CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{apxs} -o mod_%{mod_name}.so -c *.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/apache start\" to start apache HTTP daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc docs/LICENSE.TERMS CHANGES docs/*.html
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
