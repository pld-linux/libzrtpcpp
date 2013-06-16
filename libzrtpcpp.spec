Summary:	GNU RTP stack for the zrtp protocol specification
Summary(pl.UTF-8):	Stos GNU RTP dla specyfikacji protokołu zrtp
Name:		libzrtpcpp
Version:	2.3.3
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/ccrtp/%{name}-%{version}.tar.gz
# Source0-md5:	3467e5fd361a8abcb9ea9c953870e13b
URL:		http://www.gnu.org/software/ccrtp/
BuildRequires:	cmake >= 2.6
BuildRequires:	ccrtp-devel >= 2.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Requires:	ccrtp >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library is a GPL licensed extension to the GNU RTP Stack, ccrtp,
that offers compatibility with Phil Zimmermann's zrtp/Zfone voice
encryption, and which can be directly embedded into telephony
applications.

%description -l pl.UTF-8
Ta biblioteka jest licencjonowanym na GPL rozszerzeniem stosu GNU RTP
- ccrtp - oferującym kompatybilność z szyfrowaniem głosu zrtp/Zfont
Phila Zimmermanna i mogącym być bezpośrednio włączone do aplikacji
telefonicznych.

%package devel
Summary:	Header files for libzrtpcpp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libzrtpcpp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ccrtp-devel >= 2.0.0
Requires:	openssl-devel >= 0.9.8
Requires:	libstdc++-devel
Obsoletes:	libzrtpcpp-static

%description devel
Header files for libzrtpcpp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzrtpcpp.

%prep
%setup -q

%{__sed} -i -e '/set(CMAKE_VERBOSE_MAKEFILE FALSE)/d' CMakeLists.txt

%build
%cmake .
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libzrtpcpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzrtpcpp.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzrtpcpp.so
%{_includedir}/libzrtpcpp
%{_pkgconfigdir}/libzrtpcpp.pc
