#
# spec file for package runit (Version 2.1.1)
#
# Copyright (c) 2010 Ian Meyer <ianmmeyer@gmail.com>

Name:           runit
Version:        2.1.1
Release:        2

Group:          System/Base
License:        BSD

# Override _sbindir being /usr/sbin
%define _sbindir /sbin

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Url:            http://smarden.org/runit/
Source:         http://smarden.org/runit/runit-%{version}.tar.gz
Patch:          runit-2.1.1-etc-service.patch
Patch1:         runit-2.1.1-runsvdir-path-cleanup.patch

Obsoletes: runit <= %{version}-%{release}
Provides: runit = %{version}-%{release}

Summary:        A UNIX init scheme with service supervision

%description
runit is a cross-platform Unix init scheme with service supervision; a
replacement for sysvinit and other init schemes. It runs on GNU/Linux, *BSD,
Mac OS X, and Solaris, and can easily be adapted to other Unix operating
systems. runit implements a simple three-stage concept. Stage 1 performs the
system's one-time initialization tasks. Stage 2 starts the system's uptime
services (via the runsvdir program). Stage 3 handles the tasks necessary to
shutdown and halt or reboot.

Authors:
---------
    Gerrit Pape <pape@smarden.org>

%prep
%setup -n admin/%{name}-%{version}
%patch
%patch1

%build
sh package/compile

%install
for i in $(< package/commands) ; do
    %{__install} -D -m 0755 command/$i %{buildroot}%{_sbindir}/$i
done
for i in man/*8 ; do
    %{__install} -D -m 0755 $i %{buildroot}%{_mandir}/man8/${i##man/}
done
%{__install} -d -m 0755 %{buildroot}/etc/service
%{__install} -D -m 0750 etc/2 %{buildroot}%{_sbindir}/runsvdir-start

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 = 1 ];
then
  grep -q 'RI:123456:respawn:/sbin/runsvdir-start' /etc/inittab
  if [ $? -eq 1 ]
  then
    echo -n "Installing /sbin/runsvdir-start into /etc/inittab.."
    echo "RI:123456:respawn:/sbin/runsvdir-start" >> /etc/inittab
    echo " success."
    # Reload init
    telinit q
  fi
fi

%postun
if [ $1 = 0 ];
then
  echo " #################################################"
  echo " # Remove /sbin/runsvdir-start from /etc/inittab #"
  echo " # if you really want to remove runit            #"
  echo " #################################################"
fi

%files
%defattr(-,root,root,-)
%{_sbindir}/chpst
%{_sbindir}/runit
%{_sbindir}/runit-init
%{_sbindir}/runsv
%{_sbindir}/runsvchdir
%{_sbindir}/runsvdir
%{_sbindir}/sv
%{_sbindir}/svlogd
%{_sbindir}/utmpset
%{_sbindir}/runsvdir-start
%{_mandir}/man8/*.8*
%doc doc/* etc/
%doc package/CHANGES package/COPYING package/README package/THANKS package/TODO
%dir /etc/service

%changelog
* Sun Jan 23 2011 ianmmeyer@gmail.com
- Make compatible with Redhat based systems
