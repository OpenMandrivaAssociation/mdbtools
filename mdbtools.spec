%define snap 20060524

%define libmajor 1
%define libname %mklibname %{name} %{libmajor}

Summary:	MDB Tools accesses data stored in Microsoft Access databases
Name:		mdbtools
Version:	0.6
Release:	%mkrel 0.%{snap}.1
Group:		Development/Databases
License:	LGPL/GPL
URL:		http://mdbtools.sourceforge.net
Source0:	%{name}-%{version}-%{snap}.tar.bz2
BuildRequires:	libglade2.0-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	unixODBC-devel
BuildRequires:	ImageMagick
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib-devel
Requires:	%{libname} = %{version}
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
mdb-dump   -- simple hex dump utility for looking at mdb files
mdb-schema -- prints DDL for the specified table
mdb-export -- export table to CSV format
mdb-tables -- a simple dump of table names to be used with shell scripts
mdb-header -- generates a C header to be used in exporting mdb data to a C prog
mdb-parsecvs -- generates a C program given a CSV file made with mdb-export
mdb-sql -- demo SQL engine program
mdb-ver -- print version of database

%package -n	%{libname}-devel
Summary:	Include files needed for development with MDB Tools
Group:		Development/Databases
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel

%description -n	%{libname}-devel
The libmdbtools-devel package contains the files necessary for development
with with the MDB Tools libraries.

%package -n	%{libname}-static-devel
Summary:	Include files needed for development with MDB Tools
Group:		Development/Databases
Requires:	%{libname}-devel = %{version}

%description -n	%{libname}-static-devel
The libmdbtools-static-devel package contains the files necessary for 
development with with the MDB Tools libraries.

%package -n	%{libname}
Summary:	MDB Tools ODBC driver for unixODBC
Group:		System/Libraries

%description -n	%{libname}
The libmdbtools package contains ODBC driver build for unixODBC.

%package	gui
Summary:	The gmdb2 graphical interface for MDB Tools
Group:		Databases
#Requires:      %{libname} = %{version}, libgnomeui2_0, libglade2.0_0

%description	gui
The mdbtools-gui package contains the gmdb2 graphical user interface for 
MDB Tools

%prep

%setup -q -n %{name}

%build
sh ./autogen.sh

%configure2_5x \
    --with-unixodbc

%make

%install
rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}%{_menudir}
cat <<EOF > %{buildroot}%{_menudir}/%{name}-gui
?package(%{name}-gui): \
needs="x11" \
section="More Applications/Databases" \
title="Gmdb" \
longtitle="GNOME MDB Viewer" \
command="%{_bindir}/gmdb2" needs="X11" \
icon="%{name}.png" \
xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gmdb
Comment=GNOME MDB Viewer
Exec=%{_bindir}/gmdb2
Icon=%{name}
Terminal=false
Type=Application
Categories=GNOME;GTK;X-MandrivaLinux-MoreApplications-Databases;
EOF

mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir},%{_iconsdir}}
convert src/gmdb2/pixmaps/logo.xpm -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert src/gmdb2/pixmaps/logo.xpm -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert src/gmdb2/pixmaps/logo.xpm -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post gui
%update_menus

%postun gui
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO HACKING
%{_bindir}/mdb-array
%{_bindir}/mdb-export
%{_bindir}/mdb-header
%{_bindir}/mdb-hexdump
%{_bindir}/mdb-parsecsv
%{_bindir}/mdb-prop
%{_bindir}/mdb-schema
%{_bindir}/mdb-sql
%{_bindir}/mdb-tables
%{_bindir}/mdb-ver
%{_mandir}/man1/*

%files -n %{libname}-devel
%defattr (-,root,root)
%{_includedir}/connectparams.h
%{_includedir}/gmdb.h
%{_includedir}/mdbodbc.h
%{_includedir}/mdbprivate.h
%{_includedir}/mdbsql.h
%{_includedir}/mdbtools.h
%{_includedir}/mdbver.h
%{_libdir}/libmdb.la
%{_libdir}/libmdbsql.la
%{_libdir}/libmdbodbc.la
%{_libdir}/libmdb.so
%{_libdir}/libmdbsql.so
%{_libdir}/libmdbodbc.so
%{_libdir}/pkgconfig/libmdb.pc
%{_libdir}/pkgconfig/libmdbsql.pc

%files -n %{libname}-static-devel
%defattr (-,root,root)
%{_libdir}/libmdbsql.a
%{_libdir}/libmdb.a
%{_libdir}/libmdbodbc.a

%files -n %{libname}
%defattr(-,root,root)
#%{_libdir}/libmdb.la
%{_libdir}/libmdb.so.*
#%{_libdir}/libmdbsql.la
%{_libdir}/libmdbsql.so.*
%{_libdir}/libmdbodbc.so.*

%files gui
%defattr (-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO HACKING
%{_iconsdir}/%{name}.*
%{_miconsdir}/%{name}.*
%{_liconsdir}/%{name}.*
%{_menudir}/%{name}-gui
%{_datadir}/applications/*
%{_bindir}/gmdb2
%{_datadir}/gmdb/glade/code.xpm
%{_datadir}/gmdb/glade/debug.xpm
%{_datadir}/gmdb/glade/form_big.xpm
%{_datadir}/gmdb/glade/forms.xpm
%{_datadir}/gmdb/glade/gmdb-debug.glade
%{_datadir}/gmdb/glade/gmdb-export.glade
%{_datadir}/gmdb/glade/gmdb.glade
%{_datadir}/gmdb/glade/gmdb-prefs.glade
%{_datadir}/gmdb/glade/gmdb-props.glade
%{_datadir}/gmdb/glade/gmdb-schema.glade
%{_datadir}/gmdb/glade/gmdb-sql-file.glade
%{_datadir}/gmdb/glade/gmdb-sql.glade
%{_datadir}/gmdb/glade/logo.xpm
%{_datadir}/gmdb/glade/macro_big.xpm
%{_datadir}/gmdb/glade/macros.xpm
%{_datadir}/gmdb/glade/module_big.xpm
%{_datadir}/gmdb/glade/pk.xpm
%{_datadir}/gmdb/glade/query_big.xpm
%{_datadir}/gmdb/glade/query.xpm
%{_datadir}/gmdb/glade/report_big.xpm
%{_datadir}/gmdb/glade/reports.xpm
%{_datadir}/gmdb/glade/stock_export-16.png
%{_datadir}/gmdb/glade/stock_export.png
%{_datadir}/gmdb/glade/table_big.xpm
%{_datadir}/gmdb/glade/table.xpm
%{_datadir}/gnome/help/gmdb/C/gmdb.xml
%{_datadir}/gnome/help/gmdb/C/legal.xml
%{_datadir}/gnome/help/gmdb/C/figures/gmdb2_window.png
%{_datadir}/gnome/help/gmdb/C/figures/gmdb2_sql_window.png
