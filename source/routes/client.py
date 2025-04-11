from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.client import ClientCreate, ClientUpdate, ClientResponse
from config.database import engine, Base, get_db
from models.user import User
from typing import List
from controllers.client import (
    create_client, get_client, update_client, 
    delete_client, get_all_clients, get_client_by_name
)
from controllers.auth import get_current_user
from utils.authorization import is_care_coordinator_required, is_office_user
from models.client import Client
from config.parameters import *

# ---- Routes ----
client_router = APIRouter(tags=["Clients"])
Base.metadata.create_all(bind=engine)

@client_router.post("/create_client/", response_model=ClientResponse, dependencies=[Depends(get_current_user)])
def create(client_data: ClientCreate, db: Session = Depends(get_db), current_user:User = Depends(get_current_user), _=Depends(is_office_user)):
    return create_client(db, client_data)

@client_router.get("/get_single_client/{client_id}", response_model=ClientResponse, dependencies=[Depends(get_current_user)])
def read(client_id: int, db: Session = Depends(get_db), current_user:User = Depends(get_current_user), _=Depends(is_care_coordinator_required)):
    return get_client(db, client_id)

@client_router.get("/get_single_client_by_name/{client_name}", response_model=List[ClientResponse], dependencies=[Depends(get_current_user)])
def read_by_name(client_name: str, db: Session = Depends(get_db), current_user:User = Depends(get_current_user), _=Depends(is_care_coordinator_required)):
    return get_client_by_name(db, client_name)

@client_router.get("/get_all_clients/", response_model=List[ClientResponse], dependencies=[Depends(get_current_user)])
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user:User = Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_all_clients(db, skip, limit)

@client_router.put("/update_client/{client_id}", response_model=ClientResponse, dependencies=[Depends(get_current_user)])
def update(client_id: int, update_data: ClientUpdate, db: Session = Depends(get_db), current_user:User = Depends(get_current_user), _=Depends(is_office_user)):
    return update_client(db, client_id, update_data)

@client_router.delete("/delete_client/{client_id}", dependencies=[Depends(get_current_user)])
def delete(client_id: int, db: Session = Depends(get_db), current_user:User = Depends(get_current_user), _=Depends(is_office_user)):
    return delete_client(db, client_id)
