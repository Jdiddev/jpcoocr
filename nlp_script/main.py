import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json



from sklearn.model_selection import train_test_split


# Chemin vers votre fichier .jsonl
file_path = 'C:\\Users\\yjdid2\\Desktop\\ProjectOCr\\train_data.jsonl'

# Initialiser une liste pour stocker les données
invoice_data = []

# Ouvrir le fichier et lire chaque ligne
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Charger chaque ligne comme un objet JSON et l'ajouter à la liste
        invoice_data.append(json.loads(line))

# Maintenant, `invoice_data` contient une liste d'objets JSON chargés

def get_spacy_doc(file, data):
    nlp = spacy.blank('fr')  # Créer un modèle vide pour la langue française
    db = DocBin()  # Créer un objet DocBin pour stocker les Doc objects

    for entry in tqdm(data):
        text = entry['text']
        annotations = entry.get('label', [])  # Utiliser get pour éviter les erreurs si 'label' n'existe pas
        doc = nlp.make_doc(text)

        ents = []  # Initialiser une liste pour stocker les entités

        for start, end, label in annotations:
            # Créer un span pour chaque entité et l'ajouter à la liste des entités
            span = doc.char_span(start, end, label=label, alignment_mode='strict')
            if span is not None:  # Vérifier si le span est valide
                ents.append(span)
            else:
                # Si le span n'est pas valide, écrire l'erreur dans le fichier
                err_data = f"{[start, end]} {text}\n"
                file.write(err_data)

        # Définir les entités du document
        doc.ents = ents

        # Ajouter le document au DocBin
        db.add(doc)

    return db
    
train , test = train_test_split(invoice_data,test_size=0.3)
len(train)




file = open('error.txt','w')


db = get_spacy_doc(file , train)
db.to_disk('train_data.spacy')


db = get_spacy_doc(file , test)
db.to_disk('test_data.spacy')

file.close()



