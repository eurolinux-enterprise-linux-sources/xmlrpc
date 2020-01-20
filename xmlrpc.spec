Name:       xmlrpc
Version:    3.1.3
Release:    7%{?dist}
Epoch:      1
Summary:    Java XML-RPC implementation
License:    ASL 2.0
URL:        http://ws.apache.org/xmlrpc/
Source0:    http://www.apache.org/dist/ws/xmlrpc/sources/apache-xmlrpc-%{version}-src.tar.bz2
# Add OSGi MANIFEST information
Patch0:     %{name}-client-addosgimanifest.patch
Patch1:     %{name}-common-addosgimanifest.patch
Patch2:     %{name}-javax-methods.patch

BuildRequires:  maven-local
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  ws-commons-util
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  tomcat-servlet-3.0-api
BuildRequires:  junit
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  apache-commons-logging

BuildArch:    noarch

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:    Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package common
Summary:    Common classes for XML-RPC client and server implementations
# Provide xmlrpc is not here because it would be useless due to different jar names
Obsoletes:  %{name} < 3.1.3
Obsoletes:  %{name}3-common < 3.1.3-13
Provides:   %{name}3-common = 3.1.3-13
# in OSGI manifest
Requires:   apache-commons-logging

%description common
%{summary}.

%package client
Summary:    XML-RPC client implementation
Obsoletes:  %{name}3-client < 3.1.3-13
Provides:  %{name}3-client = 3.1.3-13
# in OSGI manifest
Requires:   jakarta-commons-httpclient

%description client
%{summary}.

%package server
Summary:    XML-RPC server implementation
Obsoletes:  %{name}3-server < 3.1.3-13
Provides:  %{name}3-server = 3.1.3-13

%description server
%{summary}.

%prep
%setup -q -n apache-%{name}-%{version}-src
%patch2 -b .sav
pushd client
%patch0 -b .sav
popd
pushd common
%patch1 -b .sav
popd

sed -i 's/\r//' LICENSE.txt

%pom_remove_dep jaxme:jaxmeapi

%pom_disable_module dist

%mvn_package :xmlrpc common
%mvn_package :xmlrpc-{common} @1
%mvn_package :xmlrpc-{client} @1
%mvn_package :xmlrpc-{server} @1

%mvn_file :xmlrpc-{common} %{name}-@1 %{name}3-@1
%mvn_file :xmlrpc-{client} %{name}-@1 %{name}3-@1
%mvn_file :xmlrpc-{server} %{name}-@1 %{name}3-@1

%build
# ignore test failure because server part needs network
%mvn_build -f

%install
%mvn_install

%files common -f .mfiles-common
%doc LICENSE.txt NOTICE.txt

%files client -f .mfiles-client
%files server -f .mfiles-server

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Mon Aug 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.1.3-7
- Migrate away from mvn-rpmbuild (#997460)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri May 17 2013 Alexander Kurtakov <akurtako@redhat.com> 1:3.1.3-5
- Remove javax.xml.bind from osgi imports - it's part of the JVM now.
- Drop the ws-jaxme dependency for the same reason.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:3.1.3-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Oct 20 2012 Peter Robinson <pbrobinson@fedoraproject.org>	3.1.3-2
- xmlrpc v2 had an Epoch so we need one here. Add it back

* Fri Sep 14 2012 Alexander Kurtakov <akurtako@redhat.com> 3.1.3-1
- First release of version 3.x package
