'''
Created on 19 de abr de 2016

@author: bruno

ESTE PROGRAMA GERA ARQUIVOS DE SAIDA PARA CADA PATENTE ENCONTRADA NO LINK RELACIONADO
OS ARQUIVOS CONTEM O TITULO DADO A PATENTE PELA USPTO E O LINK DA PATENTE

'''


from urllib.request import urlopen
import os
from bs4 import BeautifulSoup
import json

START_URL = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=facebook&RS=facebook&Query=facebook&TD=7157&Srch1=facebook&NextList1=Next+50+Hits"

def quant_pags():
    html = urlopen(START_URL)
    bsObj = BeautifulSoup(html, "html5lib")
    cont = int(bsObj.findAll("strong")[2].get_text())
    return int(cont / 50 ) + 1


def get_posts_links(i):
    """
    Returns an iterator with the a tags with the titles
    """
    html = urlopen("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=facebook&RS=facebook&Query=facebook&TD=7157&Srch1=facebook&NextList"+str(i)+"=Next+50+Hits")
    soup = BeautifulSoup(html,"html5lib")
    return soup.findAll('a')


def extract_data_from_link(post_link_tag):
    """
    Given a tag object, return it href value and post title
    """
    return {
        'link': "http://patft.uspto.gov" + post_link_tag.attrs['href'],
        'title': post_link_tag.getText(),
    }


def creates_output_file(data, i):
    """
    Creates a json file with data parameter
    """
    file_path = os.path.join(os.path.dirname(__file__), 'out'+str(i)+'.json')
    with open(file_path, 'w') as fp:
        json_data = json.dumps(data)
        fp.write(json_data)



quant_pags = quant_pags()
data = []
for i in range(quant_pags):
    verify = 1
    posts = get_posts_links(i)
    for link in posts:
        if 'href' in link.attrs and 'd=PTXT' in link.attrs['href'] and 'Page=Prev' not in link.attrs['href'] and 'Page=Next' not in link.attrs['href']:
            if verify % 2 == 0:
                post_data = extract_data_from_link(link)
                data.append(post_data)
                creates_output_file(data,i)
                data.clear()
            verify = verify + 1

     
