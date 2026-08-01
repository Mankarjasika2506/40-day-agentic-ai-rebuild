# Day 23 — HNSW Concept: Greedy Graph Search, Local Minima, and the Two-Layer Fix

No code today — this was a hand-traced conceptual session on a small toy graph (10 points, then 7),
done before touching ChromaDB's actual HNSW parameters.

## 1. The greedy NSW search rule

At the current node, look only at its **direct neighbors** — the nodes it's connected to by an edge,
not the whole graph. If a neighbor is **closer to the query** than the current node is, hop to it.
If **none** of the current node's neighbors are closer than the current node itself, stop — that
node is the answer.

I traced this by hand starting from node A, hopping A → H → F, and stopped at F because none of
F's neighbors (G, H, E) were closer to the query than F was. This matched the true nearest neighbor
in that graph — only 3 nodes out of 10 were ever touched, instead of comparing against all 10
(which is what brute-force k-NN from Day 22 does every single time).

## 2. Why greedy search can fail (the local minimum trap)

Greedy search only ever knows about the best node it happened to check — not the best node that
exists in the whole graph. In a second toy graph, I traced S → A1 → M, and stopped at M because
none of M's neighbors (B1, C1, X) were closer to the query than M was.

But the true closest point, T, was sitting just one hop past X. Greedy never reached it, because
X was slightly *farther* from the query than M — and the greedy rule only allows a hop that is an
immediate improvement. It can't take a step that looks slightly worse right now, even if that step
leads somewhere much better one hop later. So greedy search finds a **local minimum** (best of what
it explored), not necessarily the **global minimum** (best in the entire graph).

## 3. How the two-layer (HNSW) fix works

Layer 0 is the full graph — every node, with short-range edges to nearby points. Layer 1 is a
smaller sample of those same nodes, connected by fewer, longer-range edges — built deliberately,
not by chance.

In my example, Layer 1 only kept S, M, and T, with a single long edge going directly from M to T.
Because the trap nodes (B1, C1, X) simply aren't present in Layer 1, there's no dense local cluster
to get stuck in at that layer. Greedy search on Layer 1 goes straight S → M → T. Once that rough
neighborhood is found, the search drops down to Layer 0 and refines locally from there (checking
T's real neighbors) to confirm the answer.

So the top layer's job isn't precision — it's getting close to the right neighborhood fast, without
walking through the exact dense cluster that would trap a single-layer greedy search. This is what
`hnsw:construction_ef` and `hnsw:search_ef` in ChromaDB actually control under the hood — next
session's topic.
