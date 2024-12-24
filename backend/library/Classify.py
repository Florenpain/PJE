from library.Utils import cleanTweets
from ressources.data import NEUTRE, POSITIF, NEGATIF

# Listes de mots positifs et négatifs prédéfinies 
NEGATIVES = []
POSITIVES = []

# Listes de mots positif et négatifs prédéfinis en anglais
NEGATIFS = []
POSITIFS = []

def naive(tweets_dataframe,langue = 'fr'):
    def import_words():
        """
        Importe les listes de mot prédéfinies
        """
        global POSITIVES, NEGATIVES, POSITIFS, NEGATIFS

        with open('ressources/positive.txt', 'r', encoding='latin-1') as f:
            lines = [line.rstrip() for line in f]
            POSITIVES = lines[0].split(', ')
            POSITIFS = lines[1].split(', ')

        with open('ressources/negative.txt', 'r', encoding='latin-1') as f:
            lines = [line.rstrip() for line in f]
            NEGATIVES = lines[0].split(', ')
            NEGATIFS = lines[1].split(', ')

    def annote(s):
        """
        Cherche les mots du tweets dans les listes
        calcule le score des mots trouvés positifs moins le nombre de mots négatifs
        Renvoi la polarité du tweet
        Attention seulement tweets fr
        """
        p = 0
        n = 0
        if langue == 'fr' :
            for w in POSITIFS:
                if s.find(' '+w+' ') != -1:
                    p += 1
                    
            for w in NEGATIFS:
                if s.find(' '+w+' ') != -1:
                    n += 1
        elif langue == 'en':
            for w in POSITIVES:
                if s.find(' '+w+' ') != -1:
                    p += 1
                    
            for w in NEGATIVES:
                if s.find(' '+w+' ') != -1:
                    n += 1
                
        score = p - n

        if score == 0:
            return NEUTRE
        elif score > 0:
            return POSITIF
        
        return NEGATIF

    # Si les listes n'ont pas été importées, les importe
    if len(POSITIVES) == 0:
        import_words()
        
    df = tweets_dataframe.copy()
    df['annote'] = df['text'].apply(annote)

    return df

def knn(tweets_dataframe, baseDF, nombreVoisins):

    cleanedTweet = tweets_dataframe.copy()
    
    # Plus les tweets sont proches, plus la valeur retournée sera petite
    def distance_naive(s1, s2):
        liste_s1 = s1.split(' ')
        liste_s2 = s2.split(' ')
        communs = 0
        for w in liste_s1:
            if w in liste_s2:
                communs += 1
        return (len(liste_s1) + len(liste_s2) - communs) / (len(liste_s1) + len(liste_s2))

    def calcul_proches_voisins(tweet):

        proches_voisins = []
        for i in range(1, nombreVoisins + 1):
            proches_voisins += [baseDF.iloc[i]]
        for i in range(nombreVoisins + 1, len(baseDF)):
            dist = distance_naive(tweet, baseDF.iloc[i]['text'])
            for j in range(nombreVoisins):
                if dist > distance_naive(tweet, proches_voisins[j]['text']):
                    proches_voisins[j] = baseDF.iloc[i]
                    break

        nb_positif = 0
        nb_negatif = 0
        nb_neutre = 0

        for voisin in proches_voisins:
            if voisin['annote'] == POSITIF:
                nb_positif += 1
            elif voisin['annote'] == NEGATIF:
                nb_negatif += 1
            else :
                nb_neutre += 1

        if nb_positif > nb_negatif and nb_positif > nb_neutre:
            return POSITIF
        elif nb_negatif > nb_positif and nb_negatif > nb_neutre:
            return NEGATIF
        else:
            return NEUTRE

    cleanedTweet['annote'] = cleanedTweet['text'].apply(calcul_proches_voisins)

    return cleanedTweet

