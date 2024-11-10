from fastapi import FastAPI

app = FastAPI(title="Backend", version="1.1.0.")

@app.get("/")
def index():
    return {"message": "Hello there your fastapi server is online"}