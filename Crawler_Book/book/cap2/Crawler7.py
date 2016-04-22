'''
Created on 19 de abr de 2016

@author: bruno
'''

from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re
    
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html,"html5lib")
images = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})
for image in images:
    print(image["src"])