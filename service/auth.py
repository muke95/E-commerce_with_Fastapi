from fastapi import HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from model.models import User
from db.database import get_db
from core.security import verify_password, get_user_token, get_token_payload
from core.security import get_password_hash ,get_password_hash, get_token_payload
from utils.responses import ResponseHandler
from schemas.auth import Signup 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AccountService:
    @staticmethod
    def get_my_info(db: Session, token):
        user_id = get_token_payload(token.credentials).get('id')
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            ResponseHandler.not_found_error("User", user_id)
        return ResponseHandler.get_single_success(user.username, user.id, user)

    @staticmethod
    def edit_my_info(db: Session, token, updated_user):
        user_id = get_token_payload(token.credentials).get('id')
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        for key, value in updated_user.model_dump().items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return ResponseHandler.update_success(db_user.username, db_user.id, db_user)

    @staticmethod
    def remove_my_account(db: Session, token):
        user_id = get_token_payload(token.credentials).get('id')
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)
        db.delete(db_user)
        db.commit()
        return ResponseHandler.delete_success(db_user.username, db_user.id, db_user)


class AuthService:
    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = db.query(User).filter(User.username == user_credentials.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        return await get_user_token(id=user.id)

    @staticmethod
    async def signup(db: Session, user: Signup):
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        db_user = User(id=None, **user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)

    @staticmethod
    async def get_refresh_token(token, db):
        payload = get_token_payload(token)
        user_id = payload.get('id', None)
        if not user_id:
            raise ResponseHandler.invalid_token('refresh')

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResponseHandler.invalid_token('refresh')

        return await get_user_token(id=user.id, refresh_token=token)
    

    
