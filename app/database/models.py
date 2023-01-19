from datetime import datetime

from sqlalchemy import (TIMESTAMP, Column, Integer, MetaData, String, Table,
                        Text, Boolean)

metadata = MetaData()

post = Table(
    'post',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('body', Text, nullable=True)
)

user = Table(
    'user',
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False)
)