# load_data.py

import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Check if DATABASE_URL exists before continuing
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ ERROR: DATABASE_URL is not set. Please check your .env file.")
    print("Tip: Add a .env file in your project root with:")
    print("DATABASE_URL=sqlite:///./pokemon.db")
    sys.exit(1)

# Import after confirming DATABASE_URL exists
from app.database import SessionLocal
from app.models import Pokemon_model

db = SessionLocal()

# --- Data Loading and Cleaning ---
df = pd.read_csv("Pokemon/pokemon_data.csv")

column_mapping = {
    '#': 'id',
    'Name': 'name',
    'Type 1': 'type1',
    'Type 2': 'type2',
    'HP': 'HP',
    'Attack': 'Attack',
    'Defense': 'Defense',
    'Sp. Atk': 'Sp_Atk',
    'Sp. Def': 'Sp_Def',
    'Speed': 'Speed',
    'Generation': 'Generation',
    'Legendary': 'Legendary'
}
df = df.rename(columns=column_mapping)

df['type2'] = df['type2'].where(pd.notna(df['type2']), None)

print("Starting to load Pokémon data into the database...")
df.columns = df.columns.str.strip()

print(df.columns)


for _, row in df.iterrows():
    pokemon_record = Pokemon_model(
        pokedex_id=row["id"],
        name=row['name'],
        type1=row['type1'],
        type2=row['type2'],
        HP=row['HP'],
        Attack=row['Attack'],
        Defense=row['Defense'],
        Sp_Atk=row['Sp_Atk'],
        Sp_Def=row['Sp_Def'],
        Speed=row['Speed'],
        Generation=row['Generation'],
        Legendary=row['Legendary']
    )
    db.add(pokemon_record)

try:
    db.commit()
    print(f"✅ Successfully loaded {len(df)} Pokémon records into the database.")
except Exception as e:
    db.rollback()
    print(f"❌ An error occurred while inserting data: {e}")
finally:
    db.close()
