from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import SignUpModel, LoginModel
from models import User
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/")
def hello(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return {'message': 'Hello World'}

@auth_router.post("/login")
async def login(user: LoginModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def register(user: SignUpModel, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_uname = db.query(User).filter(User.username == user.username).first()

    if db_uname is not None:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@auth_router.get("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return {'access_token': access_token}
    