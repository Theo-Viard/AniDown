OPTIONS = {
    1: "Importer d'AniList",
    2: "Importer d'un fichier",
    3: "Chercher un anime en particulier",
    4: "Quitter",
}
QUERY = '''
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