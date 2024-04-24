import asyncio
import datetime
from types import NoneType

from sqlalchemy.ext.asyncio.engine import create_async_engine
from db.config import settings
from sqlalchemy import text
from asyncio import sleep
import json



engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,echo=True)


async def avg_time_ord(id):
    async with engine.connect() as conn:
        ord_done = await conn.execute(text(f"""SELECT orders_done FROM courier WHERE id={id}"""))
        massive = ord_done.fetchone()[0]
        ord_time = []
        if isinstance(massive,NoneType) or len(massive) == 0:
            return 'This courier havent done any order'
        try:
            for i in range(len(massive)):
                ord_start = await conn.execute(text(f"""SELECT time FROM orders WHERE ordid={massive[i]}"""))
                start = ord_start.fetchone()[0]
                ord_end = await conn.execute(text(f"""SELECT time_end FROM orders WHERE ordid={massive[i]}"""))
                end = ord_end.fetchone()[0]
                ord_time.append(end-start)
            summ = datetime.timedelta(0,0,0,0,0,0,0)
            for i in range(len(ord_time)):
                summ += ord_time[i]
            return str(summ/len(massive))[:-7:]
        except:
            return {'error':'Order may not exist'}






async def avg_day_ord(id):
    async with engine.connect() as conn:
        ord_done = await conn.execute(text(f"""SELECT orders_done FROM courier WHERE id={id}"""))
        day_set = []
        massive = ord_done.fetchone()[0]
        if isinstance(massive,NoneType) or len(massive) == 0 :
            return 'This courier havent done any order'
        try:
            for i in range(len(massive)):
                start = await conn.execute(text(f"""SELECT time FROM orders WHERE ordid={massive[i]}"""))
                list = []*1
                list.append(start.fetchone()[0].date())
                if list[0] not in day_set:
                    day_set.append(list[0])
            return int(len(massive)/len(day_set))
        except:
            return {'error':'Order may not exist'}

class Coruier_crud:
    @staticmethod
    async def get():
        async with engine.connect() as conn:
            fetch = await conn.execute(text(f"""SELECT id,name FROM courier"""))
            return fetch.fetchall()
    @staticmethod
    async def get_by_id(id):
        try:
            async with engine.connect() as conn:
                name = await conn.execute(text(f"""SELECT name FROM courier WHERE id = {id}"""))
                ord = await conn.execute(text(f"""SELECT orders FROM courier WHERE id = {id}"""))
                list = []
                list.append(ord.fetchone()[0])
                day_ord = await avg_day_ord(id)
                ord_comp = await avg_time_ord(id)
                if list[0] != None:
                    ord_name = await conn.execute(text(f"""SELECT name FROM orders WHERE ordid={list[0]}"""))
                    return {'id':{id},'name':{name.fetchone()[0]},'active_ord':{'ord_id':list[0],'ord_name':ord_name.fetchone()[0]},'avg_day_complte':day_ord,'avg_ord_complete':ord_comp}
                else:
                    return {'id':{id},'name':{name.fetchone()[0]},'active_ord':'None','avg_day_complte':day_ord,'avg_ord_complete':ord_comp}
        except:
            return {'Error':'Courier not exist'}

    @staticmethod
    async def post(request):
        async with engine.connect() as conn:
            send = await conn.execute(text(f"""INSERT INTO courier
                                            (name,area)
                                            VALUES
                                            ('{request.get('name')}','{request.get('area')}')
                                            """))
            return await conn.commit()
    @staticmethod
    async def get_area(request):
        async with engine.connect() as conn:
            fetch = await conn.execute(text(f"""SELECT id,area FROM courier
                                                WHERE orders IS NULL AND (area='{request.get('district')}')"""))

            if fetch.fetchone() != None:
                result = await conn.execute(text(f"""SELECT id,area FROM courier
                                                WHERE orders IS NULL AND (area='{request.get('district')}')"""))
                return result.fetchone()
            else:
                return ValueError


class Order_Crud:
    @staticmethod
    async def post(request):
        fetch = await Coruier_crud.get_area(request)
        try:
            if request.get('district') == fetch[1]:
                async with engine.connect() as conn:
                    send = await conn.execute(text(f"""INSERT INTO orders(name,area,is_active,time) VALUES ('{request.get('name')}','{request.get('district')}','true','{datetime.datetime.now()}')
                                                        RETURNING ordid """))
                    courier_id = await conn.execute(text(f"""SELECT id from courier WHERE orders IS NULL AND area='{request.get('district')}'"""))
                    id_list = []*2
                    id_list.append(send.fetchone()[0])
                    id_list.append(courier_id.fetchone()[0])
                    save = await conn.execute(text(f"""UPDATE courier SET orders = {id_list[0]} WHERE id={id_list[1]}"""))

                    await conn.commit()
                    return {'ord_id':id_list[0],'cour_id':id_list[1]}
        except:
            return {'error':'Area doesnt have active couirers now'}
    @staticmethod
    async def get(request):
        async with engine.connect() as conn:
            try:
                is_active = await conn.execute(text(f"""SELECT is_active FROM orders WHERE ordid={request}"""))
                active = is_active.fetchone()[0]
                if active == False:
                    cour_id = await conn.execute(text(f"""SELECT id FROM courier WHERE {request}=ANY(orders_done)"""))
                    return {'courier_id':cour_id.fetchone()[0],'status':2}
                elif active == True:
                    cour_id = await conn.execute(text(f"""SELECT id FROM courier WHERE orders={request}"""))
                    return {'courier_id':cour_id.fetchone()[0],'status':1}
            except:
                return {'error':'Order doesnt exist'}
    @staticmethod
    async def done(request):
        async with engine.connect() as conn:
            check = [] * 2
            try:
                ord_get = await conn.execute(text(f"""SELECT is_active FROM orders WHERE ordid={request}"""))
                check.append(ord_get.fetchone()[0])
            except:
                return {'error':'Order may not exist,or its done'}
            finally:
                if len(check) != 0:
                    if check[0] == True:
                        ord_done = await conn.execute(text(f"""UPDATE orders SET is_active=false WHERE ordid={request}"""))
                        time_done = await conn.execute(text(f"""UPDATE orders SET time_end='{datetime.datetime.now()}' WHERE ordid={request}"""))
                        order_done_arr = await conn.execute(text(f"""UPDATE courier SET orders_done = ARRAY_APPEND(orders_done,{request}) WHERE orders={request}"""))
                        order_done_arr_done = await conn.execute(text(f"""UPDATE courier SET orders=Null WHERE orders={request}"""))
                        await conn.commit()
                        return {'status':request + ' order done'}
                    else:
                        return {'error': 'Order may not exist,or its done'}
                else:
                    return {'error':'Order may not exist,or its done'}


