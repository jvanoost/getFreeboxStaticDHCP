import PySimpleGUI as sg

from utils import *

layout = [
    [
        sg.Button("Se connecter", key="connexion"), 
        sg.Text("Status : ", key="connexionStatus", size=(40, 1))
    ], 
    [
        sg.Text('Enregistrer la liste des baux DHCP fixes sous'),
        sg.InputText('staticDHCP.json', key='NameFileDHCP', size=(20,1), disabled=True), 
        sg.Button("Enregistrer", key='saveDHCP', disabled=True),
        sg.Text("", key="statusGetDHCP", visible=False, size=(3,1))
    ],
    [
        sg.Text('Enregistrer la liste des rediections de ports fixes sous'),
        sg.InputText('portRedirection.json', key='NameFilePorts', size=(20,1), disabled=True), 
        sg.Button("Enregistrer", key='savePorts', disabled=True),
        sg.Text("", key="statusGetPorts", visible=False, size=(3,1))
    ]
]
window = sg.Window(title="My Freebox - Utilitaire de sauvegarde", layout=layout, margins=(100, 50))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    print(event)
    if event == "connexion" :
        s = mksession()
        if s is not False:
            window["connexionStatus"].update("Status : Connecté")
            # On bloque la connexion
            window['connexion'].update(disabled=True)

            # On rend les autres boutons cliquables
            window['saveDHCP'].update(disabled=False)
            window['NameFileDHCP'].update(disabled=False)
            window['savePorts'].update(disabled=False)
            window['NameFilePorts'].update(disabled=False)
        else:
            window["connexionStatus"].update("Status : Erreur authentification")
    elif event == 'saveDHCP':
        # get all Datas from the freebox
        datas = getAllStaticIp(s)

        if datas is not False:
            # save data in a json file
            saveJsonToFile(values['NameFileDHCP'].replace(".json",""), datas)

            window["statusGetDHCP"].update("ok", visible=True, text_color="#00ff00", background_color="#00ff00")
        else:
            window["stausGetDHCP"].update("ko", visible=True, text_color="#ff0000", background_color="#ff0000")
    elif event == sg.WIN_CLOSED:
        break

window.close()
