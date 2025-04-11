
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends
from config.parameters import *
from utils.auth_util import get_tenant_from_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER_NAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()

def get_db(tenant:str = Depends(get_tenant_from_token)):
    
    db = SessionLocal()
    try:
        # This ensures that the tenant's schema is used for all queries
        db.execute(text(f"SET search_path TO '{tenant}'"))
        yield db
    finally:
        db.close()


def get_db_tenant(tenant:str = Depends(get_tenant_from_token)):
    yield tenant

def get_db_auth():
    
    # print(token)
    tenant= 'public'
    db = SessionLocal()
    try:
        # This ensures that the tenant's schema is used for all queries
        db.execute(text(f"SET search_path TO '{tenant}'"))
        yield db
    finally:
        db.close()
        

def get_db_by_tenant(tenant):
    db = SessionLocal()
    try:
        # This ensures that the tenant's schema is used for all queries
        db.execute(text(f"SET search_path TO '{tenant}'"))
        yield db
    finally:
        db.close()

def create_schema(schema_name: str):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        conn.commit()

def create_tenant_schema_and_tables(schema_name: str):
    create_schema(schema_name)
    
    # Create new metadata with schema
    metadata = MetaData(schema=schema_name)
    for table in Base.metadata.tables.values():
        table.tometadata(metadata)

    metadata.create_all(engine)

