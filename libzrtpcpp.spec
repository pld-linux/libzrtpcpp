#
# Conditional build:
%bcond_without	ccrtp		# CCRTP client library
%bcond_with	tivi		# Tivi client library (for reference)
%bcond_with	java		# Java code for Tivi client library (test only)
%bcond_with	openssl		# OpenSSL based cryptography (instead of standalone) for ccrtp
%bcond_with	sqlite		# use SQLite (3.x) for cache [always enabled for tivi]
#
Summary:	GNU RTP stack for the zrtp protocol specification
Summary(pl.UTF-8):	Stos GNU RTP dla specyfikacji protokołu zrtp
Name:		libzrtpcpp
Version:	4.7.0
Release:	1
License:	Apache v2.0 (core), GPL v3+ (CCRTP client), for reference (Tivi client)
Group:		Libraries
#Source0Download: https://github.com/wernerd/ZRTPCPP/tags
Source0:	https://github.com/wernerd/ZRTPCPP/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	24bcaa5ee64083e9da76ee3cb68c90a3
Patch0:		%{name}-java.patch
Patch1:		%{name}-includes.patch
URL:		http://www.gnutelephony.org/index.php/GNU_ZRTP
BuildRequires:	cmake >= 3.0
%{?with_ccrtp:BuildRequires:	ccrtp-devel >= 2.0.0}
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.8}
BuildRequires:	pkgconfig
%if %{with sqlite} || %{with tivi}
BuildRequires:	sqlite3-devel >= 3.7
%endif
%{?with_java:BuildRequires:	swig}
Requires:	ccrtp >= 2.0.0
%{?with_openssl:Requires:	openssl >= 0.9.8}
%{?with_sqlite:Requires:	sqlite3 >= 3.7}
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
License:	GPL v3+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-core-headers = %{version}-%{release}
%{?with_openssl:Requires:	openssl-devel >= 0.9.8}
Obsoletes:	libzrtpcpp-static

%description devel
Header files for libzrtpcpp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzrtpcpp.

%package core
Summary:	GNU ZRTP core library
Summary(pl.UTF-8):	Biblioteka podstawowa GNU ZRTP
License:	LGPL v3+
Group:		Libraries
#%{?with_openssl:Requires:	openssl >= 0.9.8}
%{?with_sqlite:Requires:	sqlite3 >= 3.7}

%description core
GNU ZRTP core library.

%description core -l pl.UTF-8
Biblioteka podstawowa GNU ZRTP.

%package core-headers
Summary:	GNU ZRTP core header files
Summary(pl.UTF-8):	Podstawowe pliki nagłówkowe GNU ZRTP
License:	LGPL v3+
Group:		Libraries
Requires:	libstdc++-devel
Conflicts:	libzrtpcpp-devel < 4

%description core-headers
GNU ZRTP core header files.

%description core-headers -l pl.UTF-8
Podstawowe pliki nagłówkowe GNU ZRTP.

%package core-devel
Summary:	GNU ZRTP core development files
Summary(pl.UTF-8):	Podstawowe pliki programistyczne GNU ZRTP
License:	LGPL v3+
Group:		Libraries
Requires:	%{name}-core = %{version}-%{release}
Requires:	%{name}-core-headers = %{version}-%{release}
#%{?with_openssl:Requires:	openssl-devel >= 0.9.8}

%description core-devel
GNU ZRTP core development files.

%description core-devel -l pl.UTF-8
Podstawowe pliki programistyczne GNU ZRTP.

%package tivi
Summary:	ZRTP tivi client library
Summary(pl.UTF-8):	Biblioteka kliencka ZRTP tivi
License:	for reference
Group:		Libraries
Requires:	sqlite3 >= 3.7

%description tivi
ZRTP tivi client library.

%description tivi -l pl.UTF-8
Biblioteka kliencka ZRTP tivi.

%package tivi-devel
Summary:	Development files for ZRTP tivi library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki klienckiej ZRTP tivi
License:	for reference
Group:		Development/Libraries
Requires:	%{name}-core-headers = %{version}-%{release}
Requires:	%{name}-tivi = %{version}-%{release}

%description tivi-devel
Development files for ZRTP tivi library.

%description tivi-devel -l pl.UTF-8
Pliki programistyczne biblioteki klienckiej ZRTP tivi.

%prep
%setup -q -n ZRTPCPP-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with ccrtp}
install -d build-ccrtp
cd build-ccrtp
%cmake .. \
	-DCCRTP=ON \
	%{?with_openssl:-DCRYPTO_STANDALONE=OFF}
%{__make}
cd ..
%endif

install -d build-core
cd build-core
%cmake .. \
	-DCORE_LIB=ON
# -DCRYPTO_STANDALONE=OFF is broken for core library
%{__make}
cd ..

%if %{with tivi}
install -d build-tivi
cd build-tivi
%cmake .. \
	-DTIVI=ON \
	%{?with_java:-DJAVA=ON}
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with ccrtp}
%{__make} -C build-ccrtp install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build-core install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with tivi}
cp -a build-tivi/clients/tivi/libzrtptivi.so* $RPM_BUILD_ROOT%{_libdir}
cp -p clients/tivi/*.h $RPM_BUILD_ROOT%{_includedir}/libzrtpcpp
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	core -p /sbin/ldconfig
%postun	core -p /sbin/ldconfig

%post	tivi -p /sbin/ldconfig
%postun	tivi -p /sbin/ldconfig

%if %{with ccrtp}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) %{_libdir}/libzrtpcpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzrtpcpp.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzrtpcpp.so
%{_includedir}/libzrtpcpp/CcrtpTimeoutProvider.h
%{_includedir}/libzrtpcpp/ZrtpQueue.h
%{_includedir}/libzrtpcpp/zrtpccrtp.h
%{_pkgconfigdir}/libzrtpcpp.pc
%endif

%files core
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) %{_libdir}/libzrtpcppcore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzrtpcppcore.so.4

%files core-headers
%defattr(644,root,root,755)
%dir %{_includedir}/libzrtpcpp
%{_includedir}/libzrtpcpp/common
%{_includedir}/libzrtpcpp/ZrtpCWrapper.h
%{_includedir}/libzrtpcpp/ZrtpCallback.h
%{_includedir}/libzrtpcpp/ZrtpCodes.h
%{_includedir}/libzrtpcpp/ZrtpConfigure.h
%{_includedir}/libzrtpcpp/ZrtpUserCallback.h

%files core-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzrtpcppcore.so
%{_pkgconfigdir}/libzrtpcppcore.pc

%if %{with tivi}
%files tivi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzrtptivi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzrtptivi.so.4

%files tivi-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzrtptivi.so
%{_includedir}/libzrtpcpp/CtZrtpCallback.h
%{_includedir}/libzrtpcpp/CtZrtpSession.h
%{_includedir}/libzrtpcpp/CtZrtpStream.h
%{_includedir}/libzrtpcpp/TiviTimeoutProvider.h
%endif
