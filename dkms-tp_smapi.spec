%define	modname	tp_smapi
%define	name	dkms-%{modname}
%define	version	0.36
%define	rel	1
%define	release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	DKMS-ready module for SMAPI BIOS of ThinkPad laptops
License:	GPL
Source0:	%{modname}-%{version}.tgz
Source1:	README.urpmi
Url:		http://heanet.dl.sourceforge.net/sourceforge/tpctl/
Group:		Development/Kernel
Requires(pre):	dkms
Requires(post): dkms
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildarch:	noarch

%description
ThinkPad laptops include a proprietary interface called SMAPI BIOS
(System Management Application Program Interface) which provides some
hardware control functionality that is not accessible by other means.

This driver exposes some features of the SMAPI BIOS through a sysfs
interface. It is suitable for newer models, on which SMAPI is invoked
through IO port writes.

WARNING:
This driver uses undocumented features and direct hardware access.
It thus cannot be guaranteed to work, and may cause arbitrary damage
(especially on models it wasn't tested on).

NOTE:
This package replaces module hdaps from upstream kernel with an
improved and tp_smapi compatible one. See the documentation.


%prep
%setup -q -c -n %{modname}-%{version}
chmod -R go=u-w .
# build in kernel 2.6.24 complains about not using EXTRA_CFLAGS
sed -i.bak -e 's/^CFLAGS/EXTRA_CFLAGS/' %{modname}-%{version}/Makefile
rm -f %{modname}-%{version}/Makefile.bak
cp %SOURCE1 .

%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}
cp -a %{modname}-%{version}/* %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}
cat > %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}/dkms.conf <<EOF

PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{modname}"
MAKE[0]="make -C \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build KBASE=\${kernel_source_dir}/.. KSRC=\${kernel_source_dir} KBUILD=\${kernel_build_dir} HDAPS=1"
CLEAN="make -C \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build clean"
BUILT_MODULE_NAME[0]="\$PACKAGE_NAME"
DEST_MODULE_LOCATION[0]="/extra"
BUILT_MODULE_NAME[1]="thinkpad_ec"
DEST_MODULE_LOCATION[1]="/extra"
BUILT_MODULE_NAME[2]="hdaps"
DEST_MODULE_LOCATION[2]="/kernel/drivers/hwmon"
REMAKE_INITRD="no"
AUTOINSTALL="YES"
EOF


%post
#if [ $1 == 1 ]
#then 
  dkms add -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade
  dkms build -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade
  dkms install -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade
#fi


%preun
#if [ $1 == 0 ]
#  then
  dkms remove -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade --all
#fi


%clean
rm -rf %buildroot


%files
%defattr(-,root,root)
%doc %{modname}-%{version}/{README,CHANGES,TODO} README.urpmi
%docdir %{_usrsrc}/%{modname}-%{version}-%{release}/doc
/usr/src/%{modname}-%{version}-%{release}
