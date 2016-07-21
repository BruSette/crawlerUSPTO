'''
Created on 19 de jul de 2016

@author: bruno
'''

from nltk import *

def lexical_diversity(text):
    return len(text) / len(set(text))

def percentage(count,total):
    return 100 * count / total



arquivo = open("saida/patentes.txt","r")

for linha in arquivo:
    linha = arquivo.readline()
    if('\n' in linha):    
        linha = linha.rstrip('\n')
    print(str(linha))
    if(str(linha) != ""):
        arquivopat = open("saida/"+str(linha)+'.html',"r")
        pat = arquivopat.readlines()
        pat = str(pat)
        print(pat.count("html"))
    