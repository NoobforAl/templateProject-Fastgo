"""This is simple Authenticate app!
    """

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from .dependencies import get_db, verify_password
from .dependencies import get_password_hash
from .schemas import Login, Register, Users
from .models import User, Base
from .config import AuthJWT

from sqlalchemy.orm import Session
from app.database import engine

from datetime import timedelta
from typing import List, Dict


Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post('/login')
def login(
    req: Login,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    user: User = db.query(User).filter(User.username == req.username,).first()
    if user is None:
        raise HTTPException(401, "user name or passowrd Incorrect !")

    if not verify_password(req.password, user.password):
        raise HTTPException(401, "user name or passowrd Incorrect !")

    exTime = timedelta(days=1)
    if req.remember_me:
        exTime = timedelta(days=30)

    access_token = Authorize.create_access_token(user.username)
    refresh_token = Authorize.create_refresh_token(user.username,
                                                   expires_time=exTime)

    Authorize.set_access_cookies(access_token,
                                 max_age=timedelta(minutes=15).seconds)
    Authorize.set_refresh_cookies(refresh_token, max_age=exTime.seconds)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()) -> Dict[str, str]:
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token,
                                 max_age=timedelta(minutes=15).seconds)
    return {"access_token": new_access_token}


@router.get("/logout")
def logout(res: Response, Authorize: AuthJWT = Depends()) -> Dict[str, str]:
    Authorize.jwt_required()
    res.delete_cookie("access_token_cookie")
    res.delete_cookie("refresh_token_cookie")
    return {"message": "removed cookie!"}


@router.post("/register")
def regester(req: Register, db: Session = Depends(get_db)) -> User:
    # ! no send mail for register
    db_user = User(
        username=req.username,
        email=req.email,
        password=get_password_hash(req.password1),
        owner=req.owner)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get('/users')
def users(
    skip: int = 0, limit: int = 100,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
) -> List[Users]:
    # ! Note: every user can see all users
    Authorize.jwt_required()
    users: List[User] = db.query(User).offset(skip).limit(limit).all()
    return [Users(
        id=v.id,
        username=v.username,
        email=v.email,
        owner=v.owner.name,
    ) for v in users]
