# Day 04 — MCP Concept Notes

## The problem raw tool-calling has

Tools like `search_civil_guru`, `get_current_date`, and `add_numbers` (built Day 29)
are tightly coupled to one codebase:

- They live inside `Mini_Project_4.py`
- `search_civil_guru` depends on a local ChromaDB `collection` object sitting on my disk
- To use any of them elsewhere, another developer would have to copy my source code,
  my database, and my environment — not just import a package

This is the same problem a plain Python function has before it becomes a proper API:
no other program (different language, different codebase) can call it without direct
access to the code itself.

## Why "just write an API" doesn't fully fix it either

An API solves *access* (anyone can hit an endpoint, regardless of language). But for
**LLM tool-calling specifically**, there's a second problem: the LLM has zero built-in
knowledge of what a tool does. Someone has to describe it — name, purpose, arguments,
return shape — the same job `@tool` + docstring does today for LangChain's `.bind_tools()`.

If every developer who wants to use my tool has to hand-write their own description/wrapper:
- That's duplicated work, N times over, for N users
- Wrappers go stale silently the moment I change how the tool actually works
- Nothing forces consistency across frameworks (LangGraph vs. something else)

## What MCP actually is

**MCP (Model Context Protocol) = a standardized way for a tool to describe and expose
itself**, so any MCP-compatible agent — regardless of framework or language — can
discover and call it without custom one-off integration code per tool per project.

It is **not** a replacement for tool-calling. The LLM still decides when to call a tool
and still gets a result back the same way. MCP is a **packaging/transport layer that
sits around tool-calling** — same relationship API had to raw function calls.

Two sides:
- **MCP server** — exposes one or more tools, describes itself once
- **MCP client** — an agent (mine or anyone else's) connects, auto-discovers available
  tools, calls them — no hand-written wrapper needed

## Why this matters for Civil Guru specifically

Today, `search_civil_guru` only works inside this one LangGraph project. If I started a
different project next month — different framework, maybe not even LangGraph — I'd have
to copy-paste the function and drag the ChromaDB connection along, rewiring it from
scratch every time.

As an MCP server, I'd build it **once**. Any future agent — mine or someone else's —
just connects and gets the tool for free, no re-integration required.
