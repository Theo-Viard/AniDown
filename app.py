import fonctions as f

print("AniDown V0.2")

while (True):
    f.print_menu()
    choix = int(input('Entrez le numéro de votre choix :'))
    if choix == 1:
        AniList_load()
    elif choix == 2:
        f.fileReader()
    elif choix == 3:
        print('Actuellement indisponible')
    elif choix == 4:
        print('Actuellement indisponible')
    elif choix == 4:
        exit
    else:
        print('Option invalide')
