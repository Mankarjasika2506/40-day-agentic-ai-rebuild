import math      # Import the math module for mathematical operations

def cosine_similarity(a,b):  # Calculate cosine similarity between two vectors
    dot_product = 0          # Initialize dot product
    for i in range(len(a)):
        dot_product += a[i] * b[i]    # Calculate dot product of vectors a and b

    magnitude_a = math.sqrt(sum(x**2 for x in a))      # Calculate magnitude of vector a
    magnitude_b = math.sqrt(sum(x**2 for x in b))      # Calculate magnitude of vector b

    return dot_product / (magnitude_a * magnitude_b)  # Return cosine similarity value

print(cosine_similarity([4, 1], [3.8, 1.2]))   
print(cosine_similarity([4, 1], [-2, 5]))       