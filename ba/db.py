
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('passwd', String(50), nullable=False),
    Column('role', String(50), nullable=False)
)



