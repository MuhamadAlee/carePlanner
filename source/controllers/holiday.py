from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.holiday import Holiday
from schemas.holiday import HolidayCreate, HolidayUpdate
from sqlalchemy import create_engine, MetaData, text
from utils.user_util import verify_user

def get_holiday(db: Session, holiday_id: int):
    """Retrieve a holiday entry by its unique identifier.
    
    Args:
        db (Session): Database session.
        holiday_id (int): Unique identifier of the holiday entry.
        
    
    Returns:
        Holiday: The retrieved holiday entry if found.
    
    Raises:
        HTTPException: If the holiday entry is not found.
    """
    try:
        holiday = db.query(Holiday).filter(
            Holiday.holiday_id == holiday_id,
        ).first()
        if not holiday:
            raise HTTPException(status_code=404, detail="Holiday entry not found")
        return holiday
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_holiday_by_user_id(db: Session, user_id: int):
    """Retrieve a holiday entry by its unique identifier.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the holiday entry for user.
        
    
    Returns:
        Holiday: The retrieved holiday entry if found.
    
    Raises:
        HTTPException: If the holiday entry is not found.
    """
    try:
        holiday = db.query(Holiday).filter(
            Holiday.user_id == user_id
        ).all()
        if not holiday:
            raise HTTPException(status_code=404, detail="Holiday entry not found")
        return holiday
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_holiday(db: Session, holiday_data: HolidayCreate):
    """Create a new holiday entry in the database.
    
    Args:
        db (Session): Database session.
        holiday_data (HolidayCreate): Holiday creation data.
        
    
    Returns:
        Holiday: The newly created holiday entry.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_user(tenant, holiday_data.user_id):
            raise HTTPException(status_code=400, detail="User or Tenant not found")
        holiday = Holiday(**holiday_data.dict())
        db.add(holiday)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(holiday)
        return holiday
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_all_holidays(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all holiday entries with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Holiday]: List of holiday entries.
    """
    try:
        return db.query(Holiday).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_holiday(db: Session, holiday_id: int, update_data: HolidayUpdate):
    """Update an existing holiday entry.
    
    Args:
        db (Session): Database session.
        holiday_id (int): Unique identifier of the holiday entry to be updated.
        update_data (HolidayUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Holiday: The updated holiday entry.
    
    Raises:
        HTTPException: If the holiday entry is not found or update fails.
    """
    try:
        holiday = get_holiday(db, holiday_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(holiday, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(holiday)
        return holiday
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_holiday(db: Session, holiday_id: int):
    """Delete a holiday entry from the database.
    
    Args:
        db (Session): Database session.
        holiday_id (int): Unique identifier of the holiday entry to be deleted.
        
    
    Returns:
        dict: Message confirming holiday entry deletion.
    
    Raises:
        HTTPException: If the holiday entry is not found or deletion fails.
    """
    try:
        holiday = get_holiday(db, holiday_id)
        db.delete(holiday)
        db.commit()
        return {"message": "Holiday entry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
