from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from config.database import get_db, SessionLocal
from controllers.contact import (
    create_contact, get_contact, update_contact, 
    delete_contact, get_all_contacts, get_contact_by_client
)
from controllers.auth import get_current_user
from config.database import engine, Base, get_db, SessionLocal
from utils.authorization import is_care_coordinator_required, is_office_user
from models.contact import Contact
from models.user import User
from typing import List

# ---- Routes ----
contact_router = APIRouter(tags=["Contacts"])
Base.metadata.create_all(bind=engine)


@contact_router.post("/create_contact/", response_model=ContactResponse, dependencies=[Depends(get_current_user)])
def create(contact_data: ContactCreate, db: Session = Depends(get_db), current_user:User =Depends(get_current_user),_=Depends(is_office_user)):
    return create_contact(db, contact_data)

@contact_router.get("/get_single_contact/{contact_id}", response_model=List[ContactResponse], dependencies=[Depends(get_current_user)])
def read(contact_id: int, db: Session = Depends(get_db), current_user:User =Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_contact(db, contact_id)

@contact_router.get("/get_contact_by_user_id/{client_id}", response_model=List[ContactResponse], dependencies=[Depends(get_current_user)])
def read_by_user_id(client_id: int, db: Session = Depends(get_db), current_user:User =Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_contact_by_client(db, client_id)


@contact_router.get("/get_all_contacts/", response_model=List[ContactResponse], dependencies=[Depends(get_current_user)])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user:User =Depends(get_current_user),_=Depends(is_care_coordinator_required)):
    return get_all_contacts(db, skip, limit)

@contact_router.put("/update_contact/{contact_id}", response_model=ContactResponse, dependencies=[Depends(get_current_user)])
def update(contact_id: int, update_data: ContactUpdate, db: Session = Depends(get_db), current_user:User =Depends(get_current_user),_=Depends(is_office_user)):
    return update_contact(db, contact_id, update_data)

@contact_router.delete("/delete_contact/{contact_id}", dependencies=[Depends(get_current_user)])
def delete(contact_id: int, db: Session = Depends(get_db), current_user:User =Depends(get_current_user),_=Depends(is_office_user)):
    return delete_contact(db, contact_id)