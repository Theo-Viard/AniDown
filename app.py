import fonctions as f

CONVERSION = False
while (True):
    f.printMenu()
    if CONVERSION:
        print("\nVous êtes en mode conversion, ce mode augmente considérablement le temps d'execution du programme.")
    choix = int(input('Entrez le numéro de votre choix :'))
    f.terminal_clear()
    if str(choix) in "123":
        f.gestionInput(choix,CONVERSION) 
    elif choix == 4:
        if CONVERSION:
            CONVERSION = False
        else:
            CONVERSION = True
    elif choix == 5:
        break
    else:
        print("Option invalide")
