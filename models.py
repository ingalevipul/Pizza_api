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
    ORDER_STATUSES=( ('PENDING','pending'),('IN_PROGRESS','in_progress'),('COMPLETED','completed'))
    PIZZA_SIZES=(('SMALL','small'),('MEDIUM','medium'),('LARGE','large'))
    __tablename__="orders"
    id =Column(Integer,primary_key=True,index=True)
    quantity = Column(Integer,nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUSES),default='PENDING')
    pizza_size=Column(ChoiceType(choices=PIZZA_SIZES),default='SMALL')
    flavour=Column(String)
    user_id=Column(Integer,ForeignKey("user.id"))
    
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}"
