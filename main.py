import smtplib
import ssl
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import uuid  # Importe le module uuid
import urllib.parse #Pour encoder les url
import logging

## les import les piece jointe 
from email.mime.base import MIMEBase # pr les piece jointe 
from email.mime.application import MIMEApplication # pr les pdf 
from email.encoders import encode_base64# aussi important , c pr encoder ( à voir pk ) 



fichier = 'mailtrack.csv'

##ssl c'est pour la securité

serveur_smtp = 'smtp.gmail.com'
port_smtp = 465

# info sur l email utilisé
expediteur = 'aravindan.compte3@gmail.com'
##mdp2 = '3b6pke2zA.232'

##pr le 3
mdp = 'fxvg jouq rmqq klsd'

# ##pr le mien
# mdp = 'afau bojf gyns fjlb'
# dst = 'aravindan.compte@gmail.com'
dst = ' arivarasi.detchanamourtty@gmail.com'
# msg = """Subject: Test Gmail avec smtplib

# Ceci est un message de test envoye via Gmail avec smtplib.
# """


contexte = ssl.create_default_context()

contact=[]
## ca va prendre les elm de chaqu collone , pr nos variable
try :
    with open(fichier,'r',encoding='utf-8') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv)
        next(lecteur_csv)  # Cette ligne permet de sauter la première ligne
    ##c pr sauter la 1er ligne
        for i in lecteur_csv:
            contact.append(i)
            # print(i)
            # print("\n")


except FileNotFoundError:
    print("fichier non trouvé , verifié son emplacement/nom")

except Exception as e :
    print(f" y a une erreur inatentu : {e}")


try:
    with smtplib.SMTP_SSL(serveur_smtp,port_smtp,context=contexte) as server:
        server.login(expediteur,mdp)

        for i in contact:
            # nom = i['nom']
            # prenom= i['prenom']
            # email = i['email']
            # sx = i['sexe']
            ## on peut pas ici car c pas un dico mais une lst , dc on doit acceder avc

            prenom = i[0]
            nom = i[1]
            sx = i[2]
            email = i[3]
            logging.info(f"Tracking EMAIL : {email}")


            #Générer identifiant unique
            tracking_id = str(uuid.uuid4())
            logging.info(f"Tracking ID généré : {tracking_id}")


            ## on creer le msg via MIME
            message = MIMEMultipart('alternative')
            # c'est un mot clée obligatoir, qui specifie ceux qu'on va use , alternative -> pr txt brut et html
            message['From'] = expediteur    # Correct
            message['To'] = email
            message['Subject'] = "Candidature de stage"  # Correct

            #cas txt brut
            # une approche avc jinja2 , c'est un peu pareille que avc les f , mais askip c mieux jinja2
            text_template = Environment(autoescape=True).from_string("""
            Bonjour {{sx}} {{nom}} {{prenom}},
            J'espère que ce message vous trouve bien.
            voici un petit message de test.

            Cordialement,
            Aravindan""")

            msg = text_template.render(sx=sx, nom=nom, prenom=prenom)

            #Chargement du template et insertion des variables
            env = Environment(loader=FileSystemLoader('mail-tracker propre'))
            html_template = env.get_template('html-model.html')
            html_final = html_template.render(sx=sx, nom=nom, prenom=prenom,tracking_id=tracking_id) #inserer les variables du html
            logging.info(f"Tracking ID généré : {tracking_id}")

            ## ou  html_final = html_template.render(sx=sx, nom=nom, prenom=prenom,email=email)  si on veut utiliser l'email comme ID, et il faut aussi modifier le html model en conséquence

            # mtn on envoie la piece jointe
            try :
                with open('CV 7 aravindan detchanamourtty.pdf','rb') as f :
                    piece_jointe = MIMEApplication(f.read(),_subtype='pdf')# ici on fait une photocpie de notre pdf 'f' , pn le met ds une envleoppe speciale MIMEAPP.. avc l'etiquette subtype
                    piece_jointe.add_header('Content-Disposition','attachment',filename='CV 7 aravindan detchanamourtty.pdf')
                    # le file name renomme le fichier pdf lors de l'nevoi ( renomation est que sur le fichier recu par client )
                   ## les mot clée contant-disposition, attachment, filename, sont des mot clé obligatoir/par defaut
                   #ca dit comment le use , le presenter ,                     # c pr dire que c une piece jointe
                    message.attach(piece_jointe)

            except FileNotFoundError :
                print(" fichier introuvable ")
            except Exception as e :
                print(f" une erreur intauentud lors de la piece jointe : {e}")

            # Donner les var au template
            #html_final = html_template.render(sx=sx, nom=nom, prenom=prenom) #Devenu inutile car on a besoin d'envoyer le tracking ID

            # Attacher les deux versions
            part1 = MIMEText(msg,'plain')
            part2 = MIMEText(html_final,'html')
            message.attach(part1)
            message.attach(part2)

            server.sendmail(expediteur, email, message.as_string())
            print(f" email envoyé avc succé pour le mail : {email}")
            ##time.sleep(0.1)
        server.quit()  # Ajout de server.quit()



except Exception as e :
    print(f" y a une erreur lors de l'nvoie : {e}")
print(" tout est terminé ")
