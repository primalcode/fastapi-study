from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session, select

app = FastAPI()


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


class ShopInfo(BaseModel):
    name: str
    location: str


class Item(BaseModel):
    name: str = Field(min_length=4, max_length=12)
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

# localhostと書くと繋がらない
engine = create_engine('mysql://yoshima:yoshima@127.0.0.1:3306/study_fastapi_db')


@app.post("/")
async def index(data: Data):
    return {"data": data}


@app.get("/heroes")
async def get_heroes():
    with Session(engine) as session:
        stmt = select(Hero)
        results = session.exec(stmt)
    return {"results": results}


@app.post("/hero")
async def create_hero(hero: Hero):
    with Session(engine) as session:
        print(f"追加前ID：{hero.id}")
        session.add(hero)
        print(f"追加後ID：{hero.id}")

        print(f"コミット前ID：{hero.id}")
        session.commit()
        print(f"コミット後ID：{hero.id}")

        # コミット後でIDは最新の状態になっているので，不要な気がする．．．
        print(f"反映前ID：{hero.id}")
        session.refresh(hero)
        print(f"反映後ID：{hero.id}")

    return {"success"}
