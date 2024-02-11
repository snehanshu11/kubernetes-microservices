from fastapi import FastAPI, status, HTTPException
import httpx
import os

app = FastAPI()

SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

@app.get("/get_item/{item_id}")
async def get_item(item_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVER_URL}/items/{item_id}")
            json_response = response.json()
            json_response["server"] = True
            json_response["client"] = True
            return json_response
        except Exception:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="server service is down")

@app.get("/health")
async def health():
    return {"msg": "hello from client"}