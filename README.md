# A2A Playground

Bulding more complex scenarios on top of simpler ones for fun and profit.

## Reqs

The whole project is written in Python 3.13. It also uses `uv` as a package manager.

Upgrade to 3.14 seems to be problematic as of now due to dependencies incompatibility.

## LLM

All agents use Gigachat under the hood.
To connect to it, use env variables.

Basically one need to set exactly one env variable to connect:

```sh
GIGACHAT_CREDENTIALS=...
```

To configure the connection and parameters more thoroughly, use other variables, like `GIGACHAT_MODEL`, `GIGACHAT_BASE_URL` etc.
Example from GC docs:

```sh
# Auth
export GIGACHAT_CREDENTIALS="<your_authorization_key>"
export GIGACHAT_SCOPE="GIGACHAT_API_PERS"

# Connect
export GIGACHAT_BASE_URL="https://gigachat.devices.sberbank.ru/api/v1"
export GIGACHAT_TIMEOUT="60.0"
export GIGACHAT_VERIFY_SSL_CERTS="true" # or false if you know what you're doing.
# TLS: custom CA
export GIGACHAT_CA_BUNDLE_FILE="<your_ca_bundle_file>"

# Модель
export GIGACHAT_MODEL="GigaChat"

# Повтор попытки
export GIGACHAT_MAX_RETRIES="3"
export GIGACHAT_RETRY_BACKOFF_FACTOR="0.5"
```

## Agents

### Simple Agent

Basic agent to just have fun with it.

Stored at `simple_agent`.
To run it with langsmith, use the following:

```sh
> uv run langgraph dev --config langgraph.json
```

Then, in the LangSmith studio, make sure "simple_agent" is used in the tab you work in.

### Agent with MCP server

This example requires (as of now) to run two separate processes.

The first one is MCP server which emulates an interface over some e-com database.
The idea is inspired by one of the tutorials online.

MCP server is based on FastMCP library which does all the heavy lifting.
To run it, use special entry point:

```sh
> uv run run_sim_mcp_server.py
```

By default, server works on `http://localhost:8001/mcp`.



