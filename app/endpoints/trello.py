import httpx
from fastapi import APIRouter
from starlette.config import Config

router = APIRouter()
config = Config('.env')


@router.get("/", name="trello_index")
async def index():
    print(f"TRELLO_API_KEY : {config('TRELLO_API_KEY')}")
    print(f"TRELLO_SECRET : {config('TRELLO_SECRET')}")
    print(f"TRELLO_SECRET : {config('TRELLO_TOKEN')}")

    api_key = config('TRELLO_API_KEY')
    api_token = config('TRELLO_TOKEN')
    board_id = config('TRELLO_BOARD')

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.trello.com/1/boards/{board_id}",
                                    params={"key": api_key, "token": api_token})
    response.raise_for_status()  # Will raise an exception for non-200 status codes
    print(f"response: {response.text}")
    return response.json()
