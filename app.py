import csv
import os
print("AniTube V0.1")

lstAnimeName = []
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

