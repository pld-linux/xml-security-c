#
# Conditional build:
%bcond_without	tests		# unit tests
%bcond_without	static_libs	# static library
%bcond_with	nss		# NSS crypto provider
%bcond_without	openssl		# OpenSSL crypto provider
%bcond_without	xalan		# xalan-c (XPath and XSLT transformations) support

Summary:	C++ Implementation of W3C security standards for XML
Summary(pl.UTF-8):	Implementacja w C++ standardów bezpieczeństwa W3C dla XML
Name:		xml-security-c
Version:	2.0.4
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://downloads.apache.org/santuario/c-library/%{name}-%{version}.tar.bz2
# Source0-md5:	53d202a6c8d082bd8291c727f4918db5
URL:		https://santuario.apache.org/cindex.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
%{?with_nss:BuildRequires:	nss-devel >= 3}
%{?with_openssl:BuildRequires:	openssl-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%{?with_xalan:BuildRequires:	xalan-c-devel >= 1.11}
BuildRequires:	xerces-c-devel >= 3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The xml-security-c library is a C++ implementation of the XML Digital
Signature specification.

The library makes use of the Apache XML project's Xerces-C XML Parser
and Xalan-C XSLT processor. The latter is used for processing XPath
and XSLT transforms.

%description -l pl.UTF-8
Biblioteka xml-security-c to implementacja w C++ specyfikacji XML
Digital Signature.

Biblioteka wykorzystuje parser XML Xerces-C oraz procesor XSLT Xalan-C
z projektu Apache XML. Biblioteka Xalan-C jest wykorzystywana do
przekształceń XPath i XSLT.

%package devel
Summary:	Development files for xml-security-c
Summary(pl.UTF-8):	Pliki programistyczne xml-security-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
%{?with_nss:Requires:	nss-devel >= 3}
%{?with_openssl:Requires: openssl-devel}
%{?with_xalan:Requires: xalan-c-devel >= 1.11}
Requires:	xerces-c-devel >= 3.2

%description devel
This package provides development files for xml-security-c, a C++
library for XML Digital Signatures.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne xml-security-c - biblioteki
C++ do podpisów cyfrowych XML.

%package static
Summary:	Static xml-security-c library
Summary(pl.UTF-8):	Statyczna biblioteka xml-security-c
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static xml-security-c library.

%description static -l pl.UTF-8
Statyczna biblioteka xml-security-c.

%prep
%setup -q

%build
# refresh lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_nss:--without-nss} \
	%{!?with_openssl:--without-openssl} \
	%{!?with_xalan:--without-xalan} \
	%{?with_static_libs:--enable-static}
%{__make}

%if %{with tests}
# Verify that what was compiled actually works.
xsec/xsec-xtest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CPPROG="cp -p" \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libxml-security-c.la

# Do not ship library test utilities. These are only needed for
# xml-security-c developers and they should have the whole source anyway.
%{__rm} $RPM_BUILD_ROOT%{_bindir}/xsec-xtest

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt INSTALL.txt NOTICE.txt
%attr(755,root,root) %{_bindir}/xsec-c14n
%attr(755,root,root) %{_bindir}/xsec-checksig
%attr(755,root,root) %{_bindir}/xsec-cipher
%attr(755,root,root) %{_bindir}/xsec-siginf
%attr(755,root,root) %{_bindir}/xsec-templatesign
%attr(755,root,root) %{_bindir}/xsec-txfmout
%attr(755,root,root) %{_bindir}/xsec-xklient
%attr(755,root,root) %{_libdir}/libxml-security-c.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libxml-security-c.so.20

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxml-security-c.so
%{_includedir}/xsec
%{_pkgconfigdir}/xml-security-c.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxml-security-c.a
%endif
