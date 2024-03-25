import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json

import os
import requests
import pdfplumber

with pdfplumber.open('testfact.pdf') as pdf:
    page = pdf.pages[0]
    text = page.extract_text()


nlp = spacy.load('C:/Users/yjdid2/Desktop/ProjectOCr/output/model-best')
chemin_fichier = 'C:/Users/yjdid2/Desktop/textocr.txt'

try:
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        text = fichier.read()
        
except FileNotFoundError:
    print(f"Le fichier {chemin_fichier} n'a pas été trouvé.")
except IOError:
    print("Une erreur est survenue lors de la lecture du fichier.")
doc  = nlp(text)
for ent in doc.ents:
    print(ent.text , "   ->>>>>>>>>" , ent.label_ , "\n\n\n")
