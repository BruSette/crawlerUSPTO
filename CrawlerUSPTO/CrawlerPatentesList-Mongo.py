from urllib.request import urlopen
import os
from bs4 import BeautifulSoup
import json
import nltk
from pymongo import MongoClient


"""
DEFINE UMA VARIÁVEL INICIAL PARA A URL
"""
START_URL = ("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2"+
            "&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html"+
            "&r=0&f=S&l=50&TERM1=facebook&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT")

patentesNum = []

client = MongoClient()

db_1 = client.patentes


def quant_pags():
    """
        FUNÇÃO QUE PEGA VIA CRAWLER A QUANTIDADE DE PÁGINAS A SEREM EXPLORADAS PELO ALGORITMO
    """
    html = urlopen(START_URL)
    bsObj = BeautifulSoup(html,"lxml")
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
                   "&r=0&f=S&l=50&d=PTXT&OS=mobile&RS=mobile&Query=mobile&TD=7220&"+
                   "Srch1=mobile&NextList"+str(i)+"=Next+50+Hits")
    soup = BeautifulSoup(html,"lxml")
    return soup.findAll('a')


def extract_data_from_link(post_link_tag):
    """
        EXTRAE O LINK DA PATENTE E O TÍTULO RESUMIDO DADA A MESMA
    """
    return {
        'link': "http://patft.uspto.gov" + post_link_tag.attrs['href'],
        'title': post_link_tag.getText(),
    }

"""
    Gera um arquivo de saida do tipo HTML com os dados pertinentes da respecitiva patente
"""
def extract_pag_patent(link_patent,patnum,mongo):

    html = urlopen("http://patft.uspto.gov" + link_patent.attrs['href'])
    '''soup = BeautifulSoup(html,"html5lib")'''
    '''Caso necessite de tokenização para conversao em NLTK'''
    soup = BeautifulSoup(html,"lxml").getText()
    '''soup = nltk.word_tokenize(soup)'''
    '''Deixa todo o texto em letras misnusculas'''

    soup = str(soup).lower()
    soup = str(soup).replace("\n", "")
    soup = str(soup).replace("\s", " ")

    #extrair aqui o description
    pat = soup[soup.find("description"):soup.find("* * * * *")]
    #print(pat)

    postCol_1 = db_1.uspto


    #inserir aqui os dados no MONGODB
    mongo.update(extract_text(soup))
    mongo.update(extract_description(pat))

    try:
        postCol_1.insert(mongo)
    except Exception as e:
        print("Patente já inserida")
"""
    Retorna o numero da patente passada por parametro
"""
def extract_patnum_from_link(post_link_tag):
    """
        EXTRAE O CÓDIGO DA PATENTE
    """
    return {
        '_id': post_link_tag.getText()
    }

def extract_description(text):

    return {
        'description': str(text)
}

def extract_text(text):

    return {
        'text': str(text)
}

def create_output_file(data, i,patnum):
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
                patnum = post_data['_id']
                mongo = extract_patnum_from_link(link)

            if verify % 2 == 0:
                post_data = extract_data_from_link(link)
                mongo.update(post_data)
                extract_pag_patent(link,patnum,mongo)
            verify = verify + 1

            if link not in allLinks:
                allLinks.add(link)
