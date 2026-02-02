from fastapi import FastAPI
from rag import chatbot


app = FastAPI()


@app.get("/")
def health():
    return {'200' : "Okay"}


@app.post("/api/rag")
def query(query):
    return chatbot(query)
