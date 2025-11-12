import subprocess 
from NCBIquery import search_abstract, retrieve_abstracts
from preprocessing import preprocessing
from chunking import chunker
from embedding import embedding





def main():
    question = input("Enter your scientific question :")
    nb_abstract = input("What is the depth of the search ? (number of abstracts to retrieve (max 20))")
    query = subprocess.run (["ollama", "run", "llama_keyword:latest"], input= question, text=True, capture_output=True)
    pmids = search_abstract(query.stdout, nb_abstract)
    abstracts = retrieve_abstracts(pmids)
    processed_abstracts = preprocessing(abstracts)
    chunks = chunker(processed_abstracts, 500, 50)
    indices = embedding(chunks, question, 2)
    important_chunks = []
    for k in indices[0]:
        print (chunks[k])
        important_chunks.append(chunks[k])
    prompt_complement = '\n'.join(important_chunks)
    prompt = f"Using the following context : {prompt_complement} \n Answer the following question : {question}"
    reponse = subprocess.run(["ollama", "run", "llama_sientist:latest"], input=prompt, text=True, capture_output=True)

    


    return reponse.stdout




if __name__=="__main__":
    print(main())

