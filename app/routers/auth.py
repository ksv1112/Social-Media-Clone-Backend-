from fastapi import FastAPI, Response, status ,HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app import utils, oauth2


router = APIRouter(
    tags= ["Authentication"]
)

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Invalid credentials")

    # Create a token
    # Return the token

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

