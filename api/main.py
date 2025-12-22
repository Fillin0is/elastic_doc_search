from fastapi import FastAPI


app = FastAPI()

@app.post("/search")
def search(query: str):
    pass