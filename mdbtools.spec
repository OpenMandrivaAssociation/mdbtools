Name:           mdbtools
Version:        0.7.1
Release:        1
Summary:        Access data stored in Microsoft Access databases

Group:          Development/Databases
License:        GPLv2+
URL:            https://github.com/brianb/mdbtools/wiki

Source0:        https://github.com/brianb/mdbtools/archive/%{version}.tar.gz
Source1:        gmdb2.desktop
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libgnomeui-2.0)
BuildRequires:  unixODBC-devel
BuildRequires:  readline-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  desktop-file-utils
BuildRequires:  txt2man
BuildRequires:  gnome-common
BuildRequires:  pkgconfig(libglade-2.0)
BuildRequires:  rarian
BuildRequires:  gnome-doc-utils
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake
Requires:       %{name}-libs = %{EVRD}

%description
MDB Tools is a suite of programs for accessing data stored in Microsoft
Access databases.

%package libs
Summary:        Library for accessing data stored in Microsoft Access databases
Group:          System/Libraries
License:        LGPLv2+

%description libs
This package contains the MDB Tools library, which can be used by applications
to access data stored in Microsoft Access databases.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Databases
License:        LGPLv2+
Requires:       %{name}-libs = %{EVRD}
Requires:	glib2-devel
Requires:	pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package gui
Summary:        Graphical interface for MDB Tools
Group:          Development/Databases
License:        GPLv2+ 
Requires:       %{name}-libs = %{EVRD}

%description gui
The mdbtools-gui package contains the gmdb2 graphical user interface
for MDB Tools

%prep
%setup -q

%build
autoreconf -vif
%configure --disable-static --enable-sql --with-unixodbc="%{_prefix}" --enable-gtk-doc
%make V=1

%install
%makeinstall_std

# remove some headers which should not be installed / exported
rm -f %{buildroot}%{_includedir}/gmdb.h
rm -f %{buildroot}%{_includedir}/mdbver.h

mkdir -p %{buildroot}%{_datadir}/applications

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

%files
%doc COPYING
%{_bindir}/mdb-*
%{_mandir}/man1/mdb-*

%files libs
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/libmdb*.so.*

%files devel
%doc HACKING ChangeLog TODO doc/faq.html
%{_libdir}/libmdb*.so
%{_libdir}/pkgconfig/libmdb*.pc
%{_includedir}/mdb*.h

%files gui
%{_bindir}/gmdb2
%{_datadir}/gmdb
%{_datadir}/gnome/help/gmdb
%{_datadir}/applications/*gmdb2.desktop
%{_datadir}/omf/mdbtools/gmdb-C.omf
%{_mandir}/man1/gmdb2*

