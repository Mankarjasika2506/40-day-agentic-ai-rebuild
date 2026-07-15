import chromadb   
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model = "llama3.2:3b")

client = chromadb.Client()  
collection = client.create_collection(name="my_documents")  

collection.add(
    documents = ["I love cats","I adore cats", "I love dogs", "The stock market crashed"],
    ids = ["doc1", "doc2", "doc3", "doc4"]
)


results = collection.query(
    query_texts=["Tell me about cats", "Tell me about the stock market"],
    n_results=1
)
print(results)


def get_context(collection, question, n_results=3):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    
    context_chunks = results["documents"][0]
    context = "\n".join(context_chunks)
    
    return context


def build_prompt(context, question):
    prompt = f"""Answer the question using only the context below.If the answer isn't in the context, say "I don't know."
Context : {context}

Question : {question}
"""
    return prompt

context = get_context(collection, "What is the capital of France?")
question = "What is the capital of France?"
prompt = build_prompt(context, question)
print(prompt)

response = llm.invoke(prompt)
print(response)
