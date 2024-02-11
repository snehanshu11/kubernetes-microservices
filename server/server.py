from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id +100, "server":True,"client":False}

@app.get("/health")
async def health():
    return {"msg": "hello from server"}