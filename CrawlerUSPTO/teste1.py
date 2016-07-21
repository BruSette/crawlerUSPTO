'''
Created on 19 de jul de 2016

@author: bruno
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=1&f=G&l=50&co1=AND&d=PTXT&s1=facebook&OS=facebook&RS=facebook")
bsObj = BeautifulSoup(html, "html5lib")

for sibling in bsObj.findAll("table").next:
    print(sibling) 