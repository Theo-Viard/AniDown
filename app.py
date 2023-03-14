import fonctions as f

print("AniDown V0.2")

while (True):
    f.printMenu()
    choix = int(input('Entrez le numéro de votre choix :'))
    f.terminal_clear()
    if choix == 1:
        f.getByAnilist()
    elif choix == 2:
        f.getByFile()
    elif choix == 3:
        f.getByInput()
    elif choix == 4:
        exit
    else:
        print('Option invalide')
