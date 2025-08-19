import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import joblib
from typing import Annotated

from .. import models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

# Using your specified paths for the models
modelpath = "app/ml_models/battle_predictor.pkl"
encoderpath = "app/ml_models/type_encoder.pkl"

# --- Load Models ---
try:
    model = joblib.load(modelpath)
    type_encoder = joblib.load(encoderpath)
    print("ML model and encoder loaded successfully.")
except FileNotFoundError:
    model = None
    type_encoder = None
    print(f"Error: Could not find model files at {modelpath} or {encoderpath}. Prediction endpoint will be disabled.")

# --- Schemas ---
class BattleRequest(BaseModel):
    pokemon1_id: int
    pokemon2_id: int

# --- Dependencies ---
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[models.User_model, Depends(oauth2.get_current_user)]


@router.post("/battle/")
def predict_battle_winner(
    request: BattleRequest,
    db: DBSession,
    current_user: CurrentUser
):
    if not model or not type_encoder:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction service is not available. Model has not been trained or loaded."
        )

    # Fetch Pokémon from the database
    p1 = db.query(models.Pokemon_model).filter(models.Pokemon_model.id == request.pokemon1_id).first()
    p2 = db.query(models.Pokemon_model).filter(models.Pokemon_model.id == request.pokemon2_id).first()

    if not p1 or not p2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more Pokémon not found.")

    # --- Preprocess data for prediction (using the simple, raw stats) ---
    data = {
        'p1_HP': [p1.HP], 'p1_Attack': [p1.Attack], 'p1_Defense': [p1.Defense], 'p1_Speed': [p1.Speed],
        'p1_Type 1': [p1.type1], 'p1_Type 2': [p1.type2 if p1.type2 else 'None'],
        'p2_HP': [p2.HP], 'p2_Attack': [p2.Attack], 'p2_Defense': [p2.Defense], 'p2_Speed': [p2.Speed],
        'p2_Type 1': [p2.type1], 'p2_Type 2': [p2.type2 if p2.type2 else 'None'],
    }
    battle_df = pd.DataFrame(data)

    try:
        battle_df['p1_Type 1_encoded'] = type_encoder.transform(battle_df['p1_Type 1'])
        battle_df['p1_Type 2_encoded'] = type_encoder.transform(battle_df['p1_Type 2'])
        battle_df['p2_Type 1_encoded'] = type_encoder.transform(battle_df['p2_Type 1'])
        battle_df['p2_Type 2_encoded'] = type_encoder.transform(battle_df['p2_Type 2'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Pokémon type found: {e}")

    # The list of features the old model expects
    features = [
        'p1_HP', 'p1_Attack', 'p1_Defense', 'p1_Speed', 'p1_Type 1_encoded', 'p1_Type 2_encoded',
        'p2_HP', 'p2_Attack', 'p2_Defense', 'p2_Speed', 'p2_Type 1_encoded', 'p2_Type 2_encoded'
    ]
    X_predict = battle_df[features]

    # --- Make Prediction ---
    prediction = model.predict(X_predict)
    prediction_proba = model.predict_proba(X_predict)

    winner_index = prediction[0]
    win_probability = prediction_proba[0][winner_index]

    winner = p1 if winner_index == 0 else p2
    
    return {
        "pokemon1": p1.name,
        "pokemon2": p2.name,
        "predicted_winner": winner.name,
        "win_probability": f"{win_probability:.2f}"
    }
