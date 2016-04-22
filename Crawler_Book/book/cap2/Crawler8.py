'''
Created on 19 de abr de 2016

@author: bruno
'''


from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html, "html5lib")
for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])
        
