from langchain_core.messages import HumanMessage, ToolMessage 
import datetime 
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


llm = ChatOllama(model="llama3.2:3b")
@tool
def get_current_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

@tool
def add_numbers(a: int, b: int):
    """Adds two integers together and returns the result."""
    return a + b

tools_by_name = {
    "get_current_date": get_current_date,
    "add_numbers": add_numbers,
}

llm_with_tools = llm.bind_tools([get_current_date, add_numbers])

def run_agent(question):
    response = llm_with_tools.invoke(question)

    if not response.tool_calls:
        return response.content

    messages = [HumanMessage(content=question), response]

    for call in response.tool_calls:
        selected_tool = tools_by_name[call["name"]]
        result = selected_tool.invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    final_response = llm_with_tools.invoke(messages)
    return final_response.content

print(run_agent("What is today's date?"))
print(run_agent("What is 15 plus 27?"))
print(run_agent("What is the capital of Rajasthan?"))