from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship

# Association table for Many-to-Many
team_pokemon = Table(
    "team_pokemon",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
    Column("pokemon_id", Integer, ForeignKey("pokemon_model.id"), primary_key=True)
)

class Pokemon_model(Base):
    __tablename__ = "pokemon_model"

    id = Column(Integer, primary_key=True, index=True)
    pokedex_id = Column(Integer, index=True)
    name = Column(String(100))
    type1 = Column(String(50))
    type2 = Column(String(50), nullable=True)
    HP = Column(Integer)
    Attack = Column(Integer)
    Defense = Column(Integer)
    Sp_Atk = Column(Integer)
    Sp_Def = Column(Integer)
    Speed = Column(Integer)
    Generation = Column(Integer)
    Legendary = Column(Boolean)

    # M2M with Team
    teams = relationship("Team", secondary=team_pokemon, back_populates="pokemons")


class User_model(Base):
    __tablename__ = "user_model"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))  
    # One-to-Many with Team
    teams = relationship("Team", back_populates="owner")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    owner_id = Column(Integer, ForeignKey("user_model.id"))
    
    # Many-to-One with User_model
    owner = relationship("User_model", back_populates="teams")

    # Many-to-Many with Pokemon_model
    pokemons = relationship("Pokemon_model", secondary=team_pokemon, back_populates="teams")
