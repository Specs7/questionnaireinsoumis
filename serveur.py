# serveur.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)
CSV_FILE = 'reponses_questionnaire.csv'

def write_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    champs = [
        'gender', 'neighborhood', 'age', 'statut', 'domaines', 'attentes', 'attentes_autre',
        'atelier', 'contact_nom', 'contact_prenom', 'contact_email', 'contact_telephone', 'email'
    ]
    thematiques = data.get('thematiques', {})
    thematiques_flat = {}
    for k, v in thematiques.items():
        thematiques_flat[f"thema_{k}"] = ";".join(v) if isinstance(v, list) else str(v)
    header = champs + list(thematiques_flat.keys())
    row = [str(data.get(champ, "")) if not isinstance(data.get(champ, ""), list) else ";".join(data.get(champ, "")) for champ in champs]
    row += [thematiques_flat[k] for k in thematiques_flat]
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

@app.route('/enregistrer', methods=['POST', 'OPTIONS'])
def enregistrer():
    print("Route /enregistrer appelée avec méthode", request.method)
    if request.method == 'OPTIONS':
        return '', 204
    data = request.get_json()
    write_csv(data)
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# Ne pas mettre app.run(debug=True) sur PythonAnywhere

if __name__ == '__main__':
    app.run(debug=True)