from ..hashing import Hash
from ..database import get_db
from typing import Annotated,List
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,status
from ..schemas import User,UserCreate
from .. import models,token
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    tags=["User"]
)

DBSession = Annotated[Session,Depends(get_db)]

@router.post("/create_user")
async def create_user(request:UserCreate,db:DBSession):
    new_user = models.User_model(email = request.email,username = request.username,password = Hash.hashing(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(db:DBSession,request:OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User_model).filter(models.User_model.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Password Incorrect")
    
    access_token = token.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
    