def bayes(tweets_dataframe, base, mode=0):

    baseDF = base

    def calcul_proba(tweet):

        # Calcul de la probabilité d'être positif
        proba_positif = (baseDF['annote'] == POSITIF).sum() / baseDF.shape[0]
        proba_negatif = (baseDF['annote'] == NEGATIF).sum() / baseDF.shape[0]
        proba_neutre = (baseDF['annote'] == NEUTRE).sum() / baseDF.shape[0]

        # On récupère les mots du tweet
        if mode == 0 or mode == 2:
            for word in tweet.split():
                compteur_occurence_positive = 1 # compteur d'occurence du mot dans les tweets positifs
                compteur_occurence_negative = 1
                compteur_occurence_neutre = 1

                nombre_total_mots_tweets_base = baseDF['text'].str.split().str.len().sum() # Nombre total de mots dans la base d'apprentissage

                nombre_total_mots_classe_positive = nombre_total_mots_tweets_base
                nombre_total_mots_classe_negative = nombre_total_mots_tweets_base
                nombre_total_mots_classe_neutre = nombre_total_mots_tweets_base

                for tweetPositif in baseDF[baseDF['annote'] == POSITIF]['text']: # On parcourt les tweets positifs
                    nombre_total_mots_classe_positive += len(tweetPositif.split())  # On incrémente le nombre total de mots dans les tweets positifs
                    if word in tweetPositif.split(): # Si le mot est présent dans le tweet positif
                        compteur_occurence_positive += 1 # On incrémente le compteur d'occurence
                proba_positif *= compteur_occurence_positive / nombre_total_mots_classe_positive # On multiplie la probabilité par la probabilité du mot dans la classe positive

                for tweetNegatif in baseDF[baseDF['annote'] == NEGATIF]['text']:
                    nombre_total_mots_classe_negative += len(tweetNegatif.split())
                    if word in tweetNegatif.split():
                        compteur_occurence_negative += 1
                proba_negatif *= compteur_occurence_negative / nombre_total_mots_classe_negative

                for tweetNeutre in baseDF[baseDF['annote'] == NEUTRE]['text']:
                    nombre_total_mots_classe_neutre += len(tweetNeutre.split())
                    if word in tweetNeutre.split():
                        compteur_occurence_neutre += 1
                proba_neutre *= compteur_occurence_neutre / nombre_total_mots_classe_neutre
            
        if mode == 1 or mode == 2 :
            for word1, word2 in zip(tweet.split(), tweet.split()[1:]): # Pour chaque paire de mots du tweet

                compteur_occurence_positive = 1  # compteur d'occurence du mot dans les tweets positifs
                compteur_occurence_negative = 1
                compteur_occurence_neutre = 1

                nombre_total_mots_tweets_base = baseDF['text'].str.split().str.len().sum()  # Nombre total de mots dans la base d'apprentissage

                nombre_total_mots_classe_positive = nombre_total_mots_tweets_base
                nombre_total_mots_classe_negative = nombre_total_mots_tweets_base
                nombre_total_mots_classe_neutre = nombre_total_mots_tweets_base

                for tweetPositif in baseDF[baseDF['annote'] == POSITIF]['text']: # On parcourt les tweets positifs
                    nombre_total_mots_classe_positive += len(tweetPositif.split())  # On incrémente le nombre total de mots dans les tweets positifs
                    if word1 + " " + word2 in tweetPositif.split(): # Si le mot est présent dans le tweet positif
                        compteur_occurence_positive += 1 # On incrémente le compteur d'occurence
                proba_positif *= compteur_occurence_positive / nombre_total_mots_classe_positive

                for tweetNegatif in baseDF[baseDF['annote'] == NEGATIF]['text']:
                    nombre_total_mots_classe_negative += len(tweetNegatif.split())
                    if word1 + " " + word2 in tweetNegatif.split():
                        compteur_occurence_negative += 1
                proba_negatif *= compteur_occurence_negative / nombre_total_mots_classe_negative

                for tweetNeutre in baseDF[baseDF['annote'] == NEUTRE]['text']:
                    nombre_total_mots_classe_neutre += len(tweetNeutre.split())
                    if word1 + " " + word2 in tweetNeutre.split():
                        compteur_occurence_neutre += 1
                proba_neutre *= compteur_occurence_neutre / nombre_total_mots_classe_neutre

        if proba_positif > proba_negatif and proba_positif > proba_neutre:
            return POSITIF
        elif proba_negatif > proba_positif and proba_negatif > proba_neutre:
            return NEGATIF
        else:
            return NEUTRE

    tweets_dataframe['annote'] = tweets_dataframe['text'].apply(calcul_proba)

    return tweets_dataframe

