Name:           mdbtools
Version:        0.9.4
Release:        1
Summary:        Access data stored in Microsoft Access databases

Group:          Development/Databases
License:        GPLv2+
URL:            https://github.com/mdbtools/mdbtools/wiki

Source0:        https://github.com/mdbtools/mdbtools/releases/download/v%{version}/mdbtools-%{version}.tar.gz
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  unixODBC-devel
BuildRequires:  readline-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  desktop-file-utils
BuildRequires:  txt2man
BuildRequires:  rarian
BuildRequires:  gnome-doc-utils
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake
Requires:       %{name}-libs = %{EVRD}
# The GUI was dropped after 0.7.x
Obsoletes:	%{name}-gui < %{EVRD}

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

%prep
%autosetup -p1
sed -i -e 's,-Werror,,g' configure.ac
autoreconf -vif
%configure --disable-static --enable-sql --with-unixodbc="%{_prefix}" --enable-gtk-doc

%build
%make_build V=1

%install
%make_install

# remove some headers which should not be installed / exported
rm -f %{buildroot}%{_includedir}/gmdb.h
rm -f %{buildroot}%{_includedir}/mdbver.h

mkdir -p %{buildroot}%{_datadir}/applications


%files
%doc COPYING
%{_bindir}/mdb-*
%{_mandir}/man1/mdb-*
%{_datadir}/bash-completion/completions/*

%files libs
%doc AUTHORS COPYING.LIB NEWS
%{_libdir}/libmdb*.so.*

%files devel
%doc HACKING
%{_libdir}/libmdb*.so
%{_libdir}/pkgconfig/libmdb*.pc
%{_includedir}/mdb*.h
