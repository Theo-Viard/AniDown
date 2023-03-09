from CONSTANTES import OPTIONS
import tkinter as tk
from tkinter import filedialog

def print_menu():
    for key in OPTIONS.keys():
        print(key, '--', OPTIONS[key])

def fileReader():
    print("Extention acceptée : CSV, TXT, MD")
    contenu_fichier = lire_fichier()
    print(contenu_fichier)

        

def lire_fichier():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("CSV files", "*.csv"), ("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            contenu_fichier = f.read()
        return contenu_fichier
    else:
        return None


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