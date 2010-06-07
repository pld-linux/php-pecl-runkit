#
# Conditional build:
%bcond_without	tests		# build without tests

%define		modname	runkit
%define		status	beta
Summary:	%{modname} - mangle with user defined functions and classes
Summary(pl.UTF-8):	%{modname} - obróbka zdefiniowanych przez użytkownika funkcji i klas
Name:		php-pecl-%{modname}
Version:	0.9
Release:	5
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	855786f79a3803972b04e44c32cece8d
Patch0:		branch.diff
Patch1:		php52-api-warnings.patch
Patch2:		php53.patch
Patch3:		php53-zts.patch
Patch4:		php53-refcount.patch
Patch5:		php53-sapi_headers.patch
URL:		http://pecl.php.net/package/runkit/
BuildRequires:	php-devel >= 4:5.3.2-5
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Replace, rename, and remove user defined functions and classes. Define
customized superglobal variables for general purpose use. Execute code
in restricted environment (sandboxing).

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Zastępowanie, zmiana nazwy lub usuwanie zdefiniowanych przez
użytkownika funkcji i klas. Definiowanie zmiennych superglobalnych do
ogólnego użytku. Wykonywanie danego kodu w ograniczonym środowisku
(sandbox).

To rozszerzenie ma w PECL status: %{status}.

%description -l ru.UTF-8
Замещение, переименование и удаление оперделенных пользователем
функций и классов. Определение собственных суперглобальных переменных.
Выполнение кода в ограниченной среде (песочнице)

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch0 -p0
%patch1 -p1
%patch2 -p2
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
phpize
%configure
%{__make}

%if %{with tests}
cat <<'EOF' > run-tests.sh
#!/bin/sh
%{__make} test \
	RUN_TESTS_SETTINGS="-q $*"
EOF
chmod +x run-tests.sh
./run-tests.sh -w failed.log
test -f failed.log -a ! -s failed.log
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
