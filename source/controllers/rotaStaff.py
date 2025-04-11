from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.rotaStaff import RotaStaff
from utils.rota_util import verify_rota
from utils.user_util import verify_user
from schemas.rotaStaff import RotaStaffCreate, RotaStaffUpdate
from sqlalchemy import text

def get_rota_staff(db: Session, rota_staff_id: int):
    """Retrieve a rota staff entry by its unique identifier.
    
    Args:
        db (Session): Database session.
        rota_staff_id (int): Unique identifier of the rota staff entry.
        
    
    Returns:
        RotaStaff: The retrieved rota staff object if found.
    
    Raises:
        HTTPException: If the rota staff entry is not found.
    """
    try:
        rota_staff = db.query(RotaStaff).filter(
            RotaStaff.rota_staff_id == rota_staff_id
        ).first()
        if not rota_staff:
            raise HTTPException(status_code=404, detail="Rota staff entry not found")
        return rota_staff
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_rota_staff_by_user_id(db: Session, user_id: int):
    """Retrieve a rota staff entry by its unique identifier.
    
    Args:
        db (Session): Database session.

        user_id (int): Unique identifier of the user to which rota belongs.
        
    
    Returns:
        RotaStaff: The retrieved rota staff object if found.
    
    Raises:
        HTTPException: If the rota staff entry is not found.
    """
    try:
        rota_staff = db.query(RotaStaff).filter(
            RotaStaff.user_id == user_id
        ).all()
        if not rota_staff:
            raise HTTPException(status_code=404, detail="Rota staff entry not found")
        return rota_staff
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_rota_staff_by_rota_id(db: Session, rota_id: int):
    """Retrieve a rota staff entry by its unique identifier.
    
    Args:
        db (Session): Database session.

        rota_id (int): Unique identifier of the rota belongs.
        
    
    Returns:
        RotaStaff: The retrieved rota staff object if found.
    
    Raises:
        HTTPException: If the rota staff entry is not found.
    """
    try:
        rota_staff = db.query(RotaStaff).filter(
            RotaStaff.rota_id == rota_id
        ).all()
        if not rota_staff:
            raise HTTPException(status_code=404, detail="Rota staff entry not found")
        return rota_staff
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_rota_staff(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all rota staff entries with optional pagination.
    
    Args:
        db (Session): Database session.
        
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[RotaStaff]: List of rota staff entries.
    """
    try:
        return db.query(RotaStaff).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_rota_staff(db: Session, rota_staff_data: RotaStaffCreate):
    """Create a new rota staff entry in the database.
    
    Args:
        db (Session): Database session.
        rota_staff_data (RotaStaffCreate): Rota staff creation data.
    
    Returns:
        RotaStaff: The newly created rota staff entry.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_rota(tenant, rota_staff_data.rota_id):
            raise HTTPException(status_code=404, detail='Rota not found')
        if not verify_user(tenant, rota_staff_data.user_id):
            raise HTTPException(status_code=404, detail='Rota not found')
        rota_staff = RotaStaff(**rota_staff_data.dict())
        db.add(rota_staff)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota_staff)
        return rota_staff
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_rota_staff(db: Session, rota_staff_id: int, update_data: RotaStaffUpdate):
    """Update an existing rota staff entry's details.
    
    Args:
        db (Session): Database session.
        rota_staff_id (int): Unique identifier of the rota staff entry to be updated.
        update_data (RotaStaffUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        RotaStaff: The updated rota staff object.
    
    Raises:
        HTTPException: If the rota staff entry is not found or update fails.
    """
    try:
        rota_staff = get_rota_staff(db, rota_staff_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(rota_staff, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota_staff)
        return rota_staff
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_rota_staff(db: Session, rota_staff_id: int):
    """Delete a rota staff entry from the database.
    
    Args:
        db (Session): Database session.
        rota_staff_id (int): Unique identifier of the rota staff entry to be deleted.
    
    Returns:
        dict: Message confirming rota staff deletion.
    
    Raises:
        HTTPException: If the rota staff entry is not found or deletion fails.
    """
    try:
        rota_staff = get_rota_staff(db, rota_staff_id)
        db.delete(rota_staff)
        db.commit()
        return {"message": "Rota staff entry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
