# coding: utf-8
import traceback
from toolkit import *
from send import *
import json


def webhook_get(me, token, request):
    choix_dict = build_choix()

    global start_time
    try:
        data = json.loads(request.data.decode())  #recupere le message envoye a notre chatbot
        sender = data['entry'][0]['messaging'][0]['sender']['id']   # Qui nous l a envoye
        depaquet = depaquetage(sender,data,me,ponct_liste)
        type_msg_recu = depaquet[0]
        if type_msg_recu == 'text_msg' :
            type_msg_recu, texte, mots_du_msg=depaquet
            menu, index = download_menu()
            print(menu)
            print(index) # Pour delimiter le passage du diner du midi à celui du soir. Sachant qu'à la cafete c'est toujours 6 items
            if ("menu" in mots_du_msg) and (similitudes(midi_liste,mots_du_msg)!=[]):
                texte ="Menu du midi :"+'\n\n'
                for i in range(index):
                    texte = texte +menu[i][1]+" : " +menu[i][0]+'\n\n'
                payload = send_choix_multiple5(sender,texte,choix_dict)
                send_paquet(token,payload)
                print('Repas midi envoyé')
                return 'nothing'
            elif ("menu" in mots_du_msg) and ("soir" in mots_du_msg):
                texte ="Menu du soir :"+'\n\n'
                for i in range(index,len(menu)-6):
                    texte = texte +menu[i][1]+" : " +menu[i][0]+'\n\n'
                    sender(sender, texte, choix_dict)
            elif similitudes(cafete_liste,mots_du_msg)!=[]:
                texte ="Menu de la cafete :"+'\n'+'\n' +\
                       menu[len(menu)-6][1]+" : " +\
                       menu[len(menu)-6][0]+'\n\n' +\
                       menu[len(menu)-5][1]+" : "+\
                       menu[len(menu)-5][0]+'\n\n'+\
                       menu[len(menu)-4][1]+" : " +\
                       menu[len(menu)-4][0]+'\n\n'+\
                       menu[len(menu)-3][1]+" : " +\
                       menu[len(menu)-3][0]+'\n\n'+\
                       menu[len(menu)-2][1]+" : " +\
                       menu[len(menu)-2][0]+'\n\n'+\
                       menu[len(menu)-1][1]+" : " +\
                       menu[len(menu)-1][0]
                sender(sender,texte,choix_dict)

            elif similitudes(horaire_liste,mots_du_msg)!=[]:
                texte = "RAK :\nLundi au vendredi \n" \
                        "11h30 - 13h15\n19h15 - 20h00\n\n" \
                        "Samedi - Dimanche - Jours fériés \n" \
                        "12h15 - 13h\n19h15 - 20h00\n\n" \
                        "Vacances scolaires \n11h45 - 13h" \
                        "\n19h30 - 20h\n\n" \
                        "BAR :\nLundi au vendredi" \
                        " \n7h30 - 16h45"
                sender(sender, texte, choix_dict)
            elif ("partager" in mots_du_msg):
                sender(sender, texte, choix_dict)
            elif ("menu" in mots_du_msg):
                texte = "Tu veux quel type de menu ? Appuie sur les boutons ci dessous"
                sender(sender, texte, choix_dict)
            else :
                texte = "Je suis là que pour donner le menu ne m'en demandes pas trop! 😉"
                sender(sender, texte, choix_dict)
        else:
            print(type_msg_recu)

    except Exception as e:
                print(traceback.format_exc())
    return "Nothing"
