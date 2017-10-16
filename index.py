# coding: utf-8
import os
import requests
import traceback
import json
from flask import Flask, request
from toolkit import *
from send import *
import urllib.request
from bs4 import BeautifulSoup


#TOKEN de prod
token = os.environ.get('FB_ACCESS_TOKEN')
FB_VERIFY_TOKEN = (os.environ.get('FB_VERIFY_TOKEN'))
if token==None:
    #TOKEN de test
    token="EAAFo1IiXrQwBABjWTFk7ZA4XL2kmhFt6M0t0pTjJWSGRppsTWQOYI7Lylcub4899ZBpZBOHz3N4CfvABclqw7ZA5CNZB1JtfhtFEVShC8KP3ZB3GLqmc5RLtnBX3WGl1aMM0zYvm6DAxIvCeOXem1YsFqpcVsrp1pZAzpkeF0QeCAZDZD"

if FB_VERIFY_TOKEN==None:
    FB_VERIFY_TOKEN = "test_token"

me = "1437816462930392"

app = Flask("app")  #instance de la classe FLask. premier argument est le nom
choix1 = "Menu midi"
choix2 = "Menu soir"
choix3 = "Cafete"
choix4 = "Horaires"

print('     /$$$$$$$$\                  /$$   $$    ')
print('    | $$    |$$                 | $$  $$     ')
print('    | $$    | $$    /$$$$$$$    | $$ $$      ')
print('    | $$$$$$$$$$   |_______$$   | $$$$       ')
print('    | $$    \ $$    /$$$$$$$$   | $$ $$      ')
print('    | $$     \ $$  |$$__   $$   | $$  $$     ')
print('    | $$      \ $$ | $$$$$$$$   | $$ \ $$    ')
print('    |__/       \_/  \_______/   |__/  |_/    ')

@app.route('/', methods=['GET', 'POST']) #A decorator that is used to register a view function for a given URL rule.Ici rule = / et en option les methodes assignées à ce rule
def webhook():
    global start_time
    if request.method == 'POST':  # Toutes les requetes post passent par la ; dans les deux sens
        try:
            data = json.loads(request.data.decode())  #recupere le message envoye a notre chatbot
            sender = data['entry'][0]['messaging'][0]['sender']['id']   # Qui nous l a envoye
            depaquet = depaquetage(sender,data,me,ponct_liste)
            print(depaquet)
            type_msg_recu = depaquet[0]
            if type_msg_recu == 'text_msg' :
                type_msg_recu, texte, mots_du_msg=depaquet
                menu=download_menu()
                print(len(menu))
                if ("menu" in mots_du_msg) and (similitudes(midi_liste,mots_du_msg)!=[]):
                    texte ="Menu du midi :"+'\n'+'\n' +menu[0][1]+" : " +menu[0][0]+'\n\n' +menu[1][1]+" : "+ menu[1][0]+'\n\n'+menu[2][1]+" : " + menu[2][0]+'\n\n'+menu[3][1]+" : "+ menu[3][0]+'\n\n'+menu[4][1] +" : "+ menu[4][0]+'\n\n'+menu[5][1]+" : "+ menu[5][0]+'\n\n'+menu[6][1]+" : "+ menu[6][0]
                    payload = send_choix_multiple4(sender,texte,choix1,choix2,choix3,choix4)
                    send_paquet(token,payload)
                    print('Repas midi envoyé')
                    return 'nothing'
                elif ("menu" in mots_du_msg) and ("soir" in mots_du_msg):
                    texte ="Menu du soir :"+'\n'+'\n'+menu[7][1]+" : " +menu[7][0]+'\n\n' +menu[8][1]+" : "+ menu[8][0]+'\n\n'+menu[9][1]+" : " + menu[9][0]+'\n\n'+menu[10][1]+" : " + menu[10][0]
                    payload = send_choix_multiple4(sender,texte,choix1,choix2,choix3,choix4)
                    send_paquet(token,payload)
                    print('Repas soir envoyé')
                    return 'nothing'
                elif similitudes(cafete_liste,mots_du_msg)!=[]:
                    texte ="Menu de la cafete :"+'\n'+'\n' +menu[11][1]+" : " +menu[11][0]+'\n\n' +menu[12][1]+" : "+ menu[12][0]+'\n\n'+menu[13][1]+" : " + menu[13][0]+'\n\n'+menu[14][1]+" : " + menu[14][0]+'\n\n'+menu[15][1]+" : " + menu[15][0]+'\n\n'+menu[16][1]+" : " + menu[16][0]
                    payload = send_choix_multiple4(sender,texte,choix1,choix2,choix3,choix4)
                    send_paquet(token,payload)
                    print('Repas soir envoyé')
                    return 'nothing'
                elif similitudes(horaire_liste,mots_du_msg)!=[]:
                    texte = "RAK :\nLundi au vendredi \n11h30 - 13h15\n19h15 - 20h00\n\nSamedi - Dimanche - Jours fériés \n12h15 - 13h\n19h15 - 20h00\n\nVacances scolaires \n11h45 - 13h\n19h30 - 20h\n\nBAR :\n Lundi au vendredi \n7h30 - 16h45" 
                    payload = send_choix_multiple4(sender,texte,choix1,choix2,choix3,choix4)
                    send_paquet(token,payload)
                    print('Demande du type de menu')
                    return 'nothing'
                elif ("partager" in mots_du_msg):
                    payload = send_share(sender)                    
                    send_paquet(token,payload)
                    print('Demande de partage')
                    return 'nothing'
                elif ("menu" in mots_du_msg):
                    texte = "Tu veux quel type de menu ? Appuie sur les boutons ci dessous" 
                    payload = send_choix_multiple4(sender,texte,choix1,choix2,choix3,choix4)
                    send_paquet(token,payload)
                    print('Demande du type de menu')
                    return 'nothing'
                elif ("white" in mots_du_msg):
                    payload = whitelist()
                    send_paquet(token,payload)
                    print('Whitelist demandé')
                    return 'nothing'
                else :
                    texte = "Je suis là que pour donner le menu ne m'en demandes pas trop! 😉"
                    payload = send_choix_multiple4(sender,texte,choix1,choix2,choix3,choix4)
                    send_paquet(token,payload)
                    print('Message - Pas compris')
                    return 'nothing'
            else:
                print(data)

        except Exception as e:
                    print(traceback.format_exc())
    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == FB_VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"

