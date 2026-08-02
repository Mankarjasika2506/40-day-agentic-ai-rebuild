import datetime  # standard lib for getting the current date

from langchain_core.tools import tool  # decorator that turns a plain function into an LLM-callable tool

@tool  # wraps get_current_date so it has .name, .description, .invoke() for LangChain to use
def get_current_date():
    """Returns the current date in YYYY-MM-DD format."""  # this docstring IS what the LLM sees as the tool's description
    return str(datetime.datetime.now().date())  # returns a string (not a date object) so it's JSON-serializable

print(get_current_date.name)         # prints "get_current_date" - the tool's identifier
print(get_current_date.description)  # prints the docstring text above

from langchain_ollama import ChatOllama  # LangChain's wrapper around your local Ollama models

llm = ChatOllama(model="llama3.2:3b")           # connects to your locally running llama3.2:3b via Ollama
llm_with_tools = llm.bind_tools([get_current_date])  # tells the LLM this tool exists and describes it in the prompt

response = llm_with_tools.invoke("What is the capital of Rajasthan?")  # unrelated question - tests whether LLM wrongly calls the tool
for call in response.tool_calls:            # loops through any tool call requests the LLM made (step 2 of the loop)
    result = get_current_date.invoke(call["args"])  # actually EXECUTES the real Python function (step 3)
    print(result)                            # prints the real computed date

print(response.tool_calls)  # shows the raw tool call request(s) the LLM generated - just the "request", not the execution

from langchain_core.messages import HumanMessage, ToolMessage  # message types LangChain uses to represent conversation turns

question = "What is today's date?"          # this time a genuinely relevant question
response = llm_with_tools.invoke(question)  # LLM sees the question, decides to request the date tool (step 2)

messages = [HumanMessage(content=question), response]  # start building conversation history: the user's question + the AI's tool request

for call in response.tool_calls:                                   # go through each tool call the LLM requested
    result = get_current_date.invoke(call["args"])                  # actually run the real function (step 3)
    messages.append(ToolMessage(content=result, tool_call_id=call["id"]))  # add the tool's real result to the conversation, linked by id

final_response = llm_with_tools.invoke(messages)  # send the FULL conversation (question + AI's request + tool's real answer) back to the LLM
print(final_response.content)                     # LLM now writes a natural-language sentence using the real date it was given (step 4)