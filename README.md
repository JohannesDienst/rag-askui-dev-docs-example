# rag-askui-dev-docs-example

Little RAG example that pulls in the latest version of the [AskUI docs](https://docs.askui.com), creates embeddings for every Markdown file, feeds it to a vector store, connects an LLM, and finally exposes an API for querying it.

## Tech Stack - Local Development

* [SurrealDB](https://surrealdb.com/)
* [Langchain](https://www.langchain.com/)
* [Ollama](https://ollama.com/)
* [FastAPI](https://fastapi.tiangolo.com/)

## Local Usage

### Setup

1. Create virtual environment for python: `python -m venv venv`
2. Install all requirements: `pip install -r requirements.txt`
3. Install SurrealDB: `curl -sSf https://install.surrealdb.com | sh`
4. [Install Ollama](https://ollama.com/)

### Build Embeddings

1. Get the latest docs: `./checkout-latest-askui-dev-docs.sh`
2. Run SurrealDB in-memory: `./start-surreal.sh`
3. Run model `mistral`: `./start-ollama.sh`
4. Create embeddings and store them in SurrealDB: `./initialize_surrealdb.sh`

> ⚠️ **May take a few minutes!**

### Use

1. Run api on port `8001`: `./start-api.sh`
2. Open OpenAPI docs: `localhost:8001/docs`
3. Use the `generate` endpoint

## Tech Stack - Production - TO BE IMPLEMENTED

* [Pinecone](https://www.pinecone.io/)
* [Langchain](https://www.langchain.com/)
* [OpenAI](https://platform.openai.com/)
