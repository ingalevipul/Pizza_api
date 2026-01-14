from fastapi import APIRouter,status,Depends
from database import engine,SessionLocal
from fastapi import HTTPException
from schemas import SignUpModel,LoginModel
from models import User
from jwt_helper import JWTHelper
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException as StarletteHTTPException
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

session = SessionLocal(bind=engine)

@auth_router.get("/")
def hello():
    return {'message':'Hello World'}
@auth_router.post("/login")
async def login(user: LoginModel):
    db_user=session.query(User).filter(User.username==user.username).first()
    if db_user and check_password_hash(db_user.password,user.password):
        access_token=JWTHelper.create_access_token(subject=db_user.username)
        refresh_token=JWTHelper.create_refresh_token(subject=db_user.username)
        response={
            'access_token':access_token,
            'refresh_token':refresh_token
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")

@auth_router.post("/signup",status_code=status.HTTP_201_CREATED)
async def register(user: SignUpModel):
    db_email=session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=400,detail="Email already exists")


    db_uname= session.query(User).filter(User.username==user.username).first()

    if db_uname is not None:
        raise HTTPException(status_code=400,detail="Username already exists")  

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    return {"message":"User created successfully"}