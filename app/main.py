from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .routers import pokemon,users,teams
from .database import engine
from . import models


app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(pokemon.router)
app.include_router(users.router)
app.include_router(teams.router)


app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('app/static/index.html')

@app.get("/")
async def read_route():
    return {"Message":"Pokemon server started"}

