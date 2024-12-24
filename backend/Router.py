from fastapi import APIRouter
from library import Classify
from models.Models import *
import pandas as pd
import os

router = APIRouter()

@router.get("/test")
async def test():
    print("Test du fonctionnement de l'API PJE")
    return {"message": "The API connect is working"}

@router.post("/recent")
async def get_recent_tweets(request: RequestModel):

    def classifyTweets(dataframe, classifieur, dataframeFromCSV, nombre_voisins=None,langue = 'fr'):
        print('classifying tweets')

        if classifieur == "Naïf":
            print('naif')
            return Classify.naive(dataframe,langue)

        elif classifieur == "KNN":
            print('knn')
            return Classify.knn(dataframe, dataframeFromCSV, nombre_voisins)

        elif classifieur == "Bayesien V1":
            print('Bayesien V1')
            return Classify.bayes(dataframe, dataframeFromCSV)

        elif classifieur == "Bayesien V2":
            print('Bayesien V2')
            return Classify.bayesV2(dataframe, dataframeFromCSV)

        else:
            print('erreur')
            return dataframe

    # Vérifier si le fichier existe déjà (Pour que l'appli fonctionne sur les échantillons déjà prélevés, suite à la monétisation de l'API twitter)
    if os.path.exists(f"{request.url}"):
        print(f"Le fichier CSV existe déjà : {f"{request.url}"}. Aucun appel API n'est nécessaire.")
        dataframeFromCSV = pd.read_csv(request.url)
        # Retourner le résultat sous forme de JSON
        return dataframeFromCSV.to_json(orient="records")
    else:
        # Appel API pour récupérer les tweets
        print(f"Le fichier CSV {f"{request.url}"} n'existe pas. Appel API nécessaire.")
        # tweets_dataframe = twitter.getTweets(keywords_and=liste_mot_cle, lang=request.langue, max_results=int(nombre_tweets))

        # Nettoyage des tweets
        # tweets_dataframe = Cleaning.cleaning_chain(tweets_dataframe, cleaning.CLEANING_FUNCTIONS)

        # Classification des tweets
        # dataframeFromCSV = pd.read_csv(request.url)
        # dataframe_classified = classifyTweets(
        #     tweets_dataframe, request.classifieur, dataframeFromCSV, nombre_voisins=request.nombre_voisins, langue=request.langue
        # )

        # Mise à jour et sauvegarde du fichier CSV
        # dataframeFromCSV = pd.concat([dataframeFromCSV, dataframe_classified], ignore_index=True)
        # dataframeFromCSV.to_csv(f"ressources/{request.url}.csv", index=False)
        return 


@router.post("/annotation")
async def annotation(AnnotationModel : AnnotationModel):
    dataframe = pd.read_csv(AnnotationModel.urlBase)
    dataframe.loc[dataframe['id'] == AnnotationModel.id_tweet, 'annote'] = AnnotationModel.annotation
    dataframe.to_csv(AnnotationModel.urlBase, index=False)
    return {"message": "Annotation ajoutée"}


