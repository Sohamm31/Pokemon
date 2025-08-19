import random
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated, List

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/safari",
    tags=["Safari & Collection"]
)

# --- Dependencies ---
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[models.User_model, Depends(oauth2.get_current_user)]

# --- Game Data ---
BASE_CATCH_RATES = { 'Bulbasaur': 45, 'Ivysaur': 45, 'Venusaur': 45, 'Charmander': 45, 'Charmeleon': 45, 'Charizard': 45, 'Squirtle': 45, 'Wartortle': 45, 'Blastoise': 45, 'Caterpie': 255, 'Metapod': 120, 'Butterfree': 45, 'Weedle': 255, 'Kakuna': 120, 'Beedrill': 45, 'Pidgey': 255, 'Pidgeotto': 120, 'Pidgeot': 45, 'Rattata': 255, 'Raticate': 127, 'Spearow': 255, 'Fearow': 90, 'Ekans': 255, 'Arbok': 90, 'Pikachu': 190, 'Raichu': 75, 'Sandshrew': 255, 'Sandslash': 90, 'Nidoran♀': 235, 'Nidorina': 120, 'Nidoqueen': 45, 'Nidoran♂': 235, 'Nidorino': 120, 'Nidoking': 45, 'Clefairy': 150, 'Clefable': 25, 'Vulpix': 190, 'Ninetales': 75, 'Jigglypuff': 170, 'Wigglytuff': 50, 'Zubat': 255, 'Golbat': 90, 'Oddish': 255, 'Gloom': 120, 'Vileplume': 45, 'Paras': 190, 'Parasect': 75, 'Venonat': 190, 'Venomoth': 75, 'Diglett': 255, 'Dugtrio': 50, 'Meowth': 255, 'Persian': 90, 'Psyduck': 190, 'Golduck': 75, 'Mankey': 190, 'Primeape': 75, 'Growlithe': 190, 'Arcanine': 75, 'Poliwag': 255, 'Poliwhirl': 120, 'Poliwrath': 45, 'Abra': 200, 'Kadabra': 100, 'Alakazam': 50, 'Machop': 180, 'Machoke': 90, 'Machamp': 45, 'Bellsprout': 255, 'Weepinbell': 120, 'Victreebel': 45, 'Tentacool': 190, 'Tentacruel': 60, 'Geodude': 255, 'Graveler': 120, 'Golem': 45, 'Ponyta': 190, 'Rapidash': 60, 'Slowpoke': 190, 'Slowbro': 75, 'Magnemite': 190, 'Magneton': 60, 'Farfetch’d': 45, 'Doduo': 190, 'Dodrio': 45, 'Seel': 190, 'Dewgong': 75, 'Grimer': 190, 'Muk': 75, 'Shellder': 190, 'Cloyster': 60, 'Gastly': 190, 'Haunter': 90, 'Gengar': 45, 'Onix': 45, 'Drowzee': 190, 'Hypno': 75, 'Krabby': 225, 'Kingler': 60, 'Voltorb': 190, 'Electrode': 60, 'Exeggcute': 90, 'Exeggutor': 45, 'Cubone': 190, 'Marowak': 75, 'Hitmonlee': 45, 'Hitmonchan': 45, 'Lickitung': 45, 'Koffing': 190, 'Weezing': 60, 'Rhyhorn': 120, 'Rhydon': 60, 'Chansey': 30, 'Tangela': 45, 'Kangaskhan': 45, 'Horsea': 225, 'Seadra': 75, 'Goldeen': 225, 'Seaking': 60, 'Staryu': 225, 'Starmie': 60, 'Mr. Mime': 45, 'Scyther': 45, 'Jynx': 45, 'Electabuzz': 45, 'Magmar': 45, 'Pinsir': 45, 'Tauros': 45, 'Magikarp': 255, 'Gyarados': 45, 'Lapras': 45, 'Ditto': 35, 'Eevee': 45, 'Vaporeon': 45, 'Jolteon': 45, 'Flareon': 45, 'Porygon': 45, 'Omanyte': 45, 'Omastar': 45, 'Kabuto': 45, 'Kabutops': 45, 'Aerodactyl': 45, 'Snorlax': 25, 'Articuno': 3, 'Zapdos': 3, 'Moltres': 3, 'Dratini': 45, 'Dragonair': 45, 'Dragonite': 45, 'Mewtwo': 3, 'Mew': 45 }
POKEMON_TIERS = {
    "common": [10, 13, 16, 19, 21, 23, 27, 29, 32, 35, 37, 39, 41, 43, 46, 48, 50, 52, 54, 56, 58, 60, 63, 66, 69, 72, 74, 77, 79, 81, 83, 84, 86, 88, 90, 92, 96, 98, 100, 102, 104, 109, 111, 114, 116, 118, 120, 129, 133, 138, 140, 147],
    "uncommon": [1, 4, 7, 11, 14, 17, 20, 22, 24, 26, 28, 31, 34, 36, 38, 40, 42, 44, 47, 49, 51, 53, 55, 57, 59, 61, 64, 67, 70, 73, 75, 78, 80, 82, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 108, 110, 112, 113, 115, 117, 119, 121, 122, 123, 124, 125, 126, 127, 128, 131, 132, 137, 139, 141, 142, 148],
    "rare": [2, 5, 8, 3, 6, 9, 12, 15, 18, 143, 149],
    "legendary": [144, 145, 146, 150, 151]
}
SPAWN_CHANCES = {"common": 0.70, "uncommon": 0.20, "rare": 0.09, "legendary": 0.01}
THROW_MULTIPLIERS = {
    "bad": 0.25,      # Significant penalty
    "okay": 1.5,      # No bonus, standard throw
    "excellent": 2.5  # Significant bonus
}
BALL_MULTIPLIERS = {"pokeball": 1.0, "greatball": 1.5, "ultraball": 2.0}

