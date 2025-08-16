from fastapi import APIRouter,Depends
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .. import schemas,models


router = APIRouter()

DBSession = Annotated[Session,Depends(get_db)]

@router.get("/pokemon")
async def get_pokemons(db:DBSession):
    pokemons = db.query(models.Pokemon_model).all()
    return pokemons

@router.get("/pokemonbyid")
async def get_pokemon_byID(id:int,db:DBSession):
    pokemon = db.query(models.Pokemon_model).filter(models.Pokemon_model.id == id).first()
    return pokemon

@router.get("/pokemonbyname")
async def get_pokemon_byname(name:str,db:DBSession):
    pokemon = db.query(models.Pokemon_model).filter(models.Pokemon_model.name == name).first()
    return pokemon

