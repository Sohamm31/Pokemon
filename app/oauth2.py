from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import token, models, database, schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    db: Session = Depends(database.get_db), 
    data: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = token.verify_token(data, credentials_exception)

    # fetch user from DB using username
    user = db.query(models.User_model).filter(models.User_model.username == token_data.username).first()

    if user is None:
        raise credentials_exception

    return user   # ⚡ return actual User model, not TokenData
