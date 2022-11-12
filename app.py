import csv
import os
from googleapiclient.discovery import build
import webbrowser


print("AniTube V0.1")

youtube = build('youtube','v3',developerKey=youtube_api_key)
lstAnimeName = []
lstAnimeIdVid = []
mainApp = True
options = {
    1: "Importer d'AniList",
    2: "Importer d'un fichier",
    3: "Importer un anime individuel",
    4: "Importer du texte brut",
}

def print_menu():
    for key in options.keys():
        print (key, '--', options[key] )

def fileReader():
    valid = True
    while(valid):
        print("A l'heure actuelle, le choix d'opening n'est pas possible.")
        print("Veuillez bien a mettre le fichier dans le même répertoire que l'application")
        print("Extentions acceptées : CSV, TXT, MD")
        fileName = (input("Ecrivez le nom de votre fichier (avec l'extention) : "))
        extention = fileName.partition(".")[2]
        if extention != "":
            if os.path.isfile(fileName):
                valid = False
            else:
                print("Le fichier n'existe pas")
        else:
            print("Pensez a ajouter l'extention de votre fichier")
    match(extention):
        case "csv":
            print('En CSV, seule la premiere ligne est comptabilisée\n les scores ne sont donc pas comptabilisés')
            with open(fileName) as data:
                fileReader = csv.reader(data)
                for ligne in fileReader:
                    lstAnimeName.append(ligne[0])
            print(lstAnimeName)
    print("Veuillez entrer votre clef Api Youtube (Elle ne sera pqs sauvegardée)")
    print("Pour plus d'informations consultez le lien suivant : https://www.youtube.com/watch?v=MX-4aRdPkqU")
    youtube_api_key = input()
    urlStrList = "http://www.youtube.com/watch_videos?video_ids="
    firstLoop = True
    for video in lstAnimeName:
        request = youtube.search().list(
        part="snippet",
        type='video',
        maxResults=1,
        q=video + " Opening")
        response = request.execute()
        if(firstLoop):
            urlStrList += response['items'][0]['id']['videoId']
        else:
            urlStrList += ","+response['items'][0]['id']['videoId']
    print(urlStrList)
    webbrowser.open(urlStrList)
    link = input('Veuillez copier ci dessous le lien que votre navigateur viens de vous ouvrir')
    link += "&disable_polymer=true"
    webbrowser.open(link)
    print("Vous n'avez plus qu'a cliquer sur les 3 points pour créer votre playlist ;)")
    mainApp = False

while(mainApp):
    print_menu()
    choix = int(input('Entrez le numéro de votre choix :')) 
    if choix == 1:
        print('Actuellement indisponible')
    elif choix == 2:
        fileReader()
    elif choix == 3:
        print('Actuellement indisponible')
    elif choix == 4:
        print('Actuellement indisponible')
    else:
        print('Option invalide')

