from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.userAvailability import UserAvailability
from sqlalchemy import text
from schemas.userAvailability import UserAvailabilityCreate, UserAvailabilityUpdate


def get_user_availability(db: Session, availability_id: int):
    """Retrieve a user's availability by its unique identifier.
    
    Args:
        db (Session): Database session.
        availability_id (int): Unique identifier of the availability record.
        
    
    Returns:
        UserAvailability: The retrieved availability object if found.
    
    Raises:
        HTTPException: If the record is not found.
    """
    try:
        availability = db.query(UserAvailability).filter(
            UserAvailability.availability_id == availability_id
        ).first()
        if not availability:
            raise HTTPException(status_code=404, detail="Availability record not found")
        return availability
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_single_user_availabilities(db: Session, user_id: int):
    """Retrieve all availability records for a specific user with optional pagination.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the user.
        
    
    Returns:
        List[UserAvailability]: List of availability records.
    """
    try:
        return db.query(UserAvailability).filter(
            UserAvailability.user_id == user_id
        ).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_single_user_availabilities_on_day(db: Session, user_id: int, day:str):
    """Retrieve all availability records for a specific user with optional pagination.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the user.
        day (str): day of the week.
        
    
    Returns:
        List[UserAvailability]: List of availability records.
    """
    try:
        availability = db.query(UserAvailability).filter(
            UserAvailability.day_of_week==day,
            UserAvailability.user_id == user_id
        ).first()
        if not availability:
            raise HTTPException(status_code=404, detail="No availability found")
        return availability
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

def get_all_users_availabilities(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all availability records for a specific user with optional pagination.
    
    Args:
        db (Session): Database session.

        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[UserAvailability]: List of availability records.
    """
    try:
        return db.query(UserAvailability).filter(
        ).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def create_user_availability(db: Session ,availability_data: UserAvailabilityCreate):
    """Create a new availability record for a user.
    
    Args:
        db (Session): Database session.
        
        availability_data (UserAvailabilityCreate): Availability creation data.
    
    Returns:
        UserAvailability: The newly created availability record.
    """
    try:
        availability = UserAvailability(**availability_data.dict())
        db.add(availability)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(availability)
        return availability
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))


def update_user_availability(db: Session, availability_id: int, update_data: UserAvailabilityUpdate):
    """Update an existing user's availability record.
    
    Args:
        db (Session): Database session.
        availability_id (int): Unique identifier of the availability record.
        update_data (UserAvailabilityUpdate): Data containing the fields to update.
        
    
    Returns:
        UserAvailability: The updated availability record.
    
    Raises:
        HTTPException: If the record is not found or update fails.
    """
    try:
        availability = get_user_availability(db, availability_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(availability, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(availability)
        return availability
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))


def delete_user_availability(db: Session, availability_id: int):
    """Delete a user's availability record.
    
    Args:
        db (Session): Database session.
        availability_id (int): Unique identifier of the availability record.
        
    Returns:
        dict: Message confirming deletion.
    
    Raises:
        HTTPException: If the record is not found or deletion fails.
    """
    try:
        availability = get_user_availability(db, availability_id)
        db.delete(availability)
        db.commit()
        return {"message": "Availability record deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
