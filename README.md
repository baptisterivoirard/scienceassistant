# Projet assistant scientifique

## But et interet du projet

Ce projet consiste en la création d'un assistant de réponse à des questions scientifiques en prenant appui sur les technologies LMM. 
Il utilise un deux modèles de langage préentrainé qui ont été spécialisé à une tache précise à l'aide d'un modèle File (mettre le nom de la téchnique). Le but est de fournir une réponse sûr à l'utilisateur en utilisant le procédé de retrival augmanted génération (RAG) afin de fournir une information scientifique correcte et limiter l'hallucination propre aux modèles LLM. Cet asssistant est capable de : Recevoir une question scientifique complexe.

Utiliser un LLM local (via Ollama) pour en extraire des mots-clés ou requêtes PubMed.

Interroger l’API PubMed (NCBI E-utilities) pour récupérer des articles pertinents.

Prétraiter, découper et indexer les abstracts.

Faire un RAG (Retrieval-Augmented Generation) pour fournir une réponse scientifique argumentée et sourcée.

Le second but du projet a été de me former et apprendre à utiliser et comprednre des technologie qui m'intéresse grandemet et qui me seront utiles pour ma vie professionelle. J'ai ainsi pu apprendre à run des modèle LLM localement avec Ollama, les personanliser et les spécialiser à l'aide de model Files, utiliser Biobert pour réaliser des embedings de chunk de text, utiliser l'API de NCBI via request, utiliser un index FAISS et réaliser des recherche de similarité pour une approche de RAG.  

## Fonctionnement du projet 

Le projet est codé en python et utilise 5 scripts principaux pour le code + deux ficher texte annexes qui sont les modèles Files nécessaires à la personalisation des modèles locaux de Ollama 

## Modèles personnalisés  

Deux modèles ont été customé avec la méthode de Prompt-based model customization aussi appelé model conditioning. Cette méthode consiste à ajouté un Propt system permanent à un modèle préentrainé afin de le contraindre par exemple à un type de réponse spécifique. 
Dans notre cas un petit modèle Llama (le llama3.2:3b) a été customisé de deux manières différentes avec la commande ollama create. Le premier modèle file a permis d'obtenir un modèle qui extrait d'une question scientifique les mots cléfs pour les rechereches avancées pubmed. Le second permet d'obtenir la réponse à la question en se basant unqiement sur les informations extraites des articles. 

## NCBIquery.py 

Après avoir extrait les mots clés de la quesiton scientifique avec le modèle configurer pour, ils sont utilisé pour récuperer les abstracts des articles corespondants le plus au dit mots clefs (le nombre d'abstract à récuprer est defini par l'utilisateur après avoir rentré sa question). J'ai choisis de me limiter au abstract pour car c'est la ou la majorité des conclusions importantes des articles se trouve ce qui permet de prendre plus d'articles pour avoir une vu plus générale de la question sans prendre trop de texte inutilement ce qui ralongerai le procesus de traitement, embeding et indexage de l'information. 
Ce script contient deux fonctions : 
- search_abstract qui va récuperer les pubmed Ids des n articles les plus pertinents qui ressortent après la recherche avancée
- retrieve_abstract qui à l'aide de ces pubmed Ids récupère le texte des abstracts de chacun des articles

## preprocessing.py 

Ce script ne contient qu'une fonction qui permet de netoyer le texte des abstract de tous ce qui ne contient pas l'information et est donc inutile comme les liens ou les numéro faisant référence à un article de la bibligraphie à l'aide d'expression regex. 

## Chunking.py 

Ce script ne contient qu'une fonction qui permet de découper le texte des abstracts en petit chunk de 500 mots avec un overlap de 50 mots (pour ne pas avoir de phrases coupées) pour chaque pour le préparer à l'embeding 

## Notes 

lenteur du code, le but était juste d'apprendre à utiliser les technologies donc le code n'est pas otpimisé pour tourner vite 

## Exemple de fonctionnement 