from typing import List, Tuple
import asyncio

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import SurrealDBStore
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

ollama_embeddings = None

def get_ollama_embeddings(model="mistral:latest"):
   global ollama_embeddings
   ollama_embeddings = OllamaEmbeddings(
      model=model,
    )
   return ollama_embeddings

db = None

def get_db(model="mistral:latest"):
  global db
  if db is None:
    db = SurrealDBStore(
      dburl="ws://localhost:8000/rpc",  # url for the hosted SurrealDB database
      embedding_function=get_ollama_embeddings(model=model),
      db_user="root",  # SurrealDB credentials if needed: db username
      db_pass="root",  # SurrealDB credentials if needed: db password
      ns="langchain", # namespace to use for vectorstore
      db="database",  # database to use for vectorstore
      collection="documents", #collection to use for vectorstore
    )     
  return db

async def initialize_empty_surrealdb_store(model="mistral:latest"):
  db = get_db(model=model)
  await db.initialize()
  await db.adelete()

# add documents to the vectorstore
async def add_documents(docs=[], model="mistral:latest"):
  # this is needed to initialize the underlying async library for SurrealDB
  db = get_db(model=model);
  await db.initialize()
  await db.aadd_documents(docs)

def main() -> None:
    asyncio.run(initialize_empty_surrealdb_store(model="mistral:latest"))

    loader = DirectoryLoader("./documents_to_import", glob="**/*.md", loader_cls=TextLoader )
    documents = loader.load()

    print(f"Found {len(documents)} documents to import.")

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    counter = 0
    for document in documents:
      counter += 1
      print(f"Processing document {counter} of {len(documents)}")
      md_header_splits = markdown_splitter.split_text(document.page_content)
      asyncio.run(add_documents(docs=md_header_splits, model="mistral:latest"))

if __name__ == "__main__":
    main()