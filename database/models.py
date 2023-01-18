from datetime import datetime

from sqlalchemy import (TIMESTAMP, Column, Integer, MetaData, String, Table,
                        Text)

metadata = MetaData()

post = Table(
    'posts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('body', Text, nullable=True)
)

user = Table(
    'users',
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow)
)