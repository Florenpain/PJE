import re

def replace_RT_with_at(s):
    return re.sub("RT @[a-zA-Z0-9_]+:", '', s)

def replace_username_with_at(s):
    return re.sub("@[a-zA-Z0-9_]+", '', s)

def replace_hashtag(s):
    return re.sub("#[a-zA-Z0-9_]+", '', s)

def replace_ponctuation_with_spaces(s):
    variable = re.search('[!?".;,]', s)
    if variable :
        return re.sub('[!?".;,]', ' ' + s[variable.end()-1] + ' ',s)
    return s

def replace_multi_spaces_with_single(s):
    return re.sub(' +', ' ',s)

def replace_tabulations_with_space(s):
    return re.sub(r'\t', ' ',s)

def replace_dollars_price_with_value(s):
    variable = re.search('\$[0-9]+[.,]?[0-9]*', s)
    if variable :
        return re.sub('\$[0-9]+[.,]?[0-9]*', s[variable.start()+1:variable.end()] ,s)
    return s

def replace_euros_price_with_value(s):
    variable = re.search('[0-9]+[.,]?[0-9]*€',s)
    if variable :
        return re.sub('[0-9]+[.,]?[0-9]*€', s[variable.start():variable.end()] ,s)
    return s

def replace_urls_with_word_url(s):
    return re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*','url',s)

def cleaning_chain(dataframe,functions_list):
    df = dataframe.copy() 
    for f in functions_list :
        df['text'] = df['text'].apply(f)
    return df

CLEANING_FUNCTIONS = {
    replace_RT_with_at,
    replace_username_with_at,
    replace_hashtag,
    replace_urls_with_word_url,
    replace_ponctuation_with_spaces,
    replace_tabulations_with_space,
    replace_dollars_price_with_value,
    replace_euros_price_with_value,
    replace_multi_spaces_with_single,
}