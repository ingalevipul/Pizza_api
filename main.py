from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI()

@app.get('/')
def hello():
    return {'message':'Hello World'}
app.include_router(auth_router)
app.include_router(order_router)


