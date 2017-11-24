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
Version:	1.7.3
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/santuario/c-library/%{name}-%{version}.tar.bz2
# Source0-md5:	61130e3273bed410e607d9710eef9de2
Patch0:		%{name}-c++.patch
URL:		http://santuario.apache.org/cindex.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
%{?with_nss:BuildRequires:	nss-devel >= 3}
%{?with_openssl:BuildRequires:	openssl-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%{?with_xalan:BuildRequires:	xalan-c-devel}
BuildRequires:	xerces-c-devel >= 2.0
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
%{?with_openssl:Requires:	openssl-devel}
%{?with_xalan:Requires:	xalan-c-devel}
Requires:	xerces-c-devel >= 2.0

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
%patch0 -p1

# Remove bogus "-O2" from CXXFLAGS to avoid overriding optflags.
%{__sed} -i -e 's/-O2 -DNDEBUG/-DNDEBUG/g' configure.ac

%build
# refresh lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_nss:--with-nss} \
	%{!?with_openssl:--without-openssl} \
	%{!?with_xalan:--without-xalan} \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
# Verify that what was compiled actually works.
xsec/xtest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CPPROG="cp -p" \
	DESTDIR=$RPM_BUILD_ROOT

# Do not ship library test utilities. These are only needed for
# xml-security-c developers and they should have the whole source anyway.
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt INSTALL.txt NOTICE.txt
%attr(755,root,root) %{_libdir}/libxml-security-c.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libxml-security-c.so.17

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxml-security-c.so
%{_includedir}/xsec

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxml-security-c.a
%endif
