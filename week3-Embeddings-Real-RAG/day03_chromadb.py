import chromadb   

# using the in-memory database
client = chromadb.Client()  # create an in-memory database
collection = client.create_collection(name="my_documents")  # Create a collection in the database

collection.add(
    documents = ["I love cats","I adore cats", "I love dogs", "The stock market crashed"],
    ids = ["doc1", "doc2", "doc3", "doc4"]
)

results = collection.query(
    query_texts = ["I really like cats"],
    n_results = 2
)

print(results)


# using the persistent database
client = chromadb.PersistentClient(path="./chroma_db")  # create a persistent database
collection = client.get_or_create_collection(name="my_documents")

collection.add(
    documents=["I love cats"],
    ids=["doc1"]
)
print("First add done")

collection.add(
    documents=["Something completely different"],
    ids=["doc1"]
)
print("Second add done")

result = collection.get(ids=["doc1"])
print(result)


# adding metadata
collection.add(
    documents=["The Battle of Plassey was fought in 1757", "Newton's laws describe motion"],
    metadatas=[{"subject": "History"}, {"subject": "Physics"}],
    ids=["fact1", "fact2"]
)

results = collection.query(
    query_texts=["Tell me about a famous battle"],
    n_results=2,
    where={"subject": "History"}
)
print(results)