import torch 
from transformers import AutoModel , AutoTokenizer

import numpy as np
import faiss

abstracts = [
    "Breast cancers with HER2 amplification have a higher risk of CNS metastasis.",
    "TLR4 is a key receptor in innate immune response against LPS.",
    "Xylocaine is a local anesthetic drug widely used in surgery.", 
    "The recptor Telt2 is important for the immune response to bacterial infections.",
    "PY45-R is a phosphate interacting protein of the membrane involve in signaling viral infections."
]

question = "What receptors are involved in immune response to LPS?"

def embedding (chunks, question,nb_chunks):
    # Chargement du model et du tokenizer de BioBERT
    model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1", torch_dtype="auto") 
    tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    # Tokenization des chunks par le tokenizer
    inputs = tokenizer(chunks, return_tensors="pt", padding =True, truncation=True, max_length=512)
    # Embedding par le modèle
    with torch.no_grad():
        outputs = model(**inputs)
    # Récupération des vector embedding finaux de chaque chunks et moyenne des tokens de chunks pour avoir un embedding vector [768] par chunk. Squeeze pour enlever les dimmension inutile et passage à numpy parce que Faiss ne supporte pas les tensor pytorch.
    embedings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    # Faiss n'accepte pas le float64
    embedings = np.array(embedings).astype(np.float32)
    # Normalisation L2 pour que tous ai une norme de 1 et donc pouvoir utiliser la cosine similarity pour la comparaison 
    faiss.normalize_L2(embedings)
    dimension = embedings.shape[1]
    # Construction de l'index basé sur le IP (inner product) ce qui avec la normalisation équivaut au cosine similarity
    index = faiss.IndexFlatIP(dimension)
    index.add(embedings) # Ajoute les vector embedding

    # Exactement le même process mais pour la question 
    question_tokenized = tokenizer(question, return_tensors="pt", padding = True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs_q = model(**question_tokenized)
        
    question_embedding = outputs_q.last_hidden_state.mean(dim=1).squeeze().numpy()
    question_embedding = np.array(question_embedding).astype(np.float32)
    question_embedding = question_embedding.reshape(1, -1)
    faiss.normalize_L2(question_embedding)

    # Calcul des chunks les plus proches de la question et récup les n chunks les plus proches
    distances , indices =index.search(question_embedding, k=nb_chunks)
    return indices ## il faut ensuite aller recup les chunks correspondants et mettre en argument le nb de chunks à prendre dans la fonction puis 


if __name__== "__main__":
    print(embedding(abstracts, question,3))