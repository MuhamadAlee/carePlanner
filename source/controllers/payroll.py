from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.payroll import Payroll
from schemas.payroll import PayrollCreate, PayrollUpdate
from utils.user_util import verify_user
from datetime import date, timedelta
from typing import Optional
from sqlalchemy import text

def get_payroll(db: Session, payroll_id: int):
    """Retrieve a payroll entry by its unique identifier.
    
    Args:
        db (Session): Database session.
        payroll_id (int): Unique identifier of the payroll entry.
        
    
    Returns:
        Payroll: The retrieved payroll entry if found.
    
    Raises:
        HTTPException: If the payroll entry is not found.
    """
    try:
        payroll = db.query(Payroll).filter(
            Payroll.payroll_id == payroll_id
        ).first()
        if not payroll:
            raise HTTPException(status_code=404, detail="Payroll entry not found")
        return payroll
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_payroll_by_user_id(db: Session, user_id: int):
    """Retrieve a payroll entry by its unique identifier.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the payroll entry.
        
    
    Returns:
        Payroll: The retrieved payroll entry if found.
    
    Raises:
        HTTPException: If the payroll entry is not found.
    """
    try:
        payroll = db.query(Payroll).filter(
            Payroll.user_id == user_id
        ).all()
        if not payroll:
            raise HTTPException(status_code=404, detail="Payroll entry not found")
        return payroll
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_payroll_by_month(db: Session, user_id: int, payroll_date: Optional[date] = None):
    """Retrieve payroll entries for a specific month based on the given date.

    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the payroll entry.
        
        payroll_date (Optional[date]): A date to filter payroll entries. Defaults to current date.

    Returns:
        List[Payroll]: A list of payroll entries for the given month.

    Raises:
        HTTPException: If no payroll entries are found.
    """
    try:
        if payroll_date is None:
            payroll_date = date.today()

        month_start = payroll_date.replace(day=1)  # First day of the month
        next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)  # First day of next month
        month_end = next_month - timedelta(days=1)  # Last day of the given month

        payroll_entries = db.query(Payroll).filter(
            Payroll.user_id == user_id,
            Payroll.start_date >= month_start,
            Payroll.end_date <= month_end
        ).all()

        if not payroll_entries:
            raise HTTPException(status_code=404, detail="No payroll entries found for the given month")

        return payroll_entries
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_payroll(db: Session, payroll_data: PayrollCreate):
    """Create a new payroll entry in the database.
    
    Args:
        db (Session): Database session.
        payroll_data (PayrollCreate): Payroll creation data.
        
    
    Returns:
        Payroll: The newly created payroll entry.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_user(tenant, payroll_data.user_id):
            raise HTTPException(status_code=400, detail="User or Tenant not found")
        payroll = Payroll(**payroll_data.dict())
        db.add(payroll)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(payroll)
        return payroll
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_all_payrolls(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all payroll entries with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Payroll]: List of payroll entries.
    """
    try:
        return db.query(Payroll).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_payroll(db: Session, payroll_id: int, update_data: PayrollUpdate):
    """Update an existing payroll entry.
    
    Args:
        db (Session): Database session.
        payroll_id (int): Unique identifier of the payroll entry to be updated.
        update_data (PayrollUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Payroll: The updated payroll entry.
    
    Raises:
        HTTPException: If the payroll entry is not found or update fails.
    """
    try:
        payroll = get_payroll(db, payroll_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(payroll, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(payroll)
        return payroll
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_payroll(db: Session, payroll_id: int):
    """Delete a payroll entry from the database.
    
    Args:
        db (Session): Database session.
        payroll_id (int): Unique identifier of the payroll entry to be deleted.
        
    
    Returns:
        dict: Message confirming payroll entry deletion.
    
    Raises:
        HTTPException: If the payroll entry is not found or deletion fails.
    """
    try:
        payroll = get_payroll(db, payroll_id)
        db.delete(payroll)
        db.commit()
        return {"message": "Payroll entry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
