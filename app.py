import mimetypes
from flask import Flask, request , send_file
# flask c le framework web pr gerer le server 
# request , pr gerer les requette 
# send_file pr envoyer le fichier ( comme le pixel.png ) 
import logging
import time
# logging pr enregistrer les evenemnts 

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

# on creer une route pr servir le pixel de tracking
@app.route("/pixel.png")
# le @ c comme un decoarateur , une etiquette , 
#ici on dit si on accede dans le chemin pixl.png , on execute la f pixel() 
def pixel():
    # on recupere l'adresse mail de l'utilisateur
    email = request.args.get("email")
    #on save l'ouverture dans le log 
    if email : 
        logging.info(f"le pixel tracked pr id : {email}")
    # on enregistre l'ouverture de l email dans un ficher autre 
        try : 
            with open ("save trace email.txt", "a" , encoding="utf-8") as f : 
                curent_time = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f" {curent_time} -email ouvert par : {email} \n")
        except Exception as e : 
            logging.error(f"erreur lors du save dans le fihcier , : {e}")
    
    # là on renvoi le pixel de tracking 
    return send_file("pixel.png" , mimetype='image/png')

## là on va verifier si le server marche bien avc un msg smimple 

@app.route("/")
## pareille mais ici c'est dès l'entrée principale du server 
def msg():
    return "server de tracking online , ok !"

if __name__ == "__main__":
    app.run(debug=False)
   # false c pr la production , y a pas tt les details , le juste necessaire 
    #true c plus detaille , server qui change à chq modif , etc ( pas optimale pour la podution , pr donné au clienst ) 
    
# ## ATTENTION , ok le code est bon 
# MAIS , ici le framework choisi , le server est de type flask , pr mo =n usage c'est ok 
# mais dans le cas ou je le deploie / donne pur d'autre prsn , mieux vaut enivsager d'utiliser un sever plus robuste ( - Gunicorn
# - uWSGI
# - Waitress
