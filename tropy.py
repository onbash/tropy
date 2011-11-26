## -*- coding: UTF-8 -*-
#tropy -detailed traceroute
#usage: python tropy.py google.com
import os,sys
import re
import urllib
import subprocess
from geopy import geocoders
if os.name=="nt":
	pass
else:
	from termcolor import colored

g=geocoders.Google()
point=0 
host = sys.argv[1]

if os.name=="nt":
	command="tracert"
else:
	command="traceroute"

p = subprocess.Popen([command, host], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True:
    line = p.stdout.readline()
    ip = re.findall("(?:\d{1,3}\.){3}\d{1,3}",line)  ## match IP address
    if ip!=[]:
        #response = urllib.urlopen('http://www.dnsstuff.com/tools/whois/?ip==%s' % ip[0]).read()
        #response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s' % ip[0]).read()
        response = urllib.urlopen('http://ipmap.com/%s' % ip[0]).read()
             
        m = re.search('City:</b></td>\s+<td>(.*)&nbsp', response)
        try:
            city,coordinates=g.geocode(m.group(1))
            
        except:
            coordinates=(0.0,0.0)
            city="Unknown"
        
        try:
           print colored("%d","red")%point," Ip: ",colored("%s","green")% ip[0]," | City-Country:",colored("%s","yellow")%city,"| Lat:",colored(" %0.3f","cyan") % coordinates[0],"Lng:",colored("%0.3f","cyan")%coordinates[1]
        except:
           print point," Ip: ", ip[0]," | City-Country:",city," | Lat: %0.3f  Lng: %0.3f" % (coordinates[0],coordinates[1])

        print "------------------------------------------------------------------------------------------------"
        point+=1
  
    
    if not line: break
p.wait()

