Name:		velocity-tools-generic
Version:	3.1
Release:	1
Summary:	Generic tools for Apache Velocity
Group:		Development/Java
License:	ASL 2.0
URL:		https://velocity.apache.org/tools/3.1/
Source0:	https://github.com/apache/velocity-tools/archive/refs/tags/3.1.tar.gz#/velocity-tools-3.1.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	mvn(org.apache.velocity:velocity-engine-core)
BuildRequires:	mvn(commons-beanutils:commons-beanutils)
BuildRequires:	mvn(org.apache.commons:commons-digester3)
BuildRequires:	mvn(org.apache.commons:commons-lang3)
BuildRequires:	mvn(org.apache.commons:commons-text)
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(com.github.cliftonlabs:json-simple)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Generic Velocity tools with no servlet dependency. This is the module
Doxia's site renderer uses. Commons Lang 3.21 no longer has
StringEscapeUtils, so escaping goes through Commons Text. The parent
POM is the Velocity Tools reactor and is not packaged.

%prep
%autosetup -n velocity-tools-%{version}
rm -rf src
mv velocity-tools-generic/src src
sed -i 's/org\.apache\.commons\.lang3\.StringEscapeUtils/org.apache.commons.text.StringEscapeUtils/' \
	src/main/java/org/apache/velocity/tools/generic/EscapeTool.java
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.velocity.tools")
add(root, "artifactId", "velocity-tools-generic")
add(root, "version", "%{version}")
add(root, "name", "Apache Velocity Tools - Generic tools")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("org.apache.velocity", "velocity-engine-core", "2.4.1"),
    ("commons-beanutils", "commons-beanutils", "1.9.4"),
    ("org.apache.commons", "commons-digester3", "3.2"),
    ("org.apache.commons", "commons-lang3", "3.21.0"),
    ("org.apache.commons", "commons-text", "1.15.0"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
    ("com.github.cliftonlabs", "json-simple", "3.0.2"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
rm -rf velocity-tools-examples velocity-tools-generic velocity-tools-view velocity-tools-view-jsp

%files -f .mfiles
%doc LICENSE NOTICE README.md
