import math      # Import the math module for mathematical operations
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(a,b):  # Calculate cosine similarity between two vectors
    dot_product = 0          # Initialize dot product
    for i in range(len(a)):
        dot_product += a[i] * b[i]    # Calculate dot product of vectors a and b

    magnitude_a = math.sqrt(sum(x**2 for x in a))      # Calculate magnitude of vector a
    magnitude_b = math.sqrt(sum(x**2 for x in b))      # Calculate magnitude of vector b

    return dot_product / (magnitude_a * magnitude_b)  # Return cosine similarity value

sentences = ["I love cats", "I adore cats", "I love dogs"]
embeddings = model.encode(sentences)

print(embeddings.shape)  # Print the shape of the embeddings array

print(cosine_similarity(embeddings[0], embeddings[1]))  # "I love cats" vs "I adore cats"
print(cosine_similarity(embeddings[0], embeddings[2]))  # "I love cats" vs "I love dogs"

print(embeddings[0][:10])
print(embeddings[0].dtype)