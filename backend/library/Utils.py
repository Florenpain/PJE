import pandas as pd
from library.Cleaning import cleaning_chain, CLEANING_FUNCTIONS

def cleanTweets(tweets):
    df = pd.DataFrame(tweets)
    df = cleaning_chain(df, CLEANING_FUNCTIONS)
    return df

def toJson(function, tweet):
    return function(tweet).to_json()