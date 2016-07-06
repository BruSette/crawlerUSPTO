
from urllib.request import urlopen
import os
from bs4 import BeautifulSoup
import json

"""
DEFINE UMA VARIÁVEL INICIAL PARA A URL
"""
START_URL = ("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2"+
            "&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html"+
            "&r=0&f=S&l=50&TERM1=facebook&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT")

def quant_pags():
    """
        FUNÇÃO QUE PEGA VIA CRAWLER A QUANTIDADE DE PÁGINAS A SEREM EXPLORADAS PELO ALGORITMO
    """
    html = urlopen(START_URL)
    bsObj = BeautifulSoup(html, "html5lib")
    """
        A QUANTIDADE DE PÁGINAS ENCONTRA-SE NA SEGUNDA TAG STRONG DO CORPO DO SITE
    """
    cont = int(bsObj.findAll("strong")[2].get_text())
    """
        SOMA-SE MAIS UM À CONTAGEM POIS A ULTIMA PÁGINA DE PATENTES NÃO SERÁ COMPUTADA
    """
    return int(cont / 50 ) + 1


def get_posts_links(i):
    
    html = urlopen("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2"+
                   "&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm"+
                   "&r=0&f=S&l=50&d=PTXT&OS=facebook&RS=facebook&Query=facebook&TD=7220&"+
                   "Srch1=facebook&NextList"+str(i)+"=Next+50+Hits")
    soup = BeautifulSoup(html,"html5lib")
    return soup.findAll('a')


def extract_data_from_link(post_link_tag):
    """
        EXTRAE O LINK DA PATENTE E O TÍTULO RESUMIDO DADA A MESMA
    """
    return {
        'link': "http://patft.uspto.gov" + post_link_tag.attrs['href'],
        'title': post_link_tag.getText(),
    }


def extract_pag_patent(link_patent,patnum):
    html = urlopen("http://patft.uspto.gov" + link_patent.attrs['href'])
    soup = BeautifulSoup(html,"html5lib")
    file_path = os.path.join(os.path.dirname(__file__)+"/saida", patnum+'.html')
    with open(file_path, "w") as fp:
        fp.write(str(soup))


def extract_patnum_from_link(post_link_tag):
    """
        EXTRAE O CÓDIGO DA PATENTE
    """
    return {
        'patnum': post_link_tag.getText()
    }


def creates_output_file(data, i,patnum):
    """
        CRIA UM ARQUIVO JSON DE SAIDA PARA CADA PATENTE ENCONTRADA
    """
    file_path = os.path.join(os.path.dirname(__file__)+"/saida", patnum+'.json')
    with open(file_path, 'w') as fp:
        json_data = json.dumps(data)
        fp.write(json_data)


"""
    MÉTODO PRINCIPAL
"""
quant_pags = quant_pags()
data = []
allLinks = set()
for i in range(quant_pags):
    """
        VARIÁVEL DE VERIFICAÇÃO (IDENTIFICAR SE ESTAMOS NO HREF CONTENTO O TITULO OU O CODIGO DA PATENTE)
    """
    verify = 1
    posts = get_posts_links(i)
    for link in posts:
        """
            ELIMINA LINKS IRRELEVANTES
        """
        if 'href' in link.attrs and 'd=PTXT' in link.attrs['href'] and 'Page=Prev' not in link.attrs['href'] and 'Page=Next' not in link.attrs['href']:
            if verify % 2 == 1:
                post_data = extract_patnum_from_link(link)
                patnum = post_data['patnum']
                data.append(post_data)
                
                
            if verify % 2 == 0:
                post_data = extract_data_from_link(link)
                data.append(post_data)
                creates_output_file(data,i,patnum)
                data.clear()
                extract_pag_patent(link,patnum)
            verify = verify + 1
            
            if link not in allLinks:
                allLinks.add(link)

     