# --- Schemas ---
class CatchRequest(BaseModel):
    pokemon_id: int
    throw_quality: str
    ball_type: str # Added ball_type

class StarterRequest(BaseModel):
    pokemon_id: int

# --- Endpoints ---

@router.get("/collection", response_model=List[schemas.Pokemon])
def get_user_collection(current_user: CurrentUser):
    return current_user.collection

@router.post("/starter", status_code=status.HTTP_201_CREATED)
def choose_starter(request: StarterRequest, db: DBSession, current_user: CurrentUser):
    if request.pokemon_id not in [1, 4, 7]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid starter Pokémon ID.")
    if len(current_user.collection) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Starter has already been chosen.")
    starter_pokemon = db.query(models.Pokemon_model).filter(models.Pokemon_model.id == request.pokemon_id).first()
    if not starter_pokemon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Starter Pokémon not found.")
    profile = db.query(models.PlayerProfile).filter(models.PlayerProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.PlayerProfile(user_id=current_user.id)
        db.add(profile)
    current_user.collection.append(starter_pokemon)
    db.commit()
    return {"message": f"{starter_pokemon.name} has been added to your collection!"}

@router.get("/encounter", response_model=schemas.Pokemon)
def get_wild_pokemon_encounter(db: DBSession, current_user: CurrentUser):
    # This logic remains the same
    tiers = list(SPAWN_CHANCES.keys())
    chances = list(SPAWN_CHANCES.values())
    chosen_tier = random.choices(tiers, weights=chances, k=1)[0]
    available_ids = POKEMON_TIERS[chosen_tier]
    caught_ids = {p.id for p in current_user.collection}
    uncaught_in_tier = [pid for pid in available_ids if pid not in caught_ids]
    if not uncaught_in_tier:
        if chosen_tier == "legendary": chosen_tier = "rare"
        if chosen_tier == "rare": chosen_tier = "uncommon"
        if chosen_tier == "uncommon": chosen_tier = "common"
        uncaught_in_tier = [pid for pid in POKEMON_TIERS[chosen_tier] if pid not in caught_ids]
    if not uncaught_in_tier:
        raise HTTPException(status_code=404, detail="You've caught all available Pokémon!")
    wild_pokemon_id = random.choice(uncaught_in_tier)
    return db.query(models.Pokemon_model).filter(models.Pokemon_model.id == wild_pokemon_id).first()

@router.post("/catch")
def attempt_catch(request: CatchRequest, db: DBSession, current_user: CurrentUser):
    if request.throw_quality not in THROW_MULTIPLIERS or request.ball_type not in BALL_MULTIPLIERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid throw or ball type.")

    pokemon_to_catch = db.query(models.Pokemon_model).filter(models.Pokemon_model.id == request.pokemon_id).first()
    if not pokemon_to_catch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokémon not found.")

    profile = db.query(models.PlayerProfile).filter(models.PlayerProfile.user_id == current_user.id).first()
    if not profile or profile.pokeballs.get(request.ball_type, 0) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No {request.ball_type}s left!")

    # Use one ball
    new_pokeballs = profile.pokeballs.copy()
    new_pokeballs[request.ball_type] -= 1
    profile.pokeballs = new_pokeballs

    base_rate = BASE_CATCH_RATES.get(pokemon_to_catch.name.strip(), 45)
    throw_bonus = THROW_MULTIPLIERS[request.throw_quality]
    ball_bonus = BALL_MULTIPLIERS[request.ball_type]
    
    # Final formula
    catch_chance = (base_rate / 255) * throw_bonus * ball_bonus

    if random.random() < catch_chance:
        current_user.collection.append(pokemon_to_catch)
        db.commit()
        return {"caught": True, "pokemon_name": pokemon_to_catch.name, "balls_left": new_pokeballs}
    else:
        db.commit()
        return {"caught": False, "pokemon_name": pokemon_to_catch.name, "balls_left": new_pokeballs}
