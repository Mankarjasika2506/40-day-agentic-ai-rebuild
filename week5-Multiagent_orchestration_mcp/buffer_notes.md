# Day 35 — Buffer Day Notes

Two deferred items tackled: the blank-placeholder data audit (new this week) and a first
real-data pass on the Day 24 precision/recall eval (previously deferred).

## 1. Data audit — blank `(Articles – )` placeholder scan

**Question:** is the hallucination-triggering blank placeholder bug (found Day 31,
reconfirmed Day 34 through MCP) isolated or systemic across the `civil_guru` collection?

**Method:** pulled every document via `collection.get()` (not `.query()`, since that
ranks by similarity — this needed the full collection) and counted chunks containing
`(Articles – )` or `(Article )`.

**Result:**
- Total chunks: 29,879
- Chunks with blank placeholder: 91 (0.3%)

**Source breakdown of the 91:**
- 61 (67%) have **no `[SOURCE:...]` tag at all** — `UNKNOWN`. This is a *separate* bug
  from the blank-article-number issue: a source-tagging gap somewhere in ingestion,
  affecting more chunks than the placeholder issue itself.
- Remaining 30 are thinly scattered across POLITY (mostly), ECONOMICS, ETHICS,
  GEOGRAPHY, and SOCIOLOGY pages — no single page dominates.

**Conclusion:** not a systemic corpus-wide failure (0.3% is small), but not
one-bad-page-either — it's a diffuse structural scraping issue, likely from tables or
multi-column layouts in the original PDFs that don't extract cleanly into linear text.

**Fix path for Day 38 (production polish), two distinct items:**
1. Chunk-quality filter — flag/exclude any chunk matching a bracketed-empty pattern
   like `(Articles – )` before it reaches retrieval, or route flagged chunks through a
   manual cleanup pass.
2. Separately investigate the `UNKNOWN`-source-tag gap (61 chunks) in the ingestion
   pipeline — bigger count than the placeholder issue, different root cause.

## 2. Day 24 real-data eval — first pass

**Method:** ran `collection.query()` for one real UPSC question against the live
`civil_guru` collection, top-5 results, hand-labeled each result as relevant/not
relevant by reading the actual retrieved text.

**Test question:** "What are the Fundamental Rights in the Indian Constitution?"

| Result | Relevant? | Note |
|---|---|---|
| 1 | Yes | Directly names Fundamental Rights, on-topic |
| 2 | No | Generic chapter-intro text, barely mentions rights |
| 3 | Yes | Lists all six rights by name (contains the blank-placeholder bug, but content is correct) |
| 4 | No | Vague, references Preamble, doesn't name specific rights |
| 5 | Yes | Explicitly states Part III / Articles, on-topic |

**Precision@5 = 3/5 = 0.6**

Recall@k not computed — would require knowing the *total* number of relevant chunks in
the whole collection for this question, which a single manual pass can't establish.
Noted honestly as a limitation rather than estimated.

**Status:** first real data point captured. Two more test questions (different
subjects — Economics, Geography/Ethics) still needed for a fuller picture. Still
partially deferred, not closed.

## Honest scope note

Both items are genuine progress, not complete closure:
- Data audit: done, conclusive, actionable for Day 38.
- Eval: one question done, two more still open. Revisit if another buffer slot appears,
  or fold into Day 38/39 polish work.
