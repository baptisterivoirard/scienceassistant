import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom



url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
        "db": "pubmed",
        "term": "chronic stress AND neuroinflammation",
        "retmax": 5,
        "retmode": "json",
        "sort" : "relevance"
    }
response = requests.get(url, params=params)
data = response.json()
pmids =data['esearchresult']['idlist']
print(pmids)


url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
params = {
        "db": "pubmed",
        "id": pmids,
        "retmode": "xml",
        "rettype": "abstract"
        
    }
response = requests.get(url, params=params)



# dom = xml.dom.minidom.parseString(response.text)
# print(dom.toprettyxml())

root = ET.fromstring(response.text)


for article in root.findall('.//PubmedArticle'):
    title = article.find('.//ArticleTitle')
    print("Titre :", title.text if title is not None else "N/A")

    abstract = article.find('.//AbstractText')
    print("Résumé :", abstract.text if abstract is not None else "N/A")

    print("---")


## Il faut encore fonctionnaliser le script pour prendre en entrée un question 