from fastapi import FastAPI

from search import search_documents, get_document_chunks


app = FastAPI()

@app.get("/")
def root():
    return {"message": "API работает"}

@app.get("/search")
def search(query: str):
    knn_documents = search_documents(query)
    full_documents = get_document_chunks(knn_documents)
    return full_documents