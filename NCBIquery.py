import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom


def search_abstract (query, nb_abstract):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" # URL des outils NCBI
    params = {
            "db": "pubmed",
            "term": query,
            "retmax": nb_abstract,
            "retmode": "json",
            "sort" : "relevance"
        } # parametres de la recherche avancé (trié par pertinence et retrivation mode en JSON)
    response = requests.get(url, params=params) # requete http à l'API de NCBI pour la recherche
    data = response.json() # transforme en dict python
    pmids =data['esearchresult']['idlist'] 
    print(pmids)
    return pmids #return le ID pubmed des n articles les plus pertinents 


def retrieve_abstracts(pmids):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
            "db": "pubmed",
            "id": pmids,
            "retmode": "xml",
            "rettype": "abstract"
            
        }
    response = requests.get(url, params=params) #requete http à l'API de NCBI pour la recuperation de document

    root = ET.fromstring(response.text) # transforme le texte qui vient de la requette en arbre XML 
    abstracts = ""
    for article in root.findall('.//PubmedArticle'): # parcours tout les éléments PubmedArticle
        abstract = article.find('.//AbstractText') 
        if abstract is not None:
            abstracts += abstract.text # concatène dans un sel str le texte de tout les abstracts
        # print(abstracts)
        # print("Résumé :", abstract.text if abstract is not None else "N/A")
    return abstracts


if __name__=="__main__":
    pmids = search_abstract("bacterial OR viral",10)
    print(retrieve_abstracts(pmids))