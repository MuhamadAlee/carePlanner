from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvoiceBase(BaseModel):
    invoice_id: int
    client_id: Optional[int] = None
    start_date: date
    end_date: date
    due_date: date
    authority: str
    billable_amount: int
    payment_status: str

class InvoiceCreate(BaseModel):
    client_id: Optional[int] = None
    start_date: date
    end_date: date
    due_date: date
    authority: str
    billable_amount: int
    payment_status: str

class InvoiceUpdate(BaseModel):
    client_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    due_date: Optional[date] = None
    authority: Optional[str] = None
    billable_amount: Optional[int] = None
    payment_status: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    invoice_id: int

    class Config:
        from_attributes = True
