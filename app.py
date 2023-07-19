from flask import Flask, render_template, request, redirect
import csv
import os
import time
import threading

app = Flask(__name__)

@app.route('/')
def home():
    headers = ['Marque', 'Description', 'Liens', 'tags']

    with open('data/data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        tableData = list(reader)

    return render_template(
        'index.html',
        headers=headers,
        tableData=tableData
    )

@app.route('/photos/<marque>')
def get_photos(marque):
    photos_folder = os.path.join('static', 'photos', marque)
    photos = []

    if os.path.exists(photos_folder):
        for filename in os.listdir(photos_folder):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.avif') or filename.endswith('.webp') or filename.endswith('.png'):
                photos.append(os.path.join('photos', marque, filename))

    headers = ['Marque', 'Description', 'Liens', 'tags']

    with open('data/data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        tableData = list(reader)

    return render_template(
        'index.html',
        headers=headers,
        tableData=tableData,
        marque_photos=photos
    )

@app.route('/click_handler', methods=['POST'])
def click_handler():
    marque = request.form['marque']
    marque_formatted = marque.lower().replace(' ', '-')
    return redirect(f'/photos/{marque_formatted}')

def check_photos_folders():
    while True:
        # Lecture des marques depuis le fichier data.csv
        with open('data/data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ignorer la première ligne (en-têtes)
            marques = [row[0] for row in reader]

        # Vérification des dossiers de photos
        for marque in marques:
            marque_formatted = marque.lower().replace(' ', '-')
            photos_folder = os.path.join('static', 'photos', marque_formatted)
            if not os.path.exists(photos_folder):
                os.makedirs(photos_folder)
                print(f"Le dossier des photos pour la marque '{marque}' a été créé.")

        #time.sleep(60 * 60 * 24)  # Attendre 24 heures
        time.sleep(60)
        
if __name__ == '__main__':
    threading.Thread(target=check_photos_folders).start()
    app.run(debug=True)
