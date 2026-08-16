from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langgraph.graph import StateGraph, END
import sys
sys.path.append("../week4-Vector_DB")
from Mini_Project_4 import llm, get_current_date, add_numbers, search_civil_guru,tools_by_name
import re
import asyncio 
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

mcp_server = StdioServerParameters(
    command="python",
    args=["day05_minimal_mcp_server.py"],
)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    question_type: str
    retrieved_context: list[str]
    draft_answer: str
    is_verified: bool
    hallucinated_numbers: list[str]


async def call_llm(state: AgentState):
    messages = state["messages"]
    llm_with_tools = llm.bind_tools([get_current_date, add_numbers, search_civil_guru])
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response],"draft_answer": response.content}

async def execute_tools(state: AgentState):
    tool_calls = state["messages"][-1].tool_calls
    results = []
    for call in tool_calls:
        print(f"Tool called: {call['name']}")
        selected_tool = tools_by_name[call["name"]]
        result = await selected_tool.ainvoke(call["args"])
        print(f"Tool result: {result[:300]}")
        results.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return {"messages": results}

async def classify_question(state: AgentState) ->dict:
    question_text = state["messages"][-1].content
    if "fundamental right" in question_text.lower():
        return {"question_type": "fundamental_rights"}
    elif "directive principle" in question_text.lower():
        return {"question_type": "directive_principles"}
    else:
        return {"question_type": "general"}

async def retrieve_context(state: AgentState) -> dict:
    question_text = state["messages"][-1].content
    async with Client(stdio_client(mcp_server)) as client:
        result = await client.call_tool("search_civil_guru_mcp", {"question": question_text})
        retrieved_text = result.structured_content["result"]
    return {"retrieved_context": [retrieved_text]}

async def fact_check(state: AgentState) -> dict:
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

async def main():
    result = await app.ainvoke({"messages": [HumanMessage(content="What are the Fundamental Rights in the Indian Constitution?")]})
    print(result["messages"][-1].content)
    print("Is the answer verified?", result["is_verified"])
    print("Hallucinated numbers:", result["hallucinated_numbers"])


if __name__ == "__main__":
    asyncio.run(main())
    