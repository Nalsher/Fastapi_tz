import fastapi.exceptions
import psycopg2
from fastapi import FastAPI
from sqlalchemy import text

from db.db_crud import Coruier_crud, Order_Crud, engine
from pydantic import BaseModel,TypeAdapter
from typing import List


class Courier(BaseModel):
    name: str
    orders: int | None = None
    area: str

class CourierList(BaseModel):
    id: int | None = None
    name: str

class Order(BaseModel):
    name: str
    district: str

class Get_ord(BaseModel):
    status: dict | tuple | list
    crid: int


app = FastAPI()


@app.get('/')
async def func():
    async with engine.connect() as conn:
        send = await conn.execute(text(f"""SELECT * FROM o"""))
        return {'True':'True'}


@app.get('/courier',response_model=List[CourierList])
async def get_courier_list():
    get = await Coruier_crud.get()
    return get

@app.post('/courier')
async def post_courier(model:Courier):
    model = dict(model)
    get = await Coruier_crud.post(model)
    return get
@app.get('/courier/{id}')
async def get_courier_byid(id):
    get = await Coruier_crud.get_by_id(id)
    return get


@app.post('/order')
async def create_ordr(model:Order):
    model = dict(model)
    send = await Order_Crud.post(model)
    return {'id':send}

@app.get('/order/{id}')
async def get_ord(id):
    get = await Order_Crud.get(id)
    return get

@app.post('/order/{id}')
async def ord_done(id):
    done = await Order_Crud.done(id)
    return done