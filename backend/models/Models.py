from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from time import time

class TweetModel(BaseModel):
    date : datetime
    text : str
    author : str

class ResponseModel(BaseModel):
    number_results : int
    tweets : List[TweetModel]

class RequestModel(BaseModel):
    mot_cle : str
    url : str
    nombre_tweets : int
    classifieur : str
    langue : str
    nombre_voisins : int

class AnnotationModel(BaseModel):
    id_tweet : int
    urlBase : str
    annotation : int