ponct_liste = ['.',',','!','?',';',':'] 
midi_liste = ["midi","dejeuner","déjeuner","dejeune"]
cafete_liste = ["cafete","cafeteriat","cafetariat","bar","cafet"]
horaire_liste = ["horaire","horaires"]

#DOWNLOAD MENU
def download_menu():
    req = urllib.request.Request('http://services.telecom-bretagne.eu/rak/')
    the_page = urllib.request.urlopen(req)
    page = the_page.read()
    soup = BeautifulSoup(page, 'html.parser')
    plats = soup.find_all("td", attrs={"class" : "col-md-4"})
    nom_plats = soup.find_all("td", attrs={"align" : "left"})
    result = []
    for i in range(len(plats)):
        a = str(plats[i].getText())
        b = str(nom_plats[i].getText())
        result.append([a[1:-1],b[2:-2]])
    return result

# ENVOYER UN PAYLOAD
def send_paquet(sender,payload):
    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
    print(r.text) # affiche la reponse à l'envoit; pratique si veut l'ID ou voir si bien envoyé
    pass

def whitelist():
    payload = {
    "setting_type" : "domain_whitelisting",
    "whitelisted_domains":[
    "https://m.me/pyrakk"
    ],
    "domain_action_type": "add"
    }
    return payload 

# CONFIGURATION DE LA PAGE HAL
def reglage_menu():
    payload = {
    "persistent_menu":[
    {
      "locale":"default",
      "call_to_actions":[
        {
          "type":"postback",
          "title":"Menu",
          "payload":"menu"
        },
        {
          "title":"Actualités",
          "type":"nested",
          "call_to_actions":[
            {
              "title":"A la une",
              "type":"postback",
              "payload":"actuune"
            },
            {
              "title":"Actu Monde",
              "type":"postback",
              "payload":"actumonde"
            },
            {
              "title":"Actu Sport",
              "type":"postback",
              "payload":"actusport"
            }
          ]
        },
        {
          "type":"postback",
          "title":"Fais croquer !",
          "payload":"partage"
        }
      ]
    },
    {
      "locale":"zh_CN",
      "composer_input_disabled":"false"
    }
  ]
 }
    return payload
def get_started():
    payload = { 
  "get_started":{
    "payload":"salut"
  }
 }
    return payload
def description():
    payload = {
  "greeting":[
    {
      "locale":"default",
      "text":"Salut {{user_first_name}}, commençons à discuter !"
    }, {
      "locale":"en_US",
      "text":"Hi {{user_first_name}}, let's start!"
    }
  ] 
 }
    return payload

if __name__ == '__main__':
    app.run(debug=True) #Runs the application on a local development server. / If the debug flag is set the server will automatically reload for code changes 