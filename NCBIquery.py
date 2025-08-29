import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom


def search_abstract (query, nb_abstract):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
            "db": "pubmed",
            "term": query,
            "retmax": nb_abstract,
            "retmode": "json",
            "sort" : "relevance"
        }
    response = requests.get(url, params=params)
    data = response.json()
    pmids =data['esearchresult']['idlist']
    print(pmids)
    return pmids


def retrieve_abstracts(pmids):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
            "db": "pubmed",
            "id": pmids,
            "retmode": "xml",
            "rettype": "abstract"
            
        }
    response = requests.get(url, params=params)

    root = ET.fromstring(response.text)
    abstracts = ""
    for article in root.findall('.//PubmedArticle'):
        abstract = article.find('.//AbstractText')
        if abstract is not None:
            abstracts += abstract.text
        # print(abstracts)
        # print("Résumé :", abstract.text if abstract is not None else "N/A")
    return abstracts


if __name__=="__main__":
    pmids = search_abstract("bacterial OR viral",10)
    print(retrieve_abstracts(pmids))