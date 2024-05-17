from fastapi import FastAPI
from prompt_llm import generate_response

from pydantic import BaseModel

class Answer(BaseModel):
    answer: str

class Query(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate")
async def generate(query: Query):
    llm_response = generate_response(query.query, "mistral:latest", stream=False)
    answer = Answer(answer=llm_response["answer"])
    return answer