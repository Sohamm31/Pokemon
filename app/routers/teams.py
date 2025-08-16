# app/routers/teams.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/teams",  # All routes in this file will start with /teams
    tags=["Teams"]    # Group these endpoints in the API docs
)

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[models.User_model, Depends(oauth2.get_current_user)]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Team)
def create_team(
    request: schemas.TeamCreate, 
    db: DBSession, 
    current_user: CurrentUser
):
    """
    Create a new team for the currently authenticated user.
    The request body should contain the team's name and an optional list of pokemon_ids.
    """
    # Create the team instance
    new_team = models.Team(name=request.name, owner_id=current_user.id)
    
    # If pokemon_ids are provided, fetch them and add to the team
    if request.pokemon_ids:
        pokemons = db.query(models.Pokemon_model).filter(models.Pokemon_model.id.in_(request.pokemon_ids)).all()
        if len(pokemons) != len(request.pokemon_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more Pokémon IDs not found.")
        new_team.pokemons = pokemons
        
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@router.get("/", response_model=List[schemas.Team])
def get_user_teams(db: DBSession, current_user: CurrentUser):
    """
    Get a list of all teams owned by the currently authenticated user.
    """
    teams = db.query(models.Team).filter(models.Team.owner_id == current_user.id).all()
    return teams


@router.delete("/{team_id}",status_code=200)
def delete_team(team_id: int, db: DBSession, current_user: CurrentUser):
    """
    Delete a team by its ID. Users can only delete their own teams.
    """
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found.")
        
    if team.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    
    # delete all team_pokemon entries first
    db.query(models.team_pokemon).filter(models.team_pokemon.c.team_id == team_id).delete()
    db.delete(team)
    db.commit()
    return {"detail": f"Team {team_id} deleted successfully"}


@router.put("/{team_id}", response_model=schemas.Team)
async def update_team(
    team_id: int, 
    team_update: schemas.TeamUpdate, 
    db: DBSession, 
    current_user: CurrentUser  # ✅ Enforce logged-in user
):
    # Get the team
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if team.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this team")

    # Update team name if provided
    if team_update.name:
        team.name = team_update.name

    # If pokemon_ids provided, update association
    if team_update.pokemon_ids is not None:
        # Clear existing pokemons
        db.query(models.team_pokemon).filter(models.team_pokemon.c.team_id == team_id).delete()

        # Add new pokemons
        for pid in team_update.pokemon_ids:
            pokemon = db.query(models.Pokemon_model).filter(models.Pokemon_model.id == pid).first()
            if not pokemon:
                raise HTTPException(status_code=404, detail=f"Pokemon with id {pid} not found")
            db.execute(models.team_pokemon.insert().values(team_id=team.id, pokemon_id=pid))

    db.commit()
    db.refresh(team)
    return team