def bayesV2(tweets_dataframe, base, mode=2):

    # On nettoie le tweet
    cleanedTweet = cleanTweets(tweets_dataframe)
    baseDF = base

    def calcul_proba(tweet):

        # Calcul de la probabilité d'être positif
        proba_positif = (baseDF['annote'] == POSITIF).sum() / baseDF.shape[0]  # Proportion de tweets positifs dans la base d'apprentissage
        proba_negatif = (baseDF['annote'] == NEGATIF).sum() / baseDF.shape[0]  # Proportion de tweets négatifs dans la base d'apprentissage
        proba_neutre = (baseDF['annote'] == NEUTRE).sum() / baseDF.shape[0]  # Proportion de tweets neutres dans la base d'apprentissage

        nombre_total_mots_tweets_base = baseDF['text'].str.split().str.len().sum()  # Nombre total de mots dans la base d'apprentissage

        if mode == 0 or mode == 2:
            for word in tweet.split(): # Pour chaque mot du tweet
                if len(word) > 3: # Si le mot fait plus de 3 caractères

                    compteur_occurence_positive = 1  # compteur d'occurence du mot dans les tweets positifs
                    compteur_occurence_negative = 1 # compteur d'occurence du mot dans les tweets négatifs
                    compteur_occurence_neutre = 1 # compteur d'occurence du mot dans les tweets neutres

                    nombre_total_mots_tweets_base = baseDF['text'].str.split().str.len().sum()  # Nombre total de mots dans la base d'apprentissage

                    nombre_total_mots_classe_positive = nombre_total_mots_tweets_base
                    nombre_total_mots_classe_negative = nombre_total_mots_tweets_base
                    nombre_total_mots_classe_neutre = nombre_total_mots_tweets_base

                    for tweetPositif in baseDF[baseDF['annote'] == POSITIF]['text']: # On parcourt les tweets positifs
                        nombre_total_mots_classe_positive += len(tweetPositif.split())  # On incrémente le nombre total de mots dans les tweets positifs
                        if word in tweetPositif.split(): # Si le mot est présent dans le tweet positif
                            compteur_occurence_positive += 1 # On incrémente le compteur d'occurence
                    proba_positif *= (compteur_occurence_positive / nombre_total_mots_classe_positive) ** tweetPositif.split().count(word) # On multiplie la probabilité par la probabilité du mot dans les tweets positifs

                    for tweetNegatif in baseDF[baseDF['annote'] == NEGATIF]['text']:
                        nombre_total_mots_classe_negative += len(tweetNegatif.split())
                        if word in tweetNegatif.split():
                            compteur_occurence_negative += 1
                    proba_negatif *= (compteur_occurence_negative / nombre_total_mots_classe_negative) ** tweetPositif.split().count(word)

                    for tweetNeutre in baseDF[baseDF['annote'] == NEUTRE]['text']:
                        nombre_total_mots_classe_neutre += len(tweetNeutre.split())
                        if word in tweetNeutre.split():
                            compteur_occurence_neutre += 1
                    proba_neutre *= (compteur_occurence_neutre / nombre_total_mots_classe_neutre) ** tweetPositif.split().count(word)

        if mode == 1 or mode == 2 :
            for word1, word2 in zip(tweet.split(), tweet.split()[1:]): # Pour chaque paire de mots du tweet

                compteur_occurence_positive = 1  # compteur d'occurence du mot dans les tweets positifs
                compteur_occurence_negative = 1
                compteur_occurence_neutre = 1

                nombre_total_mots_tweets_base = baseDF['text'].str.split().str.len().sum()  # Nombre total de mots dans la base d'apprentissage

                nombre_total_mots_classe_positive = nombre_total_mots_tweets_base
                nombre_total_mots_classe_negative = nombre_total_mots_tweets_base
                nombre_total_mots_classe_neutre = nombre_total_mots_tweets_base

                for tweetPositif in baseDF[baseDF['annote'] == POSITIF]['text']: # On parcourt les tweets positifs
                    nombre_total_mots_classe_positive += len(tweetPositif.split())  # On incrémente le nombre total de mots dans les tweets positifs
                    if word1 + " " + word2 in tweetPositif.split(): # Si le mot est présent dans le tweet positif
                        compteur_occurence_positive += 1 # On incrémente le compteur d'occurence
                proba_positif *= (compteur_occurence_positive / nombre_total_mots_classe_positive) ** tweetPositif.split().count(word1 + " " + word2) # On multiplie la probabilité par la probabilité du mot dans les tweets positifs

                for tweetNegatif in baseDF[baseDF['annote'] == NEGATIF]['text']:
                    nombre_total_mots_classe_negative += len(tweetNegatif.split())
                    if word1 + " " + word2 in tweetNegatif.split():
                        compteur_occurence_negative += 1
                proba_negatif *= (compteur_occurence_negative / nombre_total_mots_classe_negative) ** tweetPositif.split().count(word1 + " " + word2)

                for tweetNeutre in baseDF[baseDF['annote'] == NEUTRE]['text']:
                    nombre_total_mots_classe_neutre += len(tweetNeutre.split())
                    if word1 + " " + word2 in tweetNeutre.split():
                        compteur_occurence_neutre += 1
                proba_neutre *= (compteur_occurence_neutre / nombre_total_mots_classe_neutre) ** tweetPositif.split().count(word1 + " " + word2)

        if proba_positif > proba_negatif and proba_positif > proba_neutre:
            return POSITIF
        elif proba_negatif > proba_positif and proba_negatif > proba_neutre:
            return NEGATIF
        else:
            return NEUTRE

    cleanedTweet['annote'] = cleanedTweet['text'].apply(calcul_proba)

    return cleanedTweet
