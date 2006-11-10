Summary:	GNU RTP stack for the zrtp protocol specification
Name:		libzrtpcpp
Version:	0.9.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.gnu.org/pub/gnu/ccrtp/%{name}-%{version}.tar.gz
# Source0-md5:	a439328318f25e3069549e265902a119
URL:		http://wiki.gnutelephony.org/index.php/GNU_ccRTP
BuildRequires:	ccrtp-devel >= 1.5.0
BuildRequires:	doxygen
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library is a GPL licensed extension to the GNU RTP Stack, ccrtp,
that offers compatibility with Phil Zimmermann's zrtp/Zfone voice
encryption, and which can be directly embedded into telephony
applications.

%package devel
Summary:	Header files for libzrtpcpp library
Summary(pl):	Pliki nag³ówkowe biblioteki libzrtpcpp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	commoncpp2-devel

%description devel
Header files for libzrtpcpp library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libzrtpcpp.

%package static
Summary:	Static libzrtpcpp library
Summary(pl):	Statyczna biblioteka libzrtpcpp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libzrtpcpp library.

%description static -l pl
Statyczna biblioteka libzrtpcpp.

%prep
%setup -q

%build
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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/libzrtpcpp
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
