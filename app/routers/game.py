from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/game",
    tags=["Game & Shop"]
)

# --- Dependencies ---
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[models.User_model, Depends(oauth2.get_current_user)]

# --- Game Data ---
POKEBALL_PRICES = {
    "pokeball": 200,
    "greatball": 600,
    "ultraball": 1200
}

# --- Schemas ---
class ExperienceUpdate(BaseModel):
    xp: int
    
class CoinsUpdate(BaseModel):
    coins: int

class PurchaseRequest(BaseModel):
    item_name: str
    quantity: int

def xp_for_level(level: int) -> int:
    """Calculates the total XP needed to reach the next level."""
    return 100 * (level ** 2)

# --- Endpoints ---

@router.get("/profile", response_model=schemas.PlayerProfile)
def get_player_profile(db: DBSession, current_user: CurrentUser):
    """Gets the current user's game profile, creating one if it doesn't exist."""
    profile = db.query(models.PlayerProfile).filter(models.PlayerProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.PlayerProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.post("/xp", response_model=schemas.PlayerProfile)
def add_experience(xp_update: ExperienceUpdate, db: DBSession, current_user: CurrentUser):
    """Adds experience to the user's profile and handles leveling up."""
    profile = db.query(models.PlayerProfile).filter(models.PlayerProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player profile not found.")
        
    profile.experience += xp_update.xp
    
    xp_needed = xp_for_level(profile.level)
    while profile.experience >= xp_needed:
        profile.level += 1
        profile.experience -= xp_needed
        xp_needed = xp_for_level(profile.level)
        
    db.commit()
    db.refresh(profile)
    return profile

# --- NEW Endpoint to add PokéCoins ---
@router.post("/coins", response_model=schemas.PlayerProfile)
def add_pokecoins(coins_update: CoinsUpdate, db: DBSession, current_user: CurrentUser):
    """Adds PokéCoins to the user's profile."""
    profile = db.query(models.PlayerProfile).filter(models.PlayerProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player profile not found.")
        
    profile.poke_coins += coins_update.coins
    db.commit()
    db.refresh(profile)
    return profile

# --- NEW Endpoint for the Shop ---
@router.post("/buy", response_model=schemas.PlayerProfile)
def buy_items(request: PurchaseRequest, db: DBSession, current_user: CurrentUser):
    """Allows a user to buy Pokéballs with their PokéCoins."""
    if request.item_name not in POKEBALL_PRICES or request.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item or quantity.")

    profile = db.query(models.PlayerProfile).filter(models.PlayerProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player profile not found.")
        
    total_cost = POKEBALL_PRICES[request.item_name] * request.quantity
    if profile.poke_coins < total_cost:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough PokéCoins.")

    profile.poke_coins -= total_cost
    
    # Safely update the JSON 'pokeballs' field
    new_pokeballs = profile.pokeballs.copy()
    new_pokeballs[request.item_name] = new_pokeballs.get(request.item_name, 0) + request.quantity
    profile.pokeballs = new_pokeballs

    db.commit()
    db.refresh(profile)
    return profile
