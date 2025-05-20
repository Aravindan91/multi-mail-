import email
import mimetypes
from flask import Flask, request , send_file
# flask c le framework web pr gerer le server 
# request , pr gerer les requette 
# send_file pr envoyer le fichier ( comme le pixel.png ) 
import logging
import time
import os 
# logging pr enregistrer les evenemnts 
import csv  # Ajoutez cet import en haut du fichier

app = Flask(__name__)         
## on vient de creer une sintance de flash , un gateau du moule                           

#Pour la suite, nous devrons ajouter :
# 1. Une route pour servir le pixel de tracking
# 2. Une fonction pour enregistrer les ouvertures d'emails
# 3. La configuration du logging

# on config le loging pr voir les requette 
# c comme si on cinf un carnet de note des requette 
# logging.basicConfig , on prepare le carnet de note , avec : 
#INFO : les info importante 
# %(asctime)s : date et heure de la requette
#levelsname , le type , le niv d'importance 
# et enfin message , , le contenun du note 
# on aura un truc du genre : 
# 2024-01-20 14:30:45-INFO - Email ouvert par utilisateur@email.com
logging.basicConfig(level=logging.INFO, format = '%(asctime)s-%(levelname)s - %(message)s')

TRACE_FILE = os.path.join(os.path.dirname(__file__), "save_trace_email.txt")
PIXEL_FILE = os.path.join(os.path.dirname(__file__), "pixel.png")

# on creer une route pr servir le pixel de tracking
@app.route("/pixel.png")
# le @ c comme un decoarateur , une etiquette , 
#ici on dit si on accede dans le chemin pixl.png , on execute la f pixel() 

def pixel():
    email = request.args.get("email")
    if not email:
        logging.warning("Tentative de tracking sans email")
        return send_file(PIXEL_FILE, mimetype='image/png')
    
    if email:
        logging.info(f"le pixel tracked pr id : {email}")
        
    
    # Recherche des informations dans le CSV
    nom = "Inconnu"
    prenom = "Inconnu"
    try:
        with open('mailtrack.csv', 'r', encoding='utf-8') as f:
            lecteur_csv = csv.reader(f)
            next(lecteur_csv)  # Sauter l'en-tête
            for ligne in lecteur_csv:
                logging.info(f"Lecture ligne : {ligne}")
                if ligne[3] == email:  # L'email est dans la 4ème colonne
                    prenom = ligne[0]
                    nom = ligne[1]
                    trouve = True
                    break
            if not trouve:
                logging.warning(f"Email {email} non trouvé dans le CSV")



        
        # Enregistrement avec les informations complètes
        with open(TRACE_FILE, "a", encoding="utf-8") as f:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f" {current_time} - {prenom} {nom} ({email}) a ouvert l'email\n")
            logging.info(f"{current_time} - {prenom} {nom} ({email}) a ouvert l'email")
            #logging.info(f"Enregistrement réussi pour : {prenom} {nom} ({email})")
    except Exception as e:
        logging.error(f"Erreur lors du traitement : {e}")
        return "Erreur lors du tracking", 500

    return send_file(PIXEL_FILE, mimetype='image/png')


@app.route("/")
def msg():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        if not os.path.exists(TRACE_FILE):
            return "Serveur de tracking en ligne ! Aucun email n'a encore été ouvert."

        with open(TRACE_FILE, "r", encoding="utf-8") as f:
            emails_ouverts = f.readlines()  # ✅ lit toutes les lignes dans une liste

        if emails_ouverts:
            mssg = "Voici les personnes qui ont ouvert le mail :\n\n"
            for line in emails_ouverts:
                mssg += line  # ✅ ajoute chaque ligne (pas chaque lettre !)
        else:
            mssg = "Aucun mail n'a encore été ouvert."

        return f"Serveur de tracking online ✅\n\n{mssg}"

    except Exception as e:
        logging.error(f"Erreur lors de l'ouverture du fichier : {e}")
        return "Erreur lors de la lecture du fichier de tracking."


## là on va verifier si le server marche bien avc un msg smimple 





if __name__ == "__main__":
    app.run(debug=False)
   # false c pr la production , y a pas tt les details , le juste necessaire 
    #true c plus detaille , server qui change à chq modif , etc ( pas optimale pour la podution , pr donné au clienst ) 
    
# ## ATTENTION , ok le code est bon 
# MAIS , ici le framework choisi , le server est de type flask , pr mo =n usage c'est ok 
# mais dans le cas ou je le deploie / donne pur d'autre prsn , mieux vaut enivsager d'utiliser un sever plus robuste ( - Gunicorn
# - uWSGI
# - Waitress
