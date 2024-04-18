from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
UPLOAD_FOLDER = os.getenv('PATH_UPLOAD')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(image_path):
    if image_path is None:
        return "Chemin de fichier non valide"
    
    if os.path.exists(image_path):
        pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT')
        extracted_text = pytesseract.image_to_string(Image.open(image_path))
        return extracted_text
    else:
        return "Le fichier spécifié n'existe pas"




def save_text_to_file(text, filename, username):
    with open(os.path.join(UPLOAD_FOLDER + '/assets/' + username + '' + filename + '.txt'), 'w') as file:
        file.write(text)


@app.route('/upload/<username>', methods=['GET', 'POST'])
def upload_file(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Aucune partie de fichier')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Aucun fichier sélectionné')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            normalized_path = file_path.replace('\\', '/')

            file.save(normalized_path)

            extracted_text = extract_text(normalized_path)
            flash('Fichier téléchargé avec succès')
            return redirect(url_for('uploaded_file', filename=filename, extracted_text=extracted_text))
    return render_template('upload_form.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    extracted_text = request.args.get('extracted_text', '')
    return render_template('uploaded_file.html', filename=filename, extracted_text=extracted_text)


if __name__ == '__main__':
    app.run(debug=True)
