import chromadb   
from langchain_ollama import OllamaLLM

import sys 
sys.path.append("../week3-Embeddings-Real-RAG")

from day01_cosine_similarity import cosine_similarity
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "The Battle of Plassey was fought in 1757.",
    "Article 21 guarantees the right to life and personal liberty.",
    "The Tropic of Cancer passes through eight Indian states.",
]

embeddings = model.encode(documents)

# keep the single best pattern
def brute_force_knn(query_vector, documents, embeddings, k=1):
    best_score = -2
    best_document = None
    for i in range(len(embeddings)):
        score = cosine_similarity(query_vector, embeddings[i])
        if score > best_score:
            best_score = score
            best_document = documents[i]
    return best_document, best_score

query_vector = model.encode(["When was a major battle fought?"])[0]

result_document, result_score = brute_force_knn(query_vector, documents, embeddings)
print(result_document)
print(result_score)


# keep the best N pattern
def brute_force_knn(query_vector, documents, embeddings, k=1):
    all_results = []
    for i in range(len(embeddings)):
        score = cosine_similarity(query_vector, embeddings[i])
        all_results.append((documents[i], score))
    
    all_results.sort(key=lambda x: x[1], reverse=True)
    top_k_results = all_results[:k]
    
    return top_k_results

query_vector = model.encode(["When was a major battle fought?"])[0]

results = brute_force_knn(query_vector, documents, embeddings, k=2)
for doc, score in results:
    print(doc, "-", score)
