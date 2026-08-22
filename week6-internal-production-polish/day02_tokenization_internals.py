"""
Day 37 - Tokenization Internals: Byte-Pair Encoding (BPE) from scratch
40-Day Agentic AI Rebuild

Builds the actual BPE algorithm by hand: word frequency counting,
character-level splitting with end-of-word markers, pair counting,
iterative merging (training), and encoding new/unseen text using the
trained merge rules. No tokenizer libraries used.
"""

from collections import Counter


# ---------------------------------------------------------------------
# STEP 1: Word frequency counting
# BPE starts by counting how often each whole word appears in the
# training corpus -- this weighting is what drives which subword
# pieces get merged first (frequent patterns merge before rare ones).
# ---------------------------------------------------------------------
corpus = "the bank gives loans the bank saves money"
words = corpus.split()
word_freq = Counter(words)


# ---------------------------------------------------------------------
# STEP 2: Character-level split + end-of-word marker
# Every word is broken into individual characters, with a special
# </w> token appended to mark where the word ends. This boundary
# marker is essential -- without it, BPE could merge characters
# across two different words (e.g. the last letter of one word with
# the first letter of the next), producing nonsense tokens.
# Demonstrated here on a single word before building the full vocab.
# ---------------------------------------------------------------------
chars = list("bank")
chars.append("</w>")
print(chars)  # ['b', 'a', 'n', 'k', '</w>']


# ---------------------------------------------------------------------
# STEP 3: Build the initial vocab
# vocab maps: (tuple of characters + </w>) -> frequency
# This is the data structure the whole BPE algorithm operates on.
# Tuples are used (not lists) because dict keys must be hashable.
# ---------------------------------------------------------------------
vocab = {tuple(list(word) + ['</w>']): freq for word, freq in word_freq.items()}
print(vocab)


# ---------------------------------------------------------------------
# STEP 4: Adjacent pair extraction (demo on one word)
# zip(word, word[1:]) pairs each character with the one right after
# it, giving every adjacent pair in the word. n characters -> n-1
# pairs.
# ---------------------------------------------------------------------
word = ('b', 'a', 'n', 'k', '</w>')
pairs = list(zip(word, word[1:]))
print(pairs)  # [('b','a'), ('a','n'), ('n','k'), ('k','</w>')]


# ---------------------------------------------------------------------
# STEP 5: Count adjacent pairs across the WHOLE vocab
# Each pair's count is weighted by the word's frequency -- if "bank"
# appears twice in the corpus, every pair inside "bank" counts twice.
# This tells us which pair to merge next (the most frequent one).
# ---------------------------------------------------------------------
def get_pair_counts(vocab):
    pair_counts = Counter()
    for word, freq in vocab.items():
        pairs = list(zip(word, word[1:]))
        for pair in pairs:
            pair_counts[pair] += freq
    return pair_counts


# ---------------------------------------------------------------------
# STEP 6: Merge a specific pair within ONE word
# Scans left to right. When the target pair is found at position
# i, i+1, the two tokens are fused into one and the scan jumps
# forward by 2 (i += 2) so the just-merged tokens aren't reused.
# Otherwise, the single token is kept as-is and the scan moves
# forward by 1 (i += 1).
# ---------------------------------------------------------------------
def merge_pair(word, pair):
    new_word = []
    i = 0
    while i < len(word):
        if i < len(word) - 1 and (word[i], word[i + 1]) == pair:
            new_word.append(word[i] + word[i + 1])
            i += 2
        else:
            new_word.append(word[i])
            i += 1
    return tuple(new_word)


# ---------------------------------------------------------------------
# STEP 7: Apply a merge across the ENTIRE vocab
# Every word in the vocab gets the winning pair merged (if present),
# producing a new vocab with one more "fused" token type than before.
# ---------------------------------------------------------------------
def merge_vocab(vocab, pair):
    new_vocab = {}
    for word, freq in vocab.items():
        new_word = merge_pair(word, pair)
        new_vocab[new_word] = freq
    return new_vocab


# ---------------------------------------------------------------------
# STEP 8: The BPE training loop
# Repeat num_merges times:
#   1. Count all pair frequencies in the current vocab
#   2. Pick the single most frequent pair
#   3. Merge that pair everywhere it appears
#   4. Record the merge (order matters -- see encode() below)
# The resulting `merges` list, in order, IS the trained tokenizer.
# ---------------------------------------------------------------------
merges = []
num_merges = 5
for i in range(num_merges):
    pair_counts = get_pair_counts(vocab)
    if not pair_counts:
        break
    best_pair = pair_counts.most_common(1)[0][0]
    vocab = merge_vocab(vocab, best_pair)
    merges.append(best_pair)
    print(f"Merge {i + 1}: {best_pair}")

print()
print("Final vocab after", len(merges), "merges:")
for w, f in vocab.items():
    print(" ", w, f)

print()
print("Merge order (this IS the trained BPE model):")
print(merges)


# ---------------------------------------------------------------------
# STEP 9: Encode new text using the trained merges
# To tokenize a (possibly unseen) word: start from raw characters +
# </w>, then replay the learned merges IN THE SAME ORDER they were
# learned. Order matters because later merges depend on earlier ones
# having already produced their fused token -- e.g. ('th','e') can't
# match anything until the ('t','h') merge has already created the
# 'th' token. This is why BPE never fails on unseen words: it falls
# back to whatever combination of learned subwords (down to single
# characters) actually applies.
# ---------------------------------------------------------------------
def encode(word, merges):
    tokens = list(word) + ['</w>']
    for pair in merges:
        tokens = merge_pair(tuple(tokens), pair)
    return list(tokens)


print()
print('encode("the")   ->', encode("the", merges))
print('encode("bank")  ->', encode("bank", merges))
print('encode("gives") ->', encode("gives", merges))

print()
print("NEW words, never seen exactly like this in training:")
print('encode("than")  ->', encode("than", merges))
print('encode("banks") ->', encode("banks", merges))