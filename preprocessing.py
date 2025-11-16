## Script contenant la fonction de préprocessing des abstracts, même si elle ne vas pas servir pour la plupart des cas.

import re 

def preprocessing (text):
    text = re.sub(r'\[\d+\]', '', text) # enlève les reférence à un article de la bibliographie exemple [1]
    text = re.sub(r'http\S+', '', text) # enlève les liens
    text = re.sub(r'https\S+', '', text)
    text = re.sub(r'doi:\S+', '', text) # enlève les DOI
    text = re.sub(r'DOI:\S+', '', text)
    text = re.sub(r'www\S+', '', text) # enlève les liens
    text = re.sub(r"©.*$", '', text) # enlève les symboles inutiles
    return text

if __name__ == "__main__":
    print (preprocessing('this is a test http://exemple.com and doi:1000000 and [1]'))