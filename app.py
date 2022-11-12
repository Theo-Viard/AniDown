import csv
import os
from googleapiclient.discovery import build
import webbrowser
import requests

print("AniTube V0.1")

lstAnimeName = []
lstAnimeIdVid = []
mainApp = True
options = {
    1: "Importer d'AniList",
    2: "Importer d'un fichier",
    3: "Importer un anime individuel",
    4: "Importer du texte brut",
    5: "Fusionner 2 playlists"
}


def print_menu():
    for key in options.keys():
        print(key, '--', options[key])

def addPlaylist():
    print("Veuillez entrer votre clef Api Youtube (Elle ne sera pqs sauvegardée)")
    print("Pour plus d'informations consultez le lien suivant : https://www.youtube.com/watch?v=MX-4aRdPkqU")
    youtube_api_key = input()
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    urlStrList = "http://www.youtube.com/watch_videos?video_ids="
    firstLoop = True
    lstAnimeNameRest = lstAnimeName
    print(lstAnimeNameRest)
    for video in lstAnimeName:
        request = youtube.search().list(
            part="snippet",
            type='video',
            maxResults=1,
            q=video + " Opening")
        try:
            response = request.execute()
            if (firstLoop):
                urlStrList += response['items'][0]['id']['videoId']
                firstLoop = False
            else:
                urlStrList += ","+response['items'][0]['id']['videoId']
            lstAnimeNameRest.pop(0)
        except:
            print('Vous avez dépassé le quota quotidien possible de requette youtube')
            print('Un fichier csv avec les animes non ajoutés a été créé dans le répertoire courant.')
            print('Nous vous conseillons de réésayer demain avec le CSV créé (vous avez la possiblité de fusionner des playlists si besoin')
            if os.path.isfile('animeListNonUpload.csv'):
                os.remove('animeListNonUpload.csv')
            fp = open('animeListNonUpload.csv', 'x')
            fp.close()
            with open('animeListNonUpload.csv', 'w',encoding="utf-8",newline='') as file:
                writer = csv.writer(file)
                for anime in lstAnimeNameRest:
                    writer.writerow([anime])
            break
    print(urlStrList)
    webbrowser.open(urlStrList)
    link = input(
        'Veuillez copier ci dessous le lien que votre navigateur viens de vous ouvrir : ')
    link += "&disable_polymer=true"
    webbrowser.open(link)
    print("Vous n'avez plus qu'a cliquer sur les 3 points pour créer votre playlist ;)")
    mainApp = False

def fileReader():
    valid = True
    while (valid):
        print("A l'heure actuelle, le choix d'opening n'est pas possible.")
        print("Veuillez bien a mettre le fichier dans le même répertoire que l'application")
        print("Extention acceptée : CSV")
        fileName = (
            input("Ecrivez le nom de votre fichier (avec l'extention) : "))
        extention = fileName.partition(".")[2]
        if extention != "":
            if os.path.isfile(fileName):
                valid = False
            else:
                print("Le fichier n'existe pas")
        else:
            print("Pensez a ajouter l'extention de votre fichier")
        with open(fileName) as data:
            fileReader = csv.reader(data)
            for ligne in fileReader:
                lstAnimeName.append(ligne[0])
        addPlaylist()


def AniList_load():
    username = input("Entrez votre pseudo AniList : ")
    variables = {
        'username': username,
    }
    query = '''
        query ($username: String) { 
            MediaListCollection(userName: $username, type: ANIME) { 
                lists {
                    name
                    entries {
                        id
                        status
                        score(format: POINT_10)
                        progress
                        notes
                        repeat
                        media {
                            chapters
                            volumes
                            idMal
                            episodes
                            title { romaji }
                        }
                    }
                }
            }
        }
'''
    response = requests.post('https://graphql.anilist.co',
                             json={'query': query, 'variables': variables})
    data = response.json()
    for i in range(7):
        for o in data['data']['MediaListCollection']['lists'][i]['entries']:
            animeName=""
            for anime in o['media']['title']['romaji']:
                animeName+=anime
            lstAnimeName.append(animeName)
    addPlaylist()

while (mainApp):
    print_menu()
    choix = int(input('Entrez le numéro de votre choix :'))
    if choix == 1:
        AniList_load()
    elif choix == 2:
        fileReader()
    elif choix == 3:
        print('Actuellement indisponible')
    elif choix == 4:
        print('Actuellement indisponible')
    elif choix == 4:
        print('Actuellement indisponible')
    else:
        print('Option invalide')
