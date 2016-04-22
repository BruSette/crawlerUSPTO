'''
Created on 7 de abr de 2016
@author: bruno
'''
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
         html = urlopen(url)
    except HTTPError as e:
         return None
    try:
         bsObj = BeautifulSoup(html.read(), "html.parser")
         title = bsObj.td
    except AttributeError as e:
        return None
    return title

title = getTitle("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=car&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT")

if title == None:
    print("Title could not be found")
else:
    print(title)