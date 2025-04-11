from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.holidayQuota import HolidayQuota
from schemas.holidayQuota import HolidayQuotaCreate, HolidayQuotaUpdate
from utils.user_util import verify_user
from sqlalchemy import text

def get_holiday_quota(db: Session, holiday_quota_id: int):
    """Retrieve a holiday quota by its unique identifier.
    
    Args:
        db (Session): Database session.
        holiday_quota_id (int): Unique identifier of the holiday quota.
        
    
    Returns:
        HolidayQuota: The retrieved holiday quota object if found.
    
    Raises:
        HTTPException: If the holiday quota is not found.
    """
    try:
        holiday_quota = db.query(HolidayQuota).filter(
            HolidayQuota.holiday_quota_id == holiday_quota_id
        ).first()
        if not holiday_quota:
            raise HTTPException(status_code=404, detail="Holiday quota not found")
        return holiday_quota
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_holiday_quota_by_user_id(db: Session, user_id: int):
    """Retrieve a holiday quota by its unique identifier.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the user_id quota.
        
    
    Returns:
        HolidayQuota: The retrieved holiday quota object if found.
    
    Raises:
        HTTPException: If the holiday quota is not found.
    """
    try:
        holiday_quota = db.query(HolidayQuota).filter(
            HolidayQuota.user_id == user_id
        ).all()
        if not holiday_quota:
            raise HTTPException(status_code=404, detail="Holiday quota not found")
        return holiday_quota
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_holiday_quota(db: Session, holiday_quota_data: HolidayQuotaCreate):
    """Create a new holiday quota in the database.
    
    Args:
        db (Session): Database session.
        holiday_quota_data (HolidayQuotaCreate): Holiday quota creation data.
        
    
    Returns:
        HolidayQuota: The newly created holiday quota object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if (not verify_user(tenant, holiday_quota_data.user_id)):
            raise HTTPException(status_code=400, detail="User or Tenant not found")
        holiday_quota = HolidayQuota(**holiday_quota_data.dict())
        db.add(holiday_quota)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(holiday_quota)
        return holiday_quota
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
def get_all_holiday_quotas(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all holiday quotas with optional pagination.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[HolidayQuota]: List of holiday quotas.
    """
    try:
        return db.query(HolidayQuota).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_holiday_quota(db: Session, holiday_quota_id: int, update_data: HolidayQuotaUpdate):
    """Update an existing holiday quota's details.
    
    Args:
        db (Session): Database session.
        holiday_quota_id (int): Unique identifier of the holiday quota to be updated.
        update_data (HolidayQuotaUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        HolidayQuota: The updated holiday quota object.
    
    Raises:
        HTTPException: If the holiday quota is not found or update fails.
    """
    try:
        holiday_quota = get_holiday_quota(db, holiday_quota_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(holiday_quota, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(holiday_quota)
        return holiday_quota
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_holiday_quota(db: Session, holiday_quota_id: int):
    """Delete a holiday quota from the database.
    
    Args:
        db (Session): Database session.
        holiday_quota_id (int): Unique identifier of the holiday quota to be deleted.
        
    
    Returns:
        dict: Message confirming holiday quota deletion.
    
    Raises:
        HTTPException: If the holiday quota is not found or deletion fails.
    """
    try:
        holiday_quota = get_holiday_quota(db, holiday_quota_id)
        db.delete(holiday_quota)
        db.commit()
        return {"message": "Holiday quota deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
