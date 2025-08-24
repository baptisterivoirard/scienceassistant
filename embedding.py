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
    model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1", torch_dtype="auto")
    tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    
    inputs = tokenizer(chunks, return_tensors="pt", padding =True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        # Moyenne des tokens
    embedings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    
    embedings = np.array(embedings).astype(np.float32)

    faiss.normalize_L2(embedings)
    dimension = embedings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embedings)

    question_tokenized = tokenizer(question, return_tensors="pt", padding = True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs_q = model(**question_tokenized)
        
    question_embedding = outputs_q.last_hidden_state.mean(dim=1).squeeze().numpy()
    question_embedding = np.array(question_embedding).astype(np.float32)
    question_embedding = question_embedding.reshape(1, -1)
    faiss.normalize_L2(question_embedding)

    distances , indices =index.search(question_embedding, k=nb_chunks)
    return indices, distances ## il faut ensuite aller recup les chunks correspondants et mettre en argument le nb de chunks à prendre dans la fonction puis 


if __name__== "__main__":
    print(embedding(abstracts, question,3))