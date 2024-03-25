import pytesseract
from PIL import Image

try:
    chemin_image = 'D:\PROJET_PYTHON\AI\cc.jpg'
    image = Image.open(chemin_image)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
    texte = pytesseract.image_to_string(image)  
except IOError as e:
    print(f"Erreur lors de l'ouverture des images: {e}")
    print(f"Erreur lors de l'ouverture des images: {e}")
    print(f"Erreur lors de l'ouverture des images: {e}")
    print(f"Erreur lors de l'ouverture des images: {e}")


    

chemin_sortie = 'D:\\PROJET_PYTHON\\AI\\acture43_output.txt'
with open(chemin_sortie, 'w', encoding='utf-8') as fichier:
    fichier.write(texte)
print("L'extraction du texte a été effectuée avec succès. Le texte a été enregistré dans", chemin_sortie)
