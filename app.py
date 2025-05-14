import email
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
@app.route("/pixel.png")
def pixel():
    email = request.args.get("email")
    if email:
        logging.info(f"le pixel tracked pr id : {email}")
        try:
            with open("d:/code/mail tracker/mail-tracker propre/save trace email.txt", "a", encoding="utf-8") as f:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f" {current_time} -email ouvert par : {email} \n")
                logging.info(f"Enregistrement réussi pour : {email}")  # Ajout d'un log de confirmation
        except Exception as e:
            logging.error(f"erreur lors du save dans le fichier : {e}")
            return "Erreur lors du tracking", 500  # Ajout d'une réponse d'erreur
    
    return send_file("pixel.png", mimetype='image/png')

## là on va verifier si le server marche bien avc un msg smimple 

@app.route("/")
def msg():
    curent_time = time.strftime("%Y-%m-%d %H:%M:%S") 

    try : 
        # Vérifie si le fichier existe
        if not os.path.exists(chemin_fichier):
            return "Serveur de tracking en ligne ! \nAucun email n'a encore été ouvert."

            
        with open("d:/code/mail tracker/mail-tracker propre/save trace email.txt","r",encoding="utf-8") as f :
            emails_ouverts= f.readline()
        if emails_ouverts :
            mssg ="voici les diff prsn qui ont ouvert le mail : \n"
            for i in emails_ouverts :
                mssg += i
                ##mssg += f"{i} à {curent_time} \n"
        else : 
            mssg = " aucun mail a été ouvert "

        return f"server tracker online \n {mssg}"

    except Exception as e : 
        logging.error(f" erreur lors de l'oiverture du fichier : {e}")    
        return "server de tracking online , ok ! "






if __name__ == "__main__":
    app.run(debug=False)
   # false c pr la production , y a pas tt les details , le juste necessaire 
    #true c plus detaille , server qui change à chq modif , etc ( pas optimale pour la podution , pr donné au clienst ) 
    
# ## ATTENTION , ok le code est bon 
# MAIS , ici le framework choisi , le server est de type flask , pr mo =n usage c'est ok 
# mais dans le cas ou je le deploie / donne pur d'autre prsn , mieux vaut enivsager d'utiliser un sever plus robuste ( - Gunicorn
# - uWSGI
# - Waitress
