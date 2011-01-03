#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	static_libs	# don't build static libraries
%bcond_without	xalan_c		# build without xalan-c (XPath and XSLT transformations cannot be performed)

Summary:	C++ Implementation of W3C security standards for XML
Name:		xml-security-c
Version:	1.5.1
Release:	1
License:	ASL 2.0
Group:		Libraries
URL:		http://santuario.apache.org/c/
Source0:	http://santuario.apache.org/dist/c-library/%{name}-%{version}.tar.gz
# Source0-md5:	2c47c4ec12e8d6abe967aa5e5e99000c
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%{?with_xalan_c:BuildRequires:	xalan-c-devel}
BuildRequires:	xerces-c-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The xml-security-c library is a C++ implementation of the XML Digital
Signature specification.

The library makes use of the Apache XML project's Xerces-C XML Parser
and Xalan-C XSLT processor. The latter is used for processing XPath
and XSLT transforms.

%package devel
Summary:	Development files for xml-security-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel
%{?with_xalan_c:Requires:	xalan-c-devel}
Requires:	xerces-c-devel

%description devel
This package provides development files for xml-security-c, a C++
library for XML Digital Signatures.

%package static
Summary:	Static xml-security-c library
Summary(pl.UTF-8):	Statyczna biblioteka xml-security-c
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static xml-security-c library.

%prep
%setup -q
# Remove bogus "-O2" from CXXFLAGS to avoid overriding RPM_OPT_FLAGS.
sed -i -e 's/-O2 -DNDEBUG/-DNDEBUG/g' configure

%build
%configure \
	%{!?with_xalan:--without-xalan} \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
# Verify that what was compiled actually works.
./bin/xtest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	CPPROG="cp -p" \
	DESTDIR=$RPM_BUILD_ROOT

# We do not ship .la files.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Do not ship library test utilities. These are only needed for
# xml-security-c developers and they should have the whole source anyway.
rm -rf $RPM_BUILD_ROOT%{_bindir}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxml-security-c.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libxml-security-c.so.15

%files devel
%defattr(644,root,root,755)
%{_includedir}/xsec
%{_libdir}/libxml-security-c.so

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxml-security-c.a
%endif
