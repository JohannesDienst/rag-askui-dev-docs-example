import asyncio

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_community.chat_models import ChatOllama

from initialize_surrealdb import get_db

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_prompt():
    return hub.pull("rlm/rag-prompt")

def get_vectorstore_retriever():
    db = get_db()
    return db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

def get_llm(model):
    return ChatOllama(model=model, temperature=0)

def generate_response(query="Answer my question?", model="mistral:latest", stream=True):
    prompt = create_prompt()
    retriever = get_vectorstore_retriever()
    llm = get_llm(model)

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    if stream is True:
        for chunk in rag_chain_with_source.stream(query):
            print(chunk)
    else:
        result = rag_chain_with_source.invoke(query)
        return result
