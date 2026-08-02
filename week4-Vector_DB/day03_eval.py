#precision
def precision_at_k(retrieved, relevant, k):   # precision = relevant retrieved / retrieved
    retrieved_k = retrieved[:k]   # Get the first k documents from the retrieved list
    relevant_retrieved = [doc for doc in retrieved_k if doc in relevant]   # Count how many of the retrieved documents are relevant
    return len(relevant_retrieved) / k if k > 0 else 0  # Return the precision at k, which is the number of relevant retrieved documents divided by k (the number of retrieved documents considered). If k is 0, return 0 to avoid division by zero.

print(precision_at_k([1, 2, 3, 4, 5], [2, 3, 6], 5))  

#recall
def recall_at_k(retrieved, relevant, k):  # recall = relevant retrieved / relevant
    retrieved_k = retrieved[:k]   # Get the first k documents from the retrieved list
    relevant_retrieved = [doc for doc in retrieved_k if doc in relevant]  # Count how many of the retrieved documents are relevant
    return len(relevant_retrieved) / len(relevant) if len(relevant) > 0 else 0   # Return the recall at k, which is the number of relevant retrieved documents divided by the total number of relevant documents. If there are no relevant documents, return 0 to avoid division by zero.

print(recall_at_k([1, 2, 3, 4, 5], [2, 3, 6], 5))  