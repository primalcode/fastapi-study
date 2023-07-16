from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/query-param")
async def query_param(param1: Optional[str] = None, param2: int = 1):
    return {"message": f"param1 : {param1}, param2 : {param2}"}
