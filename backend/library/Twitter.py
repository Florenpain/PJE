from requests_oauthlib import OAuth1Session
import pandas as pd
from config.credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

OAUTH = OAuth1Session(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_TOKEN_SECRET,
)

def requestApi(requete_http):
    print('searching :', requete_http)
    response = OAUTH.get(requete_http)
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
    return response


def getTweets(keywords_or=[], keywords_and=[], subject=None, lang='en', max_results=10):
    """
    Recupère les tweets en créeant une requête http vers l'api v2 de tweeter
    Ne récupère pas les RT
    """
    #Base de la requête
    request = 'https://api.x.com/2/tweets/search/recent?query='
    
    # Ajoute le # à la requête
    if subject:
        request += '%23'+subject+'%20'

    # Ajoute les mots clés obligatoire
    if len(keywords_and) != 0:
        if len(keywords_and) > 1:
            request += '%28'
            request += keywords_and[0]
            for i in range(1, len(keywords_and)):
                request += '%20' + keywords_and[i]
            request += '%29'
        elif len(keywords_and) == 1:
            request += keywords_and[0]
        request += '%20'
    
    # Ajoute les mot clés secondaires
    if len(keywords_or) != 0:
        if len(keywords_or) > 1:
            request += '%28'
            request += keywords_or[0]
            for i in range(1, len(keywords_or)):
                request += '%20OR%20' + keywords_or[i]
            request += '%29'
        elif len(keywords_or) == 1:
            request += keywords_or[0]
        request += '%20'
        
    # Enlève les retweets
    request += '-is%3Aretweet%20'

    # langue du tweet
    request += 'lang%3A' + lang

    # reste des paramètre qui n'appartiennent pas a la query :
    # On les ajoutes avec un '&'
    request += '&max_results=' + str(max_results)
    
    # On ajoute les champs supplémentaire que l'on veut récupérer
    request += '&tweet.fields=created_at,id,text'

    # Enlève les RT:
    # request += "%20-is:retweet"

    # Lance la requête
    resp = requestApi(request)

    # Formate la réponse en json et crée le fichier csv
    df = pd.DataFrame(resp.json()['data'])

    return df


if __name__ == '__main__':
    params = dict()
    print("Laisser blanc pour valeur par défaut")
    params['keywords_and'] = input("Mot clés obligatoires du tweet \n").split(' ')
    params['keywords_or'] = input("Mot clés recherché dans le tweet \n").split(' ')
    params['subject'] = input("# du tweet\n")
    params['lang'] = input("Language du tweet recherché\n")
    params['max_results'] = input("Nombre de tweets recupérés maximum\n")
    for el in list(params.keys()) :
        if params[el] == '':
            del params[el]

    # Temps de requete a return
    resp = getTweets(
        ** params
    )
    print(dict(resp))

