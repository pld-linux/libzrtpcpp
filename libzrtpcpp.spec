Summary:	GNU RTP stack for the zrtp protocol specification
Summary(pl.UTF-8):	Stos GNU RTP dla specyfikacji protokołu zrtp
Name:		libzrtpcpp
Version:	1.3.0
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/ccrtp/%{name}-%{version}.tar.gz
# Source0-md5:	e2abd4f7cf68496d0772dd7e5a71873a
Patch0:		%{name}-build.patch
URL:		http://wiki.gnutelephony.org/index.php/GNU_ccRTP
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	ccrtp-devel >= 1.5.1
BuildRequires:	commoncpp2-devel >= 1.3.0
BuildRequires:	doxygen
BuildRequires:	libgcrypt-devel >= 1.2.3
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
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
Requires:	ccrtp-devel >= 1.5.1
Requires:	commoncpp2-devel >= 1.3.0
Requires:	libgcrypt-devel >= 1.2.3
Requires:	libstdc++-devel

%description devel
Header files for libzrtpcpp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzrtpcpp.

%package static
Summary:	Static libzrtpcpp library
Summary(pl.UTF-8):	Statyczna biblioteka libzrtpcpp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libzrtpcpp library.

%description static -l pl.UTF-8
Statyczna biblioteka libzrtpcpp.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
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
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libzrtpcpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzrtpcpp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzrtpcpp.so
%{_libdir}/libzrtpcpp.la
%{_includedir}/libzrtpcpp
%{_pkgconfigdir}/libzrtpcpp.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libzrtpcpp.a
