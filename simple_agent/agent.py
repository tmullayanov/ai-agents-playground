from typing import Any
from langchain.agents import create_agent
from llm.gigachat import make_gigachat_model


ASSISTANT_PROMPT = """You are a helpful assistant that uses tools to answer questions."""


tools: list[Any] = []

llm = make_gigachat_model()
agent = create_agent(
    llm,
    system_prompt=ASSISTANT_PROMPT,
)