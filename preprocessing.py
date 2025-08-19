## Script contenant la fonction de préprocessing des abstracts, même si elle ne vas pas servir pour la plupart des cas.

import re 

def preprocessing (text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'https\S+', '', text)
    text = re.sub(r'doi:\S+', '', text)
    text = re.sub(r'DOI:\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    text = re.sub(r"©.*$", '', text)
    return text

print (preprocessing('this is a test http://exemple.com and doi:1000000 and [1]'))