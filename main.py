from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/sample")
async def sample():
    return {"sample"}


@app.get("/query-param")
async def query_param(param1: str, param2: int):
    return {"message": f"param1 : {param1}, param2 : {param2}"}
