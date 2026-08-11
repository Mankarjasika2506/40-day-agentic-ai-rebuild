from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langgraph.graph import StateGraph, END
import sys
sys.path.append("../week4-Vector_DB")
from Mini_Project_4 import llm, get_current_date, add_numbers, search_civil_guru,tools_by_name
import re


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    question_type: str
    retrieved_context: list[str]
    draft_answer: str
    is_verified: bool
    hallucinated_numbers: list[str]


def call_llm(state: AgentState):
    messages = state["messages"]
    llm_with_tools = llm.bind_tools([get_current_date, add_numbers, search_civil_guru])
    response = llm_with_tools.invoke(messages)
    return {"messages": [response],"draft_answer": response.content}

def execute_tools(state: AgentState):
    tool_calls = state["messages"][-1].tool_calls
    results = []
    for call in tool_calls:
        print(f"Tool called: {call['name']}")
        selected_tool = tools_by_name[call["name"]]
        result = selected_tool.invoke(call["args"])
        print(f"Tool result: {result[:300]}")
        results.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return {"messages": results}

def classify_question(state: AgentState) ->dict:
    question_text = state["messages"][-1].content
    if "fundamental right" in question_text.lower():
        return {"question_type": "fundamental_rights"}
    elif "directive principle" in question_text.lower():
        return {"question_type": "directive_principles"}
    else:
        return {"question_type": "general"}

def retrieve_context(state: AgentState) -> dict:
    question_text = state["messages"][-1].content
    results = search_civil_guru.invoke({"question": question_text})
    return {"retrieved_context": [results]}

def fact_check(state: AgentState) -> dict:
    draft_answer = state["draft_answer"]
    context_text = "\n\n".join(state["retrieved_context"])
    
    
    draft_numbers = re.findall(r"Articles?\s(\d+)", draft_answer)
    context_numbers = re.findall(r"Articles?\s(\d+)", context_text)
    
    hallucinated = []
    for num in draft_numbers:
        if num not in context_numbers:
            hallucinated.append(num)
    
    is_verified = len(hallucinated) == 0
    
    return {"is_verified": is_verified, "hallucinated_numbers": hallucinated}
    
graph = StateGraph(AgentState)
graph.add_node("call_llm", call_llm)
graph.add_node("execute_tools", execute_tools)
graph.add_node("classify_question", classify_question)
graph.add_node("retrieve_context", retrieve_context)
graph.add_node("fact_check", fact_check)
graph.set_entry_point("classify_question")
graph.add_edge("classify_question", "retrieve_context")
graph.add_edge("retrieve_context", "call_llm")
graph.add_edge("execute_tools", "call_llm")


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "execute_tools"  
    else:
        return "end"  
    
graph.add_conditional_edges(
    "call_llm",
    should_continue,
    {"execute_tools": "execute_tools", "end": "fact_check"}
)
graph.add_edge("fact_check", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"messages": [HumanMessage(content="What are the Fundamental Rights in the Indian Constitution?")]})
    print(result["messages"][-1].content)
    print("Is the answer verified?", result["is_verified"])
    print("Hallucinated numbers:", result["hallucinated_numbers"])


