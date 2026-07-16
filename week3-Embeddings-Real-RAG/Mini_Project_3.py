import chromadb   
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model = "llama3.2:3b")

client = chromadb.Client()
collection = client.create_collection(name="MY_DOCS")

collection.add(
    documents = ["The Battle of Plassey was fought in 1757 between the British East India Company and the Nawab of Bengal.","Article 21 of the Indian Constitution guarantees the right to life and personal liberty.","The Tropic of Cancer passes through eight Indian states.","The Quit India Movement was launched by Mahatma Gandhi in August 1942.","The Rajya Sabha is the upper house of the Indian Parliament and its members are elected for six-year terms.","The Western Ghats are a UNESCO World Heritage Site known for biodiversity.","The Preamble of the Indian Constitution was amended by the 42nd Amendment Act of 1976.","Mount Kangchenjunga is the highest peak in India."],
    metadatas = [{"subject": "History"}, {"subject": "Polity"}, {"subject": "Geography"}, {"subject": "History"}, {"subject": "Polity"},{"subject": "Geography"}, {"subject": "Polity"}, {"subject": "Geography"}],
    ids=["fact1", "fact2", "fact3", "fact4", "fact5", "fact6", "fact7", "fact8"]
)

print(collection.count())

def get_context(collection, question, n_results=3):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    context_chunks = results["documents"][0]
    context = "\n".join(context_chunks)
    return context

def build_prompt(context, question):
    prompt = f"""Answer the question using only the context below. If the answer isn't in the context, say "I don't know."

Context:
{context}

Question:
{question}
"""
    return prompt

while True:
    question = input("\nAsk a UPSC question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Goodbye!")
        break
    
    context = get_context(collection, question)
    prompt = build_prompt(context, question)
    response = llm.invoke(prompt)
    
    print("\nAnswer:", response)

