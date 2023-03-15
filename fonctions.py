# Imports
import os
from CONSTANTES import OPTIONS, QUERY, SEARCH_URL
import tkinter as tk
from tkinter import filedialog
import requests
import youtube_dl
import concurrent.futures
from moviepy.editor import VideoFileClip

# Création de la variable globale de conversion
global CONVERSION



### DATA GETTERS



def getByFile():
    """
    Lecteur de fichiers pour récupérer les informations des animes
    """
    print("Extentions acceptées : CSV, TXT, MD")

    # Initialisation des variables
    listAnimeNames = []
    root = tk.Tk()
    root.withdraw()


    file_path = filedialog.askopenfilename(filetypes=[(
        "Markdown files", "*.md"), ("CSV files", "*.csv"), ("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            lignes = f.readlines()
        for line in lignes:
            listAnimeNames.append(line.strip())
        download_all_anime(listAnimeNames)
    else:
        print('Le fichier est invalide ou corrompu')

def getByAnilist():
    """
    Fonction de récupération de données utilisateurs par l'api d'AniList
    """
    username = input("Entrez votre pseudo AniList : ")
    variables = {
        'username': username,
    }
    response = requests.post('https://graphql.anilist.co',
                             json={'query': QUERY, 'variables': variables})
    data = response.json()
    lstAnimeName = []
    try:
        for o in data['data']['MediaListCollection']['lists'][0]['entries']:
            animeName = ""
            for anime in o['media']['title']['romaji']:
                animeName += anime
            lstAnimeName.append(animeName)
    except:
        input("Ce compte n'existe pas")
        terminal_clear()
    download_all_anime(lstAnimeName)

def getByInput():
    """
    Gestion de la récupération du nom de l'anime par le terminal
    """
    print("Si vous avez un doute recopiez le nom exact de l'anime sur le site https://myanimelist.net/")
    AnimeName = input("Entrez le nom de l'anime recherché : ")
    getIndividualAnimeOpeningByName(AnimeName)



### Moteur de l'application



def getOnly1080NC(AnimeList):
    """
    Permet de récupérer un seul openings parmis une liste, et privilégier ceux en bonne qualité.
    """

    #Initialisation de la variable
    dictionnaireOpenings = dict()


    for animeData in AnimeList:
        numOpening = animeData['filename'].split("-")[-1]
        if (numOpening in dictionnaireOpenings.keys() and "OP" in numOpening) or numOpening == "NCBD1080":
            if animeData['nc']: # Vérification du no credits
                if animeData['dictionnaireOpeningsolution'] >= dictionnaireOpenings[numOpening]['dictionnaireOpeningsolution']: # Comparaison de la meilleure résolution
                    if numOpening == "NCBD1080":
                        dictionnaireOpenings[animeData['filename'].split("-")[-2]] = animeData
        else:
            dictionnaireOpenings[numOpening] = animeData
    return dictionnaireOpenings


def getIndividualAnimeOpeningByName(AnimeName):
    """
    Fonction mère de l'application

    Récupére l'opening en ligne et le télécharge
    """

    # Initialisation des variables
    global CONVERSION
    params = {"q": AnimeName, "limit" : 1}

    # Récupération des informations de l'anime
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print('Téléchargement des openings de ' + AnimeName)
        videoFiles = getOnly1080NC(data['search']['videos'])

        # Téléchargement des openings
        for videos in videoFiles.values():
            if 'OP' in videos['filename']:
                try:
                    output = './downloads/'+strClear(AnimeName)+ "/" + videos['basename']
                    ydl_opts = {
                    'outtmpl': output,
                    'quiet' : True,
                    'ignoreerrors': True
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([videos['link']])
                except: 
                    print('error')
                if CONVERSION:
                    convertFile(output)
    else:
        print("Limit Rate Download Exceded", response.status_code)

def download_all_anime(listeAnime):
    """
    Système de création de Thread pour chaque anime 
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(getIndividualAnimeOpeningByName, anime) for anime in listeAnime]
    concurrent.futures.wait(futures)

def convertFile(AnimeBase):
    """
    Systeme de conversion de fichiers (WEBM to MP4)
    """
    input_file = AnimeBase
    output_file = input_file.replace(".webm", ".mp4")
    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file)
    clip.close()
    os.remove(input_file)



### Fonctions externes a l'application mère / petites fonctions nécéssaires ### 



def strClear(AnimeName):
    """
    Petite fonction de suppression de caractères spéciaux
    """
    AnimeName = ''.join(c for c in AnimeName if c not in "!@#:,∬./-_ ")
    return AnimeName

def printMenu():
    """
    Affiche le menu du fichier CONSTANTES
    """    
    print("AniDown V1")
    print("|------------------------------------------------------------------|")
    for key in OPTIONS.keys():
        print("    " + str(key), '--', OPTIONS[key])
    print("|------------------------------------------------------------------|")

def terminal_clear():
    """
    Clear le terminal
    """
    os.system("clear")
    os.system("cls")

def gestionInput(numero,conversion):
    """
    Gère les choix du menu pour rediriger aux bonnes fonctions
    """
    global CONVERSION
    CONVERSION = conversion
    if numero == 1:
        getByAnilist()
    elif numero == 2:
        getByFile()
    elif numero == 3:
        getByInput()
    elif numero == 5:
        exit
