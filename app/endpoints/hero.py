from typing import List

from fastapi import APIRouter, Depends

from ..models.heroes import Hero
from ..services import hero_service
from app.auth.oauth2 import oauth2_scheme


router = APIRouter()


@router.get("/", name="list_heroes", response_model=List[Hero])
async def get_heroes(token: str = Depends(oauth2_scheme)):
    return hero_service.get_all_hero()


@router.get("/{hero_id}", response_model=Hero)
async def get_hero_by_id(hero_id: int):
    return hero_service.get_by_id(hero_id)


@router.put("/{hero_id}")
async def update_hero(hero_id: int):
    hero_service.update_hero(hero_id)


@router.post("/")
async def create_hero(hero: Hero):
    hero_service.create_hero(hero)


@router.put("/")
async def bulk_update():
    hero_service.bulk_update()


@router.delete("/{hero_id}")
async def delete(hero_id: int):
    hero_service.delete(hero_id)
