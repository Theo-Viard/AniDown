"""
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
"""