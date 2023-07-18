from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ShopInfo(BaseModel):
    name: str
    location: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    tax: Optional[float] = None


class Data(BaseModel):
    shop_info: Optional[ShopInfo]
    items: List[Item]


@app.get("/query-param")
async def query_param(param1: Optional[str] = None, param2: int = 1):
    return {"message": f"param1 : {param1}, param2 : {param2}"}
# 単純にparam1を返却するとnull，上記のように返却するとNoneとなる


@app.post("/")
async def index(data: Data):
    return {"data": data}
