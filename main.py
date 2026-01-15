from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")

@AuthJWT.load_config
def get_config():
    return Settings()

@app.get('/')
def hello():
    return {'message':'Hello World'}

app.include_router(auth_router)
app.include_router(order_router)


