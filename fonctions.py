import os
import time
from CONSTANTES import OPTIONS, CURL_ANIMETHEME, MAX_RETRIES, DELAY
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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    for anime in listeAnime:
        alwaysOPs = True
        numOp = 1
        while (alwaysOPs):
            AnimeName = stringJoiner(anime)
            link = createLink(AnimeName, numOp)
            print(link)
            for _ in range(MAX_RETRIES):
                try:
                    ydl_opts = {
                        'outtmpl': './downloads/'+AnimeName + "_OP" + str(numOp) + ".webm",
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link])
                        break
                except:
                    alwaysOPs = False
                    break
            numOp += 1


def createLink(AnimeName, numOP):
    return CURL_ANIMETHEME + AnimeName + "-OP" + str(numOP) + ".webm"


def stringJoiner(AnimeName):
    AnimeName = AnimeName.split(" ")
    AnimeName = "".join(AnimeName)
    return AnimeName
