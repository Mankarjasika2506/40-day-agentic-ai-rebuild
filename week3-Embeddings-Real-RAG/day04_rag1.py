import chromadb   


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

context = get_context(collection, "Tell me about cats")
print(context)
print(type(context))