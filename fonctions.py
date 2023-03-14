import os
from CONSTANTES import OPTIONS, QUERY
import tkinter as tk
from tkinter import filedialog
import requests
import youtube_dl
import concurrent.futures
from moviepy.editor import VideoFileClip

def printMenu():
    for key in OPTIONS.keys():
        print(key, '--', OPTIONS[key])

def terminal_clear():
    try:
        os.system("clear")
    except:
        os.system("cls")

### Système par fichiers
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

### Système par input terminal

def getByInput():
    print("Si vous avez un doute recopiez le nom exact de l'anime sur le site https://myanimelist.net/")
    AnimeName = input("Entrez le nom de l'anime recherché : ")
    getIndividualAnimeOpeningByName(AnimeName)

### Getter d'openings
def getIndividualAnimeOpeningByName(AnimeName):
    url = "https://api.animethemes.moe/search"
    params = {"q": AnimeName, "limit" : 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print('Téléchargement des openings de ' + AnimeName)
        for videos in data['search']['videos']:
            if 'OP' in videos['filename']:
                try:
                    output = './downloads/'+strClear(AnimeName)+ "/" + videos['basename']
                    ydl_opts = {
                    'outtmpl': output
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([videos['link']])
                except: 
                    print('error')
                convertFile(output)
    else:
        print("Limit Rate Download Exceded", response.status_code)

def convertFile(AnimeBase):
    input_file = AnimeBase
    output_file = input_file.replace(".webm", ".mp4")
    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file)
    clip.close()
    os.remove(input_file)

### Getter de données de compte Anilist
def getByAnilist():
    username = input("Entrez votre pseudo AniList : ")
    variables = {
        'username': username,
    }
    response = requests.post('https://graphql.anilist.co',
                             json={'query': QUERY, 'variables': variables})
    data = response.json()
    lstAnimeName = []
    for o in data['data']['MediaListCollection']['lists'][0]['entries']:
            animeName = ""
            for anime in o['media']['title']['romaji']:
                animeName += anime
            lstAnimeName.append(animeName)
    download_all_anime(lstAnimeName)

### Gestion du téléchargement
def downloader(anime):
    getIndividualAnimeOpeningByName(anime)

def download_all_anime(listeAnime):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(downloader, anime) for anime in listeAnime]
    concurrent.futures.wait(futures)

def strClear(AnimeName):
    AnimeName = ''.join(c for c in AnimeName if c not in "!@#:,∬./-_ ")
    return AnimeName