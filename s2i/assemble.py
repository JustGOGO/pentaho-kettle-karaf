import os
import re
import sys

__author__ = 'nbaker'

stable = "5.2.0.0-R"
active = "origin/master"

if __name__ == '__main__':

    # cfg_path = "/home/nbaker/Repos/pentaho-kettle-karaf/test/extra-features.py"
    cfg_path = sys.argv[1] + "/extra-features.py"

    if os.path.isfile(cfg_path):
        options = {}
        execfile(cfg_path, options)

    template = """
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

	<modelVersion>4.0.0</modelVersion>

	<groupId>pentaho</groupId>
	<artifactId>pentaho-kettle-assembly</artifactId>
	<version>1.0-SNAPSHOT</version>
	<packaging>karaf-assembly</packaging>

	<dependencies>
		<dependency>
			<!-- scope is compile so all features (there is only one) are installed into startup.properties and the feature repo itself is not added in etc/org.apache.karaf.features.cfg file -->
			<groupId>org.apache.karaf.features</groupId>
			<artifactId>framework</artifactId>
			<version>4.0.3</version>
			<type>kar</type>
		</dependency>
		<dependency>
			<!-- scope is runtime so the feature repo is listed in etc/org.apache.karaf.features.cfg file, and features will installed into the system directory if specify in the plugin configuration -->
			<groupId>org.apache.karaf.features</groupId>
			<artifactId>standard</artifactId>
			<classifier>features</classifier>
			<version>4.0.3</version>
			<type>xml</type>
			<scope>runtime</scope>
		</dependency>


		<dependency>
			<!-- scope is runtime so the feature repo is listed in etc/org.apache.karaf.features.cfg file, and features will installed into the system directory if specify in the plugin configuration -->
			<groupId>org.apache.karaf.features</groupId>
			<artifactId>spring</artifactId>
			<classifier>features</classifier>
			<version>4.0.3</version>
			<type>xml</type>
			<scope>runtime</scope>
		</dependency>
		<dependency>
			<!-- scope is runtime so the feature repo is listed in etc/org.apache.karaf.features.cfg file, and features will installed into the system directory if specify in the plugin configuration -->
			<groupId>org.apache.karaf.features</groupId>
			<artifactId>enterprise</artifactId>
			<classifier>features</classifier>
			<version>4.0.3</version>
			<type>xml</type>
			<scope>runtime</scope>
		</dependency>
		"""
    for repo in options["repositories"]:
        # mvn:pentaho/pentaho-kettle-feature/6.1-SNAPSHOT/xml/features
        pattern = re.compile("mvn:(.*)/(.*)/(.*)/(.*)/(.*)");
        match = pattern.match(repo)

        template += """
        <dependency>
			<groupId>{}</groupId>
			<artifactId>{}</artifactId>
			<version>{}</version>
			<type>{}</type>
			<classifier>{}</classifier>
			<scope>runtime</scope>
		</dependency>
        """.format(match.group(1),match.group(2),match.group(3),match.group(4),match.group(5))

    template += """
	</dependencies>

	<build>
		<!-- if you want to include resources in the distribution -->
		<resources>
			<resource>
				<directory>src/main/resources</directory>
				<filtering>false</filtering>
				<includes>
					<include>**/*</include>
				</includes>
			</resource>
			<resource>
				<directory>src/main/filtered-resources</directory>
				<filtering>true</filtering>
				<includes>
					<include>**/*</include>
				</includes>
			</resource>
		</resources>

		<plugins>
			<!-- if you want to include resources in the distribution -->
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-resources-plugin</artifactId>
				<version>2.6</version>
				<executions>
					<execution>
						<id>process-resources</id>
						<goals>
							<goal>resources</goal>
						</goals>
					</execution>
				</executions>
			</plugin>
			<plugin>
				<groupId>org.apache.karaf.tooling</groupId>
				<artifactId>karaf-maven-plugin</artifactId>
				<version>4.0.7</version>
				<extensions>true</extensions>
				<configuration>
					<!-- no startupFeatures -->
					<bootFeatures>
						<feature>bundle</feature>
						<feature>config</feature>
						<feature>wrap</feature>
						<feature>aries-blueprint</feature>
						<feature>diagnostic</feature>
						<feature>deployer</feature>
						<feature>feature</feature>
						<feature>instance</feature>
						<feature>jaas</feature>
						<feature>kar</feature>
						<feature>log</feature>
						<feature>management</feature>
						<feature>package</feature>
						<feature>service</feature>
						<feature>shell</feature>
						<feature>shell-compat</feature>
						<feature>ssh</feature>
						<feature>system</feature>
	"""
    for feature in options["extra_features"]:
        template += "				<feature>{}</feature>\n".format(feature)
    template += """
					</bootFeatures>
					<installedFeatures>
	"""
    for feature in options["features"]:
        template += "				<feature>{}</feature>\n".format(feature)
    template += """
					</installedFeatures>
				</configuration>
			</plugin>
		</plugins>
	</build>
</project>
"""
    print template