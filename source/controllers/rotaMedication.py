from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.rotaMedication import RotaMedication
from schemas.rotaMedication import RotaMedicationCreate, RotaMedicationUpdate
from utils.rota_util import verify_rota
from sqlalchemy import text

def get_rota_medication(db: Session, medication_id: int):
    """Retrieve a rota medication by its unique identifier.
    
    Args:
        db (Session): Database session.
        medication_id (int): Unique identifier of the rota medication.
        
    
    Returns:
        RotaMedication: The retrieved rota medication object if found.
    
    Raises:
        HTTPException: If the rota medication is not found.
    """
    try:
        rota_medication = db.query(RotaMedication).filter(RotaMedication.medication_id == medication_id).first()
        if not rota_medication:
            raise HTTPException(status_code=404, detail="Rota Medication not found")
        return rota_medication
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_rota_medication_by_rota_id(db: Session, rota_id: int):
    """Retrieve a rota medication by its unique identifier.
    
    Args:
        db (Session): Database session.
        rota_id (int): Unique identifier of the rota medication.
        
    
    Returns:
        RotaMedication: The retrieved rota medication object if found.
    
    Raises:
        HTTPException: If the rota medication is not found.
    """
    try:
        rota_medication = db.query(RotaMedication).filter(RotaMedication.rota_id == rota_id).all()
        if not rota_medication:
            raise HTTPException(status_code=404, detail="Rota Medication not found")
        return rota_medication
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_rota_medications(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all rota medications with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[RotaMedication]: List of rota medications.
    """
    try:
        return db.query(RotaMedication).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_rota_medication(db: Session, rota_medication_data: RotaMedicationCreate):
    """Create a new rota medication in the database.
    
    Args:
        db (Session): Database session.
        rota_medication_data (RotaMedicationCreate): Rota medication creation data.
        
    
    Returns:
        RotaMedication: The newly created rota medication object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_rota(tenant, rota_medication_data.rota_id):
            raise HTTPException(status_code=404, detail='Unable to find Rota')
        rota_medication = RotaMedication(**rota_medication_data.dict())
        db.add(rota_medication)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota_medication)
        return rota_medication
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_rota_medication(db: Session, medication_id: int, update_data: RotaMedicationUpdate):
    """Update an existing rota medication's details.
    
    Args:
        db (Session): Database session.
        medication_id (int): Unique identifier of the rota medication to be updated.
        update_data (RotaMedicationUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        RotaMedication: The updated rota medication object.
    
    Raises:
        HTTPException: If the rota medication is not found or update fails.
    """
    try:
        rota_medication = get_rota_medication(db, medication_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(rota_medication, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota_medication)
        return rota_medication
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_rota_medication(db: Session, medication_id: int):
    """Delete a rota medication from the database.
    
    Args:
        db (Session): Database session.
        medication_id (int): Unique identifier of the rota medication to be deleted.
        
    
    Returns:
        dict: Message confirming rota medication deletion.
    
    Raises:
        HTTPException: If the rota medication is not found or deletion fails.
    """
    try:
        rota_medication = get_rota_medication(db, medication_id)
        db.delete(rota_medication)
        db.commit()
        return {"message": "Rota Medication deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
