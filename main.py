import subprocess 






def main():
    question = input("Entre your scientific question :")
    query = subprocess.run (["ollama", "run", "llama_keyword:latest"], input= question, text=True, capture_output=True)
    return(query.stdout)




if __name__=="__main__":
    print(main())

