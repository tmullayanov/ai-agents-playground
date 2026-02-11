from typing import Annotated, Sequence

from loguru import logger
from pydantic import BaseModel, Field
from .downloader import load_file
from llm.gigachat import make_gigachat_model
from langchain_core.runnables.config import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, add_messages

load_dotenv(override=True)  # pyright: ignore[reportUnusedCallResult]


llm = make_gigachat_model()

class AgentState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    document_urls: list[str] = Field(default_factory=lambda: [])

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Ты - помощник пользователя. Четко выполняй его инструкции"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

ai = prompt | llm

def agent(state: AgentState, config: RunnableConfig) -> dict:
    logger.debug("Agent node invoked")
    uploads = []
    logger.debug(f"{state=}")
    try:
        logger.debug("Checking document_urls")
        if state.document_urls:
            logger.debug("Found document_urls")
            for url in state.document_urls:
                print(f"Processing document: {url}")
                (name, contents, type) = load_file(url)

                uploaded_id = llm.upload_file(
                    file=(name, contents, type),
                    purpose="general"
                )
                uploads.append(uploaded_id)
                print(f"Uploaded file: {uploaded_id}")

        state.messages[-1].additional_kwargs["attachments"] = [u.id_ for u in uploads]

        response = ai.invoke({"messages": state.messages})
        return {"messages": [response]}
            
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"messages": [AIMessage(content=f"Error during request: {e}")]}
    finally:
        logger.debug("Deleting uploaded files if any")
        client = llm._client
        for upload in uploads:
            logger.debug(f"Deleting id={upload.id_}")
            client.delete_file(upload.id_)


workflow = StateGraph(AgentState)
workflow.add_node("agent", agent)

workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

app = workflow.compile()