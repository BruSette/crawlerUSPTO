'''
Created on 19 de abr de 2016

@author: bruno
'''


from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html5lib")
print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"
                    }).parent.previous_sibling.get_text())

