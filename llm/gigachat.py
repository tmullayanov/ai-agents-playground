from functools import lru_cache
import ssl
from typing import TypedDict
from langchain_gigachat.chat_models import GigaChat as GigaChatModel
from gigachat import GigaChat as GigaChatAPI


class GCSettings(TypedDict):
    """Settings for GigaChat API."""

    base_url: str
    ca_bundle_file: str
    cert_file: str
    key_file: str
    model: str
    modelEmbedding: str
    scope: str
    profanity_check: bool
    timeout: int
    temperature: float
    verbose: bool
    max_tokens: int


@lru_cache
def make_chat_model_with_ssl_context(settings: GCSettings):
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.load_verify_locations(settings["ca_bundle_file"])
    ctx.load_cert_chain(certfile=settings["cert_file"], keyfile=settings["key_file"])

    llm = GigaChatModel(
        base_url=settings["base_url"],
        model=settings["model"],
        profanity_check=settings["profanity_check"],
        temperature=settings["temperature"],
        timeout=settings["timeout"],
        verbose=settings["verbose"],
        max_tokens=settings["max_tokens"],
        ssl_context=ctx,
        verify_ssl_certs=False,  # Не вшиваем в приложение серверный серт
        max_connections=1,  # pyright: ignore[reportCallIssue] parameter exists, it is passed via **kwargs
    )

    return llm


@lru_cache
def make_gigachat_model() -> GigaChatModel:
    return GigaChatModel(
        max_connections=1, # # pyright: ignore[reportCallIssue]
        verify_ssl_certs=False
    )


@lru_cache
def make_gigachat_api(credentials: str) -> GigaChatAPI:
    return GigaChatAPI(
        credentials=credentials, max_connections=1, verify_ssl_certs=False
    )
