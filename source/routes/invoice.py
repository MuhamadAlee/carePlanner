from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from config.database import get_db, SessionLocal
from controllers.invoice import (
    create_invoice, get_invoice, update_invoice, 
    delete_invoice, get_all_invoices, get_invoice_by_client_id
)
from controllers.auth import get_current_user
from config.database import engine, Base, get_db, SessionLocal
from utils.authorization import is_admin_required
from models.invoice import Invoice
from models.user import User
from typing import List
from fastapi import BackgroundTasks
from scheduling.generate_invoice import generate
from datetime import date

# ---- Routes ----
invoice_router = APIRouter(tags=["Invoices"])
Base.metadata.create_all(bind=engine)

@invoice_router.post("/generate_invoices/{hours_type}/{first_day_of_month}", response_model=dict, dependencies=[Depends(get_current_user)])
def create_invoices(
    background_tasks: BackgroundTasks,
    hours_type:str,
    first_day_of_month: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
    background_tasks.add_task(generate,tenant, current_user, hours_type, first_day_of_month )
    return {"message": "Invoice creation started in the background"}

@invoice_router.post("/create_invoice/", response_model=InvoiceResponse, dependencies=[Depends(get_current_user)])
def create(invoice_data: InvoiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return create_invoice(db, invoice_data)

@invoice_router.get("/get_single_invoice/{invoice_id}", response_model=InvoiceResponse, dependencies=[Depends(get_current_user)])
def read(invoice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return get_invoice(db, invoice_id)

@invoice_router.get("/get_single_invoice_by_client_id/{client_id}", response_model=List[InvoiceResponse], dependencies=[Depends(get_current_user)])
def read_by_client_id(client_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return get_invoice_by_client_id(db, client_id)

@invoice_router.get("/get_all_invoices/", response_model=List[InvoiceResponse], dependencies=[Depends(get_current_user)])
def read_invoices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return get_all_invoices(db, skip, limit)

@invoice_router.put("/update_invoice/{invoice_id}", response_model=InvoiceResponse, dependencies=[Depends(get_current_user)])
def update(invoice_id: int, update_data: InvoiceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return update_invoice(db, invoice_id, update_data)

@invoice_router.delete("/delete_invoice/{invoice_id}", dependencies=[Depends(get_current_user)])
def delete(invoice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),_=Depends(is_admin_required)):
    return delete_invoice(db, invoice_id)
