from sqlalchemy import (Table, MetaData, String, Integer, JSON,ARRAY,
                        Column, ForeignKey, DATE, Null, Sequence, Boolean,TIMESTAMP)

metadata = MetaData()

courier = Table(
    "courier",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String),
    Column("orders",Integer,ForeignKey("orders.ordid"),nullable=True),
    Column("area",String),
    Column('orders_done',ARRAY(Integer),nullable=True)
)


orders = Table(
    "orders",
    metadata,
    Column("ordid",Integer,primary_key=True),
    Column("is_active",Boolean,nullable=False),
    Column("area", String, nullable=False),
    Column("name",String,nullable=False),
    Column("time",TIMESTAMP,nullable=True),
    Column("time_end",TIMESTAMP,nullable=True)
)

test = Table(
    "testing",
    metadata,
    Column("name",String),
    Column("id",Integer,primary_key=True),
    Column('numbeer',ARRAY(Integer))
)