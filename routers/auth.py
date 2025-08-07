from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from service.auth import AuthService , AccountService
from db.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schemas.auth import UserOut, Signup  , AccountOut , AccountUpdate
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials


router = APIRouter(tags=["Auth"], prefix="/auth")
auth_scheme = HTTPBearer()

@router.post("/signup", status_code=status.HTTP_200_OK, response_model=UserOut)
async def user_login(
        user: Signup,
        db: Session = Depends(get_db)):
    return await AuthService.signup(db, user)


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    return await AuthService.login(user_credentials, db)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
        refresh_token: str = Header(),
        db: Session = Depends(get_db)):
    return await AuthService.get_refresh_token(token=refresh_token, db=db)



@router.get("/", response_model=AccountOut)
def get_my_info(
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return AccountService.get_my_info(db, token)


@router.put("/", response_model=AccountOut)
def edit_my_info(
        updated_user: AccountUpdate,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return AccountService.edit_my_info(db, token, updated_user)

