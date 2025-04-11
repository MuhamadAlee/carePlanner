from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.invoice import Invoice
from schemas.invoice import InvoiceCreate, InvoiceUpdate
from utils.client_util import verify_client
from datetime import date, timedelta
from sqlalchemy import text

def get_invoice(db: Session, invoice_id: int):
    """Retrieve an invoice by its unique identifier.
    
    Args:
        db (Session): Database session.
        invoice_id (int): Unique identifier of the invoice.
        
    
    Returns:
        Invoice: The retrieved invoice object if found.
    
    Raises:
        HTTPException: If the invoice is not found.
    """
    try:
        invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_invoice_by_client_id(db: Session, client_id: int):
    """Retrieve an invoice by its unique identifier.
    
    Args:
        db (Session): Database session.
        client_id (int): Unique identifier of the client.
        
    
    Returns:
        Invoice: The retrieved invoice object if found.
    
    Raises:
        HTTPException: If the invoice is not found.
    """
    try:
        invoice = db.query(Invoice).filter(Invoice.client_id == client_id).all()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_invoices(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all invoices with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Invoice]: List of invoices.
    """
    try:
        return db.query(Invoice).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_invoice(db: Session, invoice_data: InvoiceCreate):
    """Create a new invoice in the database.
    
    Args:
        db (Session): Database session.
        invoice_data (InvoiceCreate): Invoice creation data.
        
    
    Returns:
        Invoice: The newly created invoice object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, invoice_data.client_id):
            raise HTTPException(status_code=404, detail="Unable to find client")
        invoice = Invoice(**invoice_data.dict())
        db.add(invoice)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(invoice)
        return invoice
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_invoice(db: Session, invoice_id: int, update_data: InvoiceUpdate):
    """Update an existing invoice's details.
    
    Args:
        db (Session): Database session.
        invoice_id (int): Unique identifier of the invoice to be updated.
        update_data (InvoiceUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Invoice: The updated invoice object.
    
    Raises:
        HTTPException: If the invoice is not found or update fails.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, update_data.client_id):
            raise HTTPException(status_code=404, detail="Unable to find client")
        invoice_check = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
        if not invoice_check:
            raise HTTPException(status_code=404, detail="Invoice not found")
        invoice = get_invoice(db, invoice_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(invoice, key, value)
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(invoice)
        return invoice
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_invoice(db: Session, invoice_id: int):
    """Delete an invoice from the database.
    
    Args:
        db (Session): Database session.
        invoice_id (int): Unique identifier of the invoice to be deleted.
        
    
    Returns:
        dict: Message confirming invoice deletion.
    
    Raises:
        HTTPException: If the invoice is not found or deletion fails.
    """
    try:
        invoice = get_invoice(db, invoice_id)
        db.delete(invoice)
        db.flush()
        db.commit()
        return {"message": "Invoice deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    
def get_invoice_by_month(db: Session, client_id: int, invoice_date: date):
    """Retrieve invoice entries for a specific month based on the given date.

    Args:
        db (Session): Database session.
        client_id (int): Unique identifier of the invoice entry.
        invoice_date (date): A date to filter invoice entries. Defaults to current date.

    Returns:
        List[Invoice]: A list of invoice entries for the given month.

    Raises:
        HTTPException: If no invoice entries are found.
    """
    try:
        if invoice_date is None:
            invoice_date = date.today()

        month_start = invoice_date.replace(day=1)  # First day of the month
        next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)  # First day of next month
        month_end = next_month - timedelta(days=1)  # Last day of the given month

        invoice_entries = db.query(Invoice).filter(
            Invoice.client_id == client_id,
            Invoice.start_date >= month_start,
            Invoice.end_date <= month_end
        ).all()

        if not invoice_entries:
            raise HTTPException(status_code=404, detail="No invoice entries found for the given month")

        return invoice_entries
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
