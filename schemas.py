from pydantic import BaseModel, field_validator
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


class OrderModel(BaseModel):
    id : Optional[int] = None
    quantity : int
    order_status : Optional[str] = None
    pizza_size : Optional[str] = None
    flavour : Optional[str]
    user_id : Optional[int]=None
    
    @field_validator('order_status', 'pizza_size', mode='before')
    @classmethod
    def to_lowercase(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v
    
    class Config :
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 1,
                "order_status": "pending",
                "pizza_size": "small",
                "flavour": "pepperoni"
            }
        }

class updateOrderModel(BaseModel):
    quantity : int
    order_status : Optional[str] = None
    pizza_size : Optional[str] = None
    flavour : Optional[str]

    @field_validator('order_status', 'pizza_size', mode='before')
    @classmethod
    def to_lowercase(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

class viewOrderModel(BaseModel):

    quantity : int
    order_status : Optional[str] = None
    pizza_size : Optional[str] = None
    flavour : Optional[str]
    user_id : Optional[int]=None
    
    @field_validator('order_status', 'pizza_size', mode='before')
    @classmethod
    def to_lowercase(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class update_order_status (BaseModel):
    order_status : Optional[str] = None
    
    @field_validator('order_status', mode='before')
    @classmethod
    def to_lowercase(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v