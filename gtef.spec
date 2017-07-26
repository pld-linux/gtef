#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Gtef - GTK+ Text Editor Framework
Summary(pl.UTF-8):	Gtef (GTK+ Text Editor Framework) - szkielet edytora tekstu operatego na GTK+
Name:		gtef
Version:	2.0.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtef/2.0/%{name}-%{version}.tar.xz
# Source0-md5:	fbd29e1b3503156e5d40714839474b25
URL:		https://wiki.gnome.org/Projects/Gtef
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.14
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 1:2.52
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gtk+3-devel >= 3.20
BuildRequires:	gtk-doc >= 1.25
BuildRequires:	gtksourceview3-devel >= 3.22
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.5
BuildRequires:	pkgconfig
BuildRequires:	uchardet-devel
BuildRequires:	vala
Requires:	glib2 >= 1:2.52
Requires:	gtk+3 >= 3.20
Requires:	gtksourceview3 >= 3.22
Requires:	libxml2 >= 1:2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The final goal is to create a Tabbed Document Interface (TDI)
framework suitable for text editors.

But the first short-term goal is to have a higher-level API to load
and save a file. All the errors would be handled by Gtef, showing
GtkInfoBars etc.

%description -l pl.UTF-8
Ostatecznym celem projektu jest stworzenie szkieletu zakładkowego
interfejsu do dokumentów (TDI - Tabbed Document Interface), nadającego
się do edytorów tekstu.

Ale pierwszym, krótkoterminowym celem, jest stworzenie
wysokopoziomowego API do wczytywania i zapisywania plików. Wszystkie
błędy mają być obsługiwane przez Gtef, z wyświetlaniem GtkInfoBarów
itp.

%package devel
Summary:	Header files for Gtef library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Gtef
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.52
Requires:	gtk+3-devel >= 3.20
Requires:	gtksourceview3-devel >= 3.22
Requires:	libxml2-devel >= 1:2.5
Requires:	uchardet-devel

%description devel
Header files for Gtef library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Gtef.

%package static
Summary:	Static Gtef library
Summary(pl.UTF-8):	Statyczna biblioteka Gtef
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Gtef library.

%description static -l pl.UTF-8
Statyczna biblioteka Gtef.

%package -n vala-gtef
Summary:	Vala API for Gtef library
Summary(pl.UTF-8):	API języka Vala do biblioteki Gtef
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala

%description -n vala-gtef
Vala API for Gtef library.

%description -n vala-gtef -l pl.UTF-8
API języka Vala do biblioteki Gtef.

%package apidocs
Summary:	API documentation for Gtef library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Gtef
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Gtef library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Gtef.

%prep
%setup -q

%build
# rebuild ac/am/lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgtef-2.la

%find_lang gtef-2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f gtef-2.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libgtef-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtef-2.so.0
%{_libdir}/girepository-1.0/Gtef-2.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtef-2.so
%{_includedir}/gtef-2
%{_datadir}/gir-1.0/Gtef-2.gir
%{_pkgconfigdir}/gtef-2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgtef-2.a
%endif

%files -n vala-gtef
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gtef-2.deps
%{_datadir}/vala/vapi/gtef-2.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gtef-2.0
