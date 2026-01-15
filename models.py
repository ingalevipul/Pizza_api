from sqlalchemy import Column, Integer, String, Float,Boolean,ForeignKey,Text
from database import Base
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}"


class Order(Base):
    ORDER_STATUSES=(('pending','PENDING'),('in_progress','IN_PROGRESS'),('completed','COMPLETED'))
    PIZZA_SIZES=(('small','SMALL'),('medium','MEDIUM'),('large','LARGE'))
    __tablename__="orders"
    id =Column(Integer,primary_key=True,index=True)
    quantity = Column(Integer,nullable=False)
    order_status = Column(String, default='pending')
    pizza_size = Column(String, default='small')
    flavour=Column(String)
    user_id=Column(Integer,ForeignKey("user.id"))
    
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}"
