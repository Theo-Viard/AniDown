import os
import time
from CONSTANTES import OPTIONS, CURL_ANIMETHEME, MAX_RETRIES, DELAY, EXCEPTIONS_SPECIALES
import tkinter as tk
from tkinter import filedialog
import requests
import youtube_dl


def print_menu():
    for key in OPTIONS.keys():
        print(key, '--', OPTIONS[key])


def fileReader():
    print("Extention acceptée : CSV, TXT, MD")
    liste_anime = get_convert_file()
    if liste_anime == None:
        print('Le fichier est invalide ou corrompu')
        return False
    return liste_anime


def getByFile():
    liste_anime = fileReader()
    downloader(liste_anime)


def terminal_clear():
    try:
        os.system("clear")
    except:
        os.system("cls")


def get_convert_file():
    liste_anim = []
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[(
        "Markdown files", "*.md"), ("CSV files", "*.csv"), ("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            lignes = f.readlines()
        for line in lignes:
            liste_anim.append(line.strip())
        return liste_anim
    else:
        return None


def getByInput():
    print("Attention, la moindre faute de frappe dans le nom de l'anime peut ne pas trouver votre anime")
    print("Laissez les espaces et mettez une majuscule a chaque mot du nom. (Lycoris Recoil par exemple)")
    print("Si vous avez un doute recopiez le nom exact de l'anime sur le site https://myanimelist.net/")
    AnimeName = input("Entrez le nom de l'anime recherché : ")
    downloader([AnimeName])


def getByAnilist():
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
    lstAnimeName = []
    for i in range(7):
        for o in data['data']['MediaListCollection']['lists'][i]['entries']:
            animeName = ""
            for anime in o['media']['title']['romaji']:
                animeName += anime
            lstAnimeName.append(animeName)
    downloader(lstAnimeName)


def downloader(listeAnime):
    undownloadable = []
    cpt = 1
    for anime in listeAnime:
        alwaysOPs = True
        numOp = 1
        while (alwaysOPs):
            terminal_clear()
            print(str(cpt) + "/" + str(len(listeAnime)))
            print("Nombre d'animes non trouvés : " + str(len(undownloadable)))
            AnimeName = stringJoiner(anime)
            link = createLink(AnimeName, numOp)
            print(link)
            try:
                ydl_opts = {
                    'outtmpl': './downloads/'+AnimeName + "_OP" + str(numOp) + ".webm",
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
            except:
                if numOp == 1:
                    undownloadable.append(AnimeName)
                alwaysOPs = False
            numOp += 1
        cpt +=1
    if undownloadable != []:
        print("Des animes n'ont pas pu être téléchargés. Essayez un autre nom, ou prennez le sur MyAnimeList et réessayez en individuel. ")
        print("Les animes non téléchargés : ")
        print(undownloadable)


def createLink(AnimeName, numOP):
    for exception in EXCEPTIONS_SPECIALES:
        if exception[0] in AnimeName:
            AnimeName = exception[1]
            break
    caracteres_a_supprimer = "!@#:,∬./-_"
    AnimeName = ''.join(c for c in AnimeName if c not in caracteres_a_supprimer)
    saison = AnimeName[-1]
    if AnimeName.endswith("Season"):
        AnimeName = AnimeName[0:-8]
    if saison.isnumeric():
        anime_name_list = list(AnimeName)
        anime_name_list.pop(-1)
        AnimeName = "".join(anime_name_list)
        AnimeName += "S" + saison
    
    return CURL_ANIMETHEME + AnimeName + "-OP" + str(numOP) + ".webm"


def stringJoiner(AnimeName):
    AnimeName = AnimeName.split(" ")
    AnimeName = "".join(AnimeName)
    return AnimeName
