%define snap 20060524

%define libmajor 1
%define libname %mklibname %{name} %{libmajor}
%define develname %mklibname %name -d
%define sdevelname %mklibname %name -d -s

Summary:	MDB Tools accesses data stored in Microsoft Access databases
Name:		mdbtools
Version:	0.6
Release:	%mkrel 0.%{snap}.7
Group:		Development/Databases
License:	LGPLv2+ and GPLv2+
URL:		http://mdbtools.sourceforge.net
Source0:	%{name}-%{version}-%{snap}.tar.bz2
Patch0:		mdbtools-linkage_fix.diff
Patch1:		mdbtools-0.6-20060524-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	libglade2.0-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	unixODBC-devel
BuildRequires:	imagemagick
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib-devel
BuildRequires:	libtool
Requires:	%{libname} = %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mdb-dump   -- simple hex dump utility for looking at mdb files
mdb-schema -- prints DDL for the specified table
mdb-export -- export table to CSV format
mdb-tables -- a simple dump of table names to be used with shell scripts
mdb-header -- generates a C header to be used in exporting mdb data to a C prog
mdb-parsecvs -- generates a C program given a CSV file made with mdb-export
mdb-sql -- demo SQL engine program
mdb-ver -- print version of database

%package -n	%{develname}
Summary:	Include files needed for development with MDB Tools
Group:		Development/Databases
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %version-%release
Provides:	%{name}-devel = %version-%release
Obsoletes:	%mklibname -d mdbtools 1

%description -n	%{develname}
The libmdbtools-devel package contains the files necessary for development
with with the MDB Tools libraries.

%package -n	%{sdevelname}
Summary:	Include files needed for development with MDB Tools
Group:		Development/Databases
Requires:	%{develname} = %{version}
Provides:	%{name}-static-devel = %version-%release
Provides:       lib%{name}-static-devel = %version-%release
Obsoletes:	%mklibname -d -s mdbtools 1

%description -n	%{sdevelname}
The libmdbtools-static-devel package contains the files necessary for 
development with with the MDB Tools libraries.

%package -n	%{libname}
Summary:	MDB Tools ODBC driver for unixODBC
Group:		System/Libraries
Conflicts:	%{_lib}%{name}0 < 0.6.0

%description -n	%{libname}
The libmdbtools package contains ODBC driver build for unixODBC.

%package	gui
Summary:	The gmdb2 graphical interface for MDB Tools
Group:		Databases

%description	gui
The mdbtools-gui package contains the gmdb2 graphical user interface for 
MDB Tools

%prep

%setup -q -n %{name}
%patch0 -p0
%patch1 -p1 -b .format_not_a_string_literal_and_no_format_arguments


# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure.in

%build
sh ./autogen.sh

%configure2_5x \
    --with-unixodbc=%{_prefix}

%make

%install
rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gmdb
Comment=GNOME MDB Viewer
Exec=%{_bindir}/gmdb2
Icon=%{name}
Terminal=false
Type=Application
Categories=GNOME;GTK;;
EOF

mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir},%{_iconsdir}}
convert src/gmdb2/pixmaps/logo.xpm -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert src/gmdb2/pixmaps/logo.xpm -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert src/gmdb2/pixmaps/logo.xpm -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post gui
%update_menus
%endif

%if %mdkversion < 200900
%postun gui
%clean_menus
%endif

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

%files -n %{develname}
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

%files -n %{sdevelname}
%defattr (-,root,root)
%{_libdir}/libmdbsql.a
%{_libdir}/libmdb.a
%{_libdir}/libmdbodbc.a

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libmdb.so.%{libmajor}*
%{_libdir}/libmdbsql.so.%{libmajor}*
%{_libdir}/libmdbodbc.so.0*

%files gui
%defattr (-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO HACKING
%{_iconsdir}/%{name}.*
%{_miconsdir}/%{name}.*
%{_liconsdir}/%{name}.*
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
