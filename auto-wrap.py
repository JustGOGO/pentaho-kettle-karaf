import os
import re
import sys
import xml.etree.ElementTree as etree
__author__ = 'nbaker'

if __name__ == '__main__':
    tree = etree.parse('/Users/nbaker/Downloads/pdi-ee-2/data-integration/system/karaf/system/pentaho/pentaho-karaf-features/6.1-SNAPSHOT/pentaho-karaf-features-6.1-SNAPSHOT-standard.xml')
    print tree.getroot()

    pattern = re.compile("wrap:mvn:(.*)/(.*)/(.*)")


    bundles = tree.findall('//{http://karaf.apache.org/xmlns/features/v1.0.0}bundle')
    print len(bundles)
    bundles = filter(lambda b: pattern.search(b.text) is not None, bundles)
    print len(bundles)
    for b in bundles:
        match = pattern.match(b.text)
        print match.groups()
        os.chdir("/Users/nbaker/Downloads/pdi-ee-2/data-integration/system/karaf/system/{}/{}/".format(match.group(1).replace(".","/"),match.group(2)))
        os.system("java -jar /Users/nbaker/IdeaProjects/Platform/pentaho-kettle-karaf/bnd.jar wrap /Users/nbaker/Downloads/pdi-ee-2/data-integration/system/karaf/system/{}/{}/{}/{}-{}.jar".format(match.group(1).replace(".","/"),match.group(2),match.group(3),match.group(2),match.group(3)))
        os.system("mv {}-{}.jar /Users/nbaker/Downloads/pdi-ee-2/data-integration/system/karaf/system/{}/{}/{}/".format(match.group(2),match.group(3),match.group(1).replace(".","/"),match.group(2),match.group(3)))