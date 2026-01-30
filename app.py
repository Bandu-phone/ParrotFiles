import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# CONFIGURACIÓN
GITHUB_TOKEN = "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"
REPO_OWNER = "Bandu-phone"
REPO_NAME = "ParrotFiles"

def get_latest_release_id():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/file"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['id']
    else:
        print("Error: Asegúrate de haber creado al menos una Release en GitHub.")
        return None

@app.route('/')
def index():
    release_id = get_latest_release_id()
    if not release_id:
        return "Error: No se encontró la Release en GitHub."
        
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{release_id}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers).json()
    
    files = response.get('assets', [])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    release_id = get_latest_release_id()
    
    if file and release_id:
        filename = file.filename
        # URL especial para subidas (uploads.github.com)
        upload_url = f"https://uploads.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{release_id}/assets?name={filename}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/octet-stream"
        }
        # Leemos el archivo y lo enviamos
        requests.post(upload_url, headers=headers, data=file.read())
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
