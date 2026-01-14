from fastapi import APIRouter
order_router = APIRouter(prefix="/orders", tags=["Orders"])

@order_router.post("/order/")
def place_order():    
    return {"message": "Order placed successfully"}


@order_router.put("/order/update/{order_id}/")
def update_order(order_id: int):
    return {"message": "Order updated successfully"}

@order_router.delete("/order/delete/{order_id}/")
def delete_order(order_id: int):
    return {"message": "Order deleted successfully"}


@order_router.put("order/status/{order_id}/")
def update_order_status(order_id: int):
    return {"message": "Order status updated successfully"}


@order_router.get("/user/orders/")
def get_user_orders():
    return {"message": "User orders fetched successfully"}


@order_router.get("/orders/")
def get_orders_all():
    return {"message": "Orders fetched successfully"}


@order_router.get("/orders/{order_id}/")
def get_order_superuser(order_id: int):
    return {"message": "Order fetched successfully"}



@order_router.get("/user/order/{order_id}/")
def get_specific_order(order_id: int):
    return {"message": "Order placed successfully"}
