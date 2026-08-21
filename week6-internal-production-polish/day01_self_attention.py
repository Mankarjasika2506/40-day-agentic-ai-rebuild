"""
Day 36 - Self-Attention from scratch (NumPy only)
40-Day Agentic AI Rebuild

Builds Q, K, V projections, scaled dot-product attention, softmax,
and the final weighted-sum output -- entirely by hand, no libraries
beyond NumPy.

NOTE - Multi-head attention (not implemented here, concept only):
Real transformers don't run self_attention() once -- they run it
several times in parallel ("heads"), each with its own W_Q/W_K/W_V
(often on a smaller slice of the embedding dim, e.g. 8-dim split into
2 heads of 4-dim each). Each head can specialize in a different kind
of relationship (grammar, pronoun resolution, etc). The heads' outputs
are then concatenated back together into the original embedding width.
Mechanically this is just calling self_attention() multiple times with
different weight matrices and stacking the results -- a natural
extension for Day 37+ / production polish, deliberately left out of
Day 36's scope to keep today focused on the core mechanism.
"""

import numpy as np


def self_attention(X, W_Q, W_K, W_V):
    """
    Compute single-head self-attention.

    X   : (seq_len, embed_dim)      raw embeddings
    W_Q : (embed_dim, embed_dim)    query projection weights
    W_K : (embed_dim, embed_dim)    key projection weights
    W_V : (embed_dim, embed_dim)    value projection weights

    Returns:
        output           : (seq_len, embed_dim) context-aware vectors
        attention_weights : (seq_len, seq_len)  softmax attention matrix
    """
    # 1. Project embeddings into Query, Key, Value spaces
    Q = X @ W_Q
    K = X @ W_K
    V = X @ W_V

    # 2. Raw pairwise relevance scores (seq_len, seq_len)
    scores = Q @ K.T

    # 3. Scale to keep softmax from becoming too sharp
    d_k = K.shape[1]
    scaled_scores = scores / np.sqrt(d_k)

    # 4. Softmax row-wise -> attention weights (probabilities per word)
    exp_scores = np.exp(scaled_scores)
    row_sums = np.sum(exp_scores, axis=1, keepdims=True)
    attention_weights = exp_scores / row_sums

    # 5. Weighted sum of Values -> new context-aware vectors
    output = attention_weights @ V

    return output, attention_weights


if __name__ == "__main__":
    np.random.seed(42)

    # Toy sequence: 4 words, 8-dim embeddings
    X = np.random.rand(4, 8)
    W_Q = np.random.rand(8, 8)
    W_K = np.random.rand(8, 8)
    W_V = np.random.rand(8, 8)

    output, attention_weights = self_attention(X, W_Q, W_K, W_V)

    print("Input shape :", X.shape)
    print("Output shape:", output.shape)
    print()
    print("Attention weights (each row sums to 1):")
    print(attention_weights)
    print()
    print("Row sums check:", np.sum(attention_weights, axis=1))
    print()
    print("Word 0 -- original embedding:")
    print(X[0])
    print("Word 0 -- context-aware output:")
    print(output[0])