import os
from typing import Annotated, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages, StateGraph
from langchain.agents import create_agent
from pydantic import BaseModel
from llm.gigachat import make_gigachat_model

from loguru import logger
from langchain_mcp_adapters.client import MultiServerMCPClient


mcp_url = os.getenv("MCP_URL", "http://localhost:8001/mcp")
client = MultiServerMCPClient({"default": {"url": mcp_url, "transport": "streamable-http"}})



ASSISTANT_PROMPT = """You are a helpful assistant that uses tools to answer questions."""

llm = make_gigachat_model()

# read from env

class AgentState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]


async def agent(state: AgentState) -> dict:
    logger.debug("Listing tools")
    tools = await client.get_tools(server_name="default")

    logger.debug("Got tools. len={len}", len=len(tools))
    _agent = create_agent(llm, tools, system_prompt=ASSISTANT_PROMPT)
    response = await _agent.ainvoke({"messages": state.messages})
    logger.info("Agent response: {response}", response=response)

    return {
        "messages": response["messages"]
    }


graph = StateGraph(AgentState)
graph.add_node("agent", agent)
graph.set_entry_point("agent")

app = graph.compile()