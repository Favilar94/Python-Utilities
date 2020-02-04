"""
Set time in the Raspberry with a web page, this code is useful when ntp servers can't be accessed
"""
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


url = "https://www.timeanddate.com/worldclock/timezone/utc" #You can changue this url changing also id=ct and id=ctdat


html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

hora=soup.find(id="ct").contents[0]
fecha=soup.find(id="ctdat").contents[0].split(',')

formato="{}{} {} UTC{}".format(fecha[0], fecha[1], hora, fecha[2])
os.system("sudo date -s '"+formato+"'")

    
