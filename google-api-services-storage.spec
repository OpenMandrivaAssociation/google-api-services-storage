Name:		google-api-services-storage
Version:	v1.rev20220705.1.32.1
Release:	1
Summary:	Google Cloud Storage JSON API client
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/googleapis/google-api-java-client-services
# Generated Java client for Cloud Storage JSON API. The Maven Central
# sources jar also shipped class files and jars; this archive keeps the
# Java sources, the discovery document, and the Apache-2.0 license.
# The catalog pin has two hyphens. RPM stores the dotted form, which
# the Gradle metadata comparison treats as the same version.
Source0:	google-api-services-storage-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	mvn(com.google.api-client:google-api-client) = 1.34.0
BuildRequires:	mvn(com.google.http-client:google-http-client) = 1.42.2
BuildRequires:	mvn(com.google.http-client:google-http-client-gson) = 1.42.2
BuildRequires:	mvn(com.google.oauth-client:google-oauth-client) = 1.34.1
BuildRequires:	mvn(com.google.guava:guava) = 33.6.0-jre
BuildRequires:	mvn(com.google.guava:failureaccess) = 1.0.3
BuildRequires:	mvn(com.google.code.gson:gson) = 2.14.0
BuildRequires:	mvn(org.apache.httpcomponents:httpclient) = 4.5.14
BuildRequires:	mvn(org.apache.httpcomponents:httpcore) = 4.4.16
BuildRequires:	mvn(commons-logging:commons-logging) = 1.4.0
Requires:	mvn(com.google.api-client:google-api-client) = 1.34.0

%description
Cloud Storage JSON API v1 client used by Gradle. The classes are the
generated sources compiled against google-api-client 1.34.0. The
provides version is v1.rev20220705.1.32.1.

%prep
%autosetup -n google-api-services-storage-%{version}
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete

%build
set -eo pipefail
find com -name '*.java' > sources.list
test "$(wc -l < sources.list)" -eq 24
CP=%{_javadir}/google-api-client.jar:%{_javadir}/google-http-client.jar:%{_javadir}/google-http-client-gson.jar:%{_javadir}/google-http-client-apache-v2.jar:%{_javadir}/google-oauth-client.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/gson-2.14.0.jar:%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/commons-logging.jar
mkdir -p classes
javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d classes @sources.list
if [ -d resources ]; then
	/bin/cp -a resources/. classes/
fi
cat > manifest.mf << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.services.storage

EOF
jar cfm google-api-services-storage.jar manifest.mf -C classes .
jar i google-api-services-storage.jar
javap -verbose -cp google-api-services-storage.jar com.google.api.services.storage.Storage | grep -F 'major version: 55'

cat > google-api-services-storage.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.apis</groupId>
  <artifactId>google-api-services-storage</artifactId>
  <version>v1.rev20220705.1.32.1</version>
  <name>Cloud Storage JSON API</name>
  <description>Generated client for the Google Cloud Storage JSON API</description>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>com.google.api-client</groupId>
      <artifactId>google-api-client</artifactId>
      <version>1.34.0</version>
    </dependency>
  </dependencies>
</project>
EOF

%install
sysjar install --buildroot %{buildroot} \
	--artifact google-api-services-storage.pom:google-api-services-storage.jar \
	--file-name google-api-services-storage \
	--filelist .mfiles

%check
set -eo pipefail
JAR=%{buildroot}%{_javadir}/google-api-services-storage.jar
test -f "$JAR"
mkdir -p check
cat > check/Smoke.java << 'EOF'
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.services.storage.Storage;
public class Smoke {
	public static void main(String[] args) throws Exception {
		HttpTransport transport = GoogleNetHttpTransport.newTrustedTransport();
		Storage storage = new Storage.Builder(transport, GsonFactory.getDefaultInstance(), null)
			.setApplicationName("gradle")
			.build();
		String root = storage.getRootUrl();
		if (!"gradle".equals(storage.getApplicationName()) || !"https://storage.googleapis.com/".equals(root)) {
			throw new RuntimeException(storage.getApplicationName() + " " + root);
		}
		System.out.println("gstorage_ok " + storage.getApplicationName() + " " + root);
	}
}
EOF
CP="$JAR:%{_javadir}/google-api-client.jar:%{_javadir}/google-http-client.jar:%{_javadir}/google-http-client-gson.jar:%{_javadir}/google-http-client-apache-v2.jar:%{_javadir}/google-oauth-client.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/gson-2.14.0.jar:%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/commons-logging.jar"
javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d check check/Smoke.java
java -cp "check:$CP" Smoke > check/out.txt
cat check/out.txt
grep -F -q 'gstorage_ok gradle https://storage.googleapis.com/' check/out.txt

%files -f .mfiles
%license LICENSE
%doc README.md
