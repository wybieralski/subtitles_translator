from flask import Flask, render_template, request, send_file
import requests
import chardet
import os

app = Flask(__name__)

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = "796d1f09-e4e5-497b-93a1-0dbdad31fe88:fx"  # Wprowadź swój klucz API

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        return result['encoding']

def translate_text(text):
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'source_lang': 'EN',
        'target_lang': 'PL',
    }
    response = requests.post(DEEPL_API_URL, data=params)
    return response.json()['translations'][0]['text']

def translate_file(input_file):
    encoding = detect_encoding(input_file)
    with open(input_file, 'r', encoding=encoding) as f:
        content = f.read()

    translated_content = translate_text(content)

    output_file = 'translated_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)

    return output_file

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            input_file_path = 'uploaded_file.txt'
            file.save(input_file_path)
            output_file_path = translate_file(input_file_path)
            return send_file(output_file_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
