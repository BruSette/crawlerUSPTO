'''
Created on 12 de abr de 2016

@author: bruno
'''

'''
Created on 7 de abr de 2016
@author: bruno
'''
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getSpan(url):
    try:
         html = urlopen(url)
    except HTTPError as e:
         return None
    try:
         bsObj = BeautifulSoup(html.read(), "html.parser")
         nameList = bsObj.findAll("span", {"class":"green"})           
    except AttributeError as e:
        return None
    return nameList

nameList = getSpan("http://www.pythonscraping.com/pages/warandpeace.html")

for name in nameList:
    print(name.get_text())
    