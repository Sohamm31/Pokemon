from typing import List, Optional,Dict
from pydantic import BaseModel, EmailStr

class PokemonBase(BaseModel):
    name: str
    type1: str
    type2: Optional[str] = None
    HP: int
    Attack: int
    Defense: int
    Sp_Atk: int
    Sp_Def: int
    Speed: int
    Generation: int
    Legendary: bool


class BattleScoreBase(BaseModel):
    score: int

class BattleScore(BattleScoreBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True


class Pokemon(PokemonBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    battle_score: Optional[BattleScore] = None
    class Config:
        orm_mode = True

class PlayerProfile(BaseModel):
    level: int
    experience: int
    poke_coins: int
    pokeballs: Dict[str, int]
    class Config:
        orm_mode = True

class TeamCreate(BaseModel):
    name: str
    pokemon_ids: List[int] = []   

class Team(BaseModel):
    id: int
    name: str
    pokemons: List[Pokemon] = []

    class Config:
        orm_mode = True

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    pokemon_ids: Optional[List[int]] = []
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LeaderboardUser(BaseModel):
    username: str
    high_score: int

    class Config:
        orm_mode = True
