import chromadb
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage 
import datetime
from langchain_core.tools import tool
from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")   # initialize a pre-trained sentence transformer model for generating embeddings for documents


class MyEmbeddingFunction(EmbeddingFunction):    # custom embedding function class that inherits from the EmbeddingFunction class provided by ChromaDB, allowing for the generation of embeddings for documents using a pre-trained sentence transformer model
    def __init__(self):       # constructor to initialize the embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # initialize the embedding model

    def __call__(self, input: Documents) -> Embeddings:  # method to generate embeddings for the input documents
        return self.model.encode(input).tolist()   # convert the embeddings to a list format for compatibility with ChromaDB


client = chromadb.PersistentClient(path=r"C:\Users\manka\OneDrive\Desktop\CIVIL_GURU\db")  # initialize a persistent ChromaDB client with the specified path to store the database
collection = client.get_collection("civil_guru", embedding_function=MyEmbeddingFunction())  # get the "civil_guru" collection from the ChromaDB client and specify the embedding function to be used for generating embeddings for the documents in this collection


results = collection.query(query_texts=["Fundamental Rights"], n_results=3)  # query the "civil_guru" collection for documents related to "Fundamental Rights" and retrieve the top 3 results
print(results["documents"][0])   # print the first document from the query results, which contains relevant information about "Fundamental Rights"


llm = ChatOllama(model="llama3.2:3b")   # initialize a ChatOllama language model with the specified model name "llama3.2:3b" for generating responses to user queries


@tool   # define a tool function that can be called by the language model to get the current date
def get_current_date():   # is a tool function that returns the current date in YYYY-MM-DD format
    """Returns the current date in YYYY-MM-DD format."""   # docstring describing the purpose of the function
    return datetime.datetime.now().strftime("%Y-%m-%d")  # return the current date formatted as a string in YYYY-MM-DD format


@tool
def add_numbers(a: int, b: int):  # is a tool function that adds two integers together and returns the result
    """Adds two integers together and returns the result."""  # docstring describing the purpose of the function
    return a + b   # return the sum of the two integers a and b


@tool
def search_civil_guru(question: str) -> str:   # is a tool function that searches the UPSC study material (NCERT textbooks) and returns relevant passages for a given topic or question
     """Searches UPSC study material (NCERT textbooks) and returns relevant passages for a given topic or question."""  # docstring describing the purpose of the function
     results = collection.query(query_texts=[question], n_results = 3) # query the "civil_guru" collection for documents related to the given question and retrieve the top 3 results
     docs = results["documents"][0]  # get the first document from the query results, which contains relevant information about the given question
     return "\n\n".join(docs)  # return the relevant passages as a single string, with each passage separated by two newline characters for better readability


tools_by_name = {   # dictionary that maps tool names to their corresponding tool functions
    "get_current_date": get_current_date,  
    "add_numbers": add_numbers,
    "search_civil_guru": search_civil_guru,
}


llm_with_tools = llm.bind_tools([get_current_date, add_numbers, search_civil_guru])  # bind the language model to the defined tools, allowing it to call these tools when generating responses to user queries



def run_agent(question):  # function that runs the agent to process a user question and generate a response using the language model and the defined tools
    response = llm_with_tools.invoke(question)  # invoke the language model with the user question to generate an initial response

    if not response.tool_calls:  # check if the response contains any tool calls; if not, return the content of the response directly
        return response.content  # return the content of the response if no tool calls are present

    messages = [HumanMessage(content=question), response]  # create a list of messages that includes the original user question and the initial response from the language model

    for call in response.tool_calls:   # iterate over each tool call in the response to process them and generate results using the corresponding tool functions
        selected_tool = tools_by_name[call["name"]]   # select the appropriate tool function based on the name of the tool call
        result = selected_tool.invoke(call["args"])  # invoke the selected tool function with the provided arguments to generate a result
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))   # append a ToolMessage to the messages list that contains the result of the tool call, along with the tool call ID for reference

    final_response = llm_with_tools.invoke(messages)  # invoke the language model again with the updated list of messages, which now includes the results of the tool calls, to generate a final response that incorporates the information obtained from the tools
    return final_response.content  # return the content of the final response generated by the language model, which includes the information obtained from the tool calls and any additional context provided by the user question



print(run_agent("What are the Fundamental Rights in the Indian Constitution?")) 
print(run_agent("What is today's date?"))
print(run_agent("What is 100 plus 250?"))
