from sqlalchemy.orm import Session
from model.models import User
from schemas.usersService import UserCreate, UserUpdate
from utils.responses import ResponseHandler
from core.security import get_password_hash
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def get_all_users(db: Session, page: int, limit: int, search: str = "", role: str = "user"):
        users = db.query(User).order_by(User.id.asc()).filter(
            User.username.contains(search), User.role == role).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} users", "data": users}

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            ResponseHandler.not_found_error("User", user_id)
            # Remove password before sending the response
        user_dict = user.__dict__.copy()
        user_dict.pop("password", None)
        return ResponseHandler.get_single_success(user.username, user_id, [user_dict])

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # Check if email already exists
        existing_user_email = db.query(User).filter(User.email == user.email).first()
        if existing_user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        existing_user_username = db.query(User).filter(User.username == user.username).first()
        if existing_user_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Proceed to create user
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        db_user = User(id=None, **user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)
        

    @staticmethod
    def update_user(db: Session, user_id: int, updated_user: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        for key, value in updated_user.model_dump().items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return ResponseHandler.update_success(db_user.username, db_user.id, db_user)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)
        db.delete(db_user)
        db.commit()
        return ResponseHandler.delete_success(db_user.username, db_user.id, [db_user])
