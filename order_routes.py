from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import OrderModel, updateOrderModel,viewOrderModel,update_order_status
from models import Order, User
from fastapi_jwt_auth import AuthJWT
from typing import List

order_router = APIRouter(prefix="/orders", tags=["Orders"])
@order_router.post("/order/",status_code=status.HTTP_201_CREATED)
def place_order(order_data:OrderModel,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()
    user_id=db.query(User.id).filter(User.username==current_user).first()

    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    order = Order(quantity=order_data.quantity,order_status=order_data.order_status,pizza_size=order_data.pizza_size,flavour=order_data.flavour,user_id=user_id.id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"message": "Order placed successfully"} 


@order_router.put("/order/update/{order_id}/",status_code=status.HTTP_201_CREATED)
def update_order(order_id: int,order_data: updateOrderModel,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    current_user=Authorize.get_jwt_subject()
    user_id=db.query(User.id).filter(User.username==current_user).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    
    if order.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update this order")
    
    order.quantity=order_data.quantity
    order.order_status=order_data.order_status
    order.pizza_size=order_data.pizza_size
    order.flavour=order_data.flavour
    db.commit()
    return {"message": "Order updated successfully"} 

@order_router.get("/order/{order_id}/",response_model=viewOrderModel)
def get_order(order_id: int,db:Session=Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    current_user=Authorize.get_jwt_subject()
    user_id=db.query(User.id).filter(User.username==current_user).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    
    if order.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update this order")
    return order
    
@order_router.delete("/order/delete/{order_id}/")
def delete_order(order_id: int,db:Session=Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    current_user=Authorize.get_jwt_subject()
    user_id=db.query(User.id).filter(User.username==current_user).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    
    if order.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update this order")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}


@order_router.put("/admin/order/status/{order_id}/")
def update_order_status(order_id: int,order_data:update_order_status,db:Session=Depends(get_db), Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    current_user=Authorize.get_jwt_subject()
    user_id=db.query(User.id).filter(User.username==current_user).first()
    is_staff=db.query(User.is_staff).filter(User.username==current_user).first()
    if not is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update this order")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    
    if order.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update this order")
    
    order.order_status=order_data.order_status
    db.commit()
    return {"message": "Order status updated successfully"}



@order_router.get("/user/orders",response_model=List[viewOrderModel])
def get_user_orders(db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    current_user=Authorize.get_jwt_subject()
    user_id=db.query(User.id).filter(User.username==current_user).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    orders=db.query(Order).filter(Order.user_id==user_id.id).all()
    return orders
    




@order_router.get("/admin/order/{user_id}",response_model=List[viewOrderModel])
def get_user_order(user_id: int,db:Session=Depends(get_db), Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    current_user=Authorize.get_jwt_subject()
    user_id_db=db.query(User.id).filter(User.username==current_user).first()
    is_staff=db.query(User.is_staff).filter(User.username==current_user).first()

    customer_id=db.query(User.id).filter(User.id==user_id).first()

    if not user_id_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized")
    

    user_temp=db.query(User).filter(User.id==user_id).first()
    if not user_temp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    orders=db.query(Order).filter(Order.user_id==user_id).all()
    return orders
