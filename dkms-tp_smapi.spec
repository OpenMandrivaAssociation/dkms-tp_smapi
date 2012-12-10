%define	modname	tp_smapi
%define	name	dkms-%{modname}
%define	version	0.41
%define	release	1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	DKMS-ready module for SMAPI BIOS of ThinkPad laptops
License:	GPLv2+
Source0:	%{modname}-%{version}.tar.gz
Source1:	README.urpmi
Source2:	kernel-2.6.27-semaphore_h.patch
Url:		http://heanet.dl.sourceforge.net/sourceforge/tpctl/
Group:		Development/Kernel
Requires(pre):	dkms
Requires(post): dkms
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
mkdir -p %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}
mkdir -p %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}/patches
cp -a %{modname}-%{version}/* %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}
cp -a %SOURCE2 %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}/patches/
cat > %{buildroot}%{_usrsrc}/%{modname}-%{version}-%{release}/dkms.conf <<EOF

PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{modname}"
MAKE[0]="make -C \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build KBASE=\${kernel_source_dir}/.. KSRC=\${kernel_source_dir} KBUILD=\${kernel_source_dir} HDAPS=1"
CLEAN="make -C \${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build clean"
BUILT_MODULE_NAME[0]="\$PACKAGE_NAME"
DEST_MODULE_LOCATION[0]="/extra"
BUILT_MODULE_NAME[1]="thinkpad_ec"
DEST_MODULE_LOCATION[1]="/extra"
BUILT_MODULE_NAME[2]="hdaps"
DEST_MODULE_LOCATION[2]="/kernel/drivers/hwmon"
REMAKE_INITRD="no"
AUTOINSTALL="YES"
PATCH[0]=%(basename %SOURCE2)
PATCH_MATCH[0]="2\.6\.27"
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


%files
%doc %{modname}-%{version}/{README,CHANGES,TODO} README.urpmi
%docdir %{_usrsrc}/%{modname}-%{version}-%{release}/doc
/usr/src/%{modname}-%{version}-%{release}


%changelog
* Wed Dec 21 2011 Alexander Khrukin <akhrukin@mandriva.org> 0.41-1
+ Revision: 744103
- version update

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.40-4mdv2011.0
+ Revision: 610254
- rebuild

* Wed Mar 24 2010 Emmanuel Andry <eandry@mandriva.org> 0.40-3mdv2010.1
+ Revision: 527298
- rebuild

* Sat Feb 21 2009 Gustavo De Nardin <gustavodn@mandriva.com> 0.40-2mdv2009.1
+ Revision: 343703
- fixed License tag

* Sun Dec 28 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.40-1mdv2009.1
+ Revision: 320139
- new version 0.40

* Tue Sep 16 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.37-2mdv2009.0
+ Revision: 285108
- add tiny patch to support building in kernel 2.6.27

* Fri Aug 22 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.37-1mdv2009.0
+ Revision: 275137
- new version 0.37

* Tue Feb 19 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.36-1mdv2008.1
+ Revision: 172912
- new version 0.36

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

