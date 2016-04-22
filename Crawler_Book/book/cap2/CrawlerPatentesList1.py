'''
Created on 19 de abr de 2016

@author: bruno
'''



from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=car&RS=car&Query=car&TD=195492&Srch1=car&NextList1=Next+50+Hits")


bsObj = BeautifulSoup(html, "html5lib")

for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print("http://patft.uspto.gov"+ link.attrs['href'])
        

