# coding: utf-8
import traceback
from toolkit import *
import json


def webhook_get(me, request):
    choix_dict = build_choix()
    try:
        data = json.loads(request.data.decode())  #recupere le message envoye a notre chatbot
        sender = data['entry'][0]['messaging'][0]['sender']['id']   # Qui nous l a envoye
        depaquet = depaquetage(sender,data,me,ponct_liste)
        type_msg_recu = depaquet[0]
        if type_msg_recu == 'text_msg' :
            type_msg_recu, texte, mots_du_msg=depaquet
            menu, index = download_menu()
            #print(menu)
            #print(index) # Pour delimiter le passage du diner du midi à celui du soir. Sachant qu'à la cafete
            # c'est toujours 6 items
            text = construct_text(sender,menu,mots_du_msg, choix_dict, index)
            sender(sender, text, choix_dict)
        else:
            print(type_msg_recu)
    except Exception :
                print(traceback.format_exc())

    return "Nothing"
