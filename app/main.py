from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import pokemon, users, teams,battle,score

# This line creates the database tables (if they don't exist)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory which will contain all your HTML files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- UPDATED ROUTING FOR SEPARATE HTML FILES ---

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('app/static/landing.html')

@app.get("/pokedex.html", include_in_schema=False)
async def read_pokedex():
    return FileResponse('app/static/pokedex.html')

@app.get("/teams.html", include_in_schema=False)
async def read_teams():
    return FileResponse('app/static/teams.html')

@app.get("/auth.html", include_in_schema=False)
async def read_auth():
    return FileResponse('app/static/auth.html')

@app.get("/battle.html", include_in_schema=False)
async def read_battle():
    return FileResponse('app/static/battle.html')
# Include all the API routers
app.include_router(pokemon.router)
app.include_router(users.router)
app.include_router(teams.router)
app.include_router(battle.router) 
app.include_router(score.router) 


