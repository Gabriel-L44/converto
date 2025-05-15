from flask import Flask, request, render_template, send_file
import os
import subprocess
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    output_format = request.form['conversion']

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    filename_wo_ext = os.path.splitext(file.filename)[0]
    output_path = os.path.join(CONVERTED_FOLDER, f"{filename_wo_ext}.{output_format}")

    try:
        if output_format == 'mp3':
            subprocess.run(['ffmpeg', '-i', input_path, output_path], check=True)
        elif output_format in ['png', 'jpg']:
            img = Image.open(input_path)
            img.save(output_path, output_format.upper())
        elif output_format == 'pdf':
            img = Image.open(input_path)
            img.convert('RGB').save(output_path, 'PDF')
        else:
            return 'Format non supporté', 400

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"Erreur lors de la conversion : {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
