from fastapi import APIRouter, Depends, Query, status
from db.database import get_db
from service.users import UserService
from sqlalchemy.orm import Session
# from schemas.usersService import UserCreate, UserOut, UsersOut, UserOutDelete, UserUpdate
from schemas.usersService import UsersOut ,UserCreate,UserOutDelete
# from app.core.security import check_admin_role


router = APIRouter(tags=["Users"], prefix="/users")


# Get All Users
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UsersOut,
    #dependencies=[Depends(check_admin_role)]
    )
def get_all_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based username"),
    role: str = Query("user", enum=["user", "admin"])
):
    return UserService.get_all_users(db, page, limit, search, role)

#Create User
@router.post("/create",status_code=status.HTTP_201_CREATED)
def create_user(user : UserCreate,db:Session = Depends(get_db)):
    return UserService.create_user(db , user)

# Get User by id
@router.get("/{user_id}",status_code=status.HTTP_200_OK,response_model=UsersOut)
def get_user(user_id : int , db : Session = Depends(get_db)):
    return UserService.get_user(db,user_id)

# Delete User by id
@router.delete("/{user_id}",status_code=status.HTTP_200_OK,response_model=UserOutDelete)
def get_user(user_id : int , db : Session = Depends(get_db)):
    return UserService.delete_user(db,user_id)