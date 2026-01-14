from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id : Optional[int] = None
    username : str
    email : str
    password : str
    is_active : Optional[bool] = True
    is_staff : Optional[bool] = False


    class Config :
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "secret",
                "is_active": True,
                "is_staff": False
            }
        }

class LoginModel(BaseModel):
    username : str
    password : str


class Settings(BaseModel):
    authjwt_secret_key : str = '1ad81ce6a926f6cafe041b806d25c0aa344988465da2ef056889822607aa6e37'