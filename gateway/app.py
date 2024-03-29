from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv() 
UPLOAD_FOLDER = os.getenv('PATH_UPLOAD')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
variablo = ''
print(UPLOAD_FOLDER)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(image_path):
    # Utiliser pytesseract pour extraire le texte à partir de l'image
    print( os.getenv('TESSERACT'))

    pytesseract.pytesseract.tesseract_cmd =   os.getenv('TESSERACT')
    extracted_text = pytesseract.image_to_string(Image.open(image_path))
    return extracted_text

def save_text_to_file(text, filename,username):
    # Enregistrer le texte dans un fichier texte
    with open(os.path.join(UPLOAD_FOLDER + '/assets/'+ username +''+filename + '.txt'), 'w') as file:
        file.write(text)

@app.route('/upload/<username>', methods=['GET', 'POST'])
def upload_file(username):
    if request.method == 'POST':
        variablo =username
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)
            
            # Extraction du texte à partir de l'image
            print(file_path)
            extracted_text = extract_text(file_path)
            flash('File uploaded successfully')
            return redirect(url_for('uploaded_file', filename=filename, extracted_text=extracted_text))
    else:
        return render_template('upload_form.html')


@app.route('/uploads//<filename>')
def uploaded_file(filename):
    extracted_text = request.args.get('extracted_text', '')
    return render_template('uploaded_file.html', filename=filename, extracted_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
