from mcp.server import MCPServer
import sys
sys.path.append("../week4-Vector_DB")
from Mini_Project_4 import llm, get_current_date, add_numbers, search_civil_guru,tools_by_name

mcp = MCPServer("CivilGuruSearch")

@mcp.tool()

def search_civil_guru_mcp(question: str) -> str:
    """Searches UPSC study material for relevant passages."""
    result = search_civil_guru.invoke({"question": question})
    return result

if __name__ == "__main__":
    mcp.run()
