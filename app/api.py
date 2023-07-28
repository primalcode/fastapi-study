from fastapi import APIRouter

from app.endpoints import hero, trello

api_router = APIRouter()
api_router.include_router(hero.router, prefix="/heroes", tags=["heroes"])
api_router.include_router(trello.router, prefix="/trello", tags=["trello"])
