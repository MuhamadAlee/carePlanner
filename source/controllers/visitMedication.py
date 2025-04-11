from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.visitMedication import VisitMedication
from schemas.visitMedication import VisitMedicationCreate, VisitMedicationUpdate
from utils.visit_util import verify_visit
from utils.medication_util import verify_medication
from sqlalchemy import text
from config.parameters import *

def get_visit_medication(db: Session, visit_medication_id: int):
    """Retrieve a visit task by its unique identifier.
    
    Args:
        db (Session): Database session.
        visit_medication_id (int): Unique identifier of the visit task.
        
    
    Returns:
        VisitMedication: The retrieved visit task object if found.
    
    Raises:
        HTTPException: If the visit task is not found.
    """
    try:
        visit_medication = db.query(VisitMedication).filter(VisitMedication.visit_medication_id == visit_medication_id).first()
        if not visit_medication:
            raise HTTPException(status_code=404, detail="Visit task not found")
        return visit_medication
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_visit_medication_by_medication_id(db: Session, medication_id: int):
    """Retrieve a visit task by its medication identifier.
    
    Args:
        db (Session): Database session.
        medication_id (int): Unique identifier of the medication.
        
    
    Returns:
        VisitMedication: The retrieved visit task object if found.
    
    Raises:
        HTTPException: If the visit task is not found.
    """
    try:
        visit_medication = db.query(VisitMedication).filter(VisitMedication.medication_id == medication_id).all()
        if not visit_medication:
            raise HTTPException(status_code=404, detail="Visit task not found")
        return visit_medication
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_visit_medication_by_visit_id(db: Session, visit_id: int):
    """Retrieve a visit task by its visit identifier.
    
    Args:
        db (Session): Database session.
        visit_id (int): Unique identifier of the visit.
        
    
    Returns:
        VisitMedication: The retrieved visit task object if found.
    
    Raises:
        HTTPException: If the visit task is not found.
    """
    try:
        visit_medication = db.query(VisitMedication).filter(VisitMedication.visit_id == visit_id).all()
        if not visit_medication:
            raise HTTPException(status_code=404, detail="Visit task not found")
        return visit_medication
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def create_visit_medication(db: Session, visit_medication_data: VisitMedicationCreate):
    """Create a new visit task in the database.
    
    Args:
        db (Session): Database session.
        visit_medication_data (VisitMedicationCreate): Visit task creation data.
        
    
    Returns:
        VisitMedication: The newly created visit task object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if (not verify_medication(tenant, visit_medication_data.medication_id) or 
            not verify_visit(tenant, visit_medication_data.visit_id)):
            raise HTTPException(status_code=400, detail="Either Task or Visit not found")
        
        visit_medication = VisitMedication(**visit_medication_data.dict())
        db.add(visit_medication)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit_medication)
        return visit_medication
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_all_visit_medications(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all visit tasks with optional pagination.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[VisitMedication]: List of visit tasks.
    """
    try:
        return db.query(VisitMedication).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_visit_medication(db: Session, visit_medication_id: int, update_data: VisitMedicationUpdate):
    """Update an existing visit task's details.
    
    Args:
        db (Session): Database session.
        visit_medication_id (int): Unique identifier of the visit task to be updated.
        update_data (VisitMedicationUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        VisitMedication: The updated visit task object.
    
    Raises:
        HTTPException: If the visit task is not found or update fails.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if (not verify_medication(tenant, update_data.medication_id) or 
            not verify_visit(tenant, update_data.visit_id)):
            raise HTTPException(status_code=400, detail="Either Task or Visit not found")
        visit_medication = get_visit_medication(db, visit_medication_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(visit_medication, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit_medication)
        return visit_medication
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_visit_medication(db: Session, visit_medication_id: int):
    """Delete a visit task from the database.
    
    Args:
        db (Session): Database session.
        visit_medication_id (int): Unique identifier of the visit task to be deleted.
        
    
    Returns:
        dict: Message confirming visit task deletion.
    
    Raises:
        HTTPException: If the visit task is not found or deletion fails.
    """
    try:
        visit_medication = get_visit_medication(db, visit_medication_id)
        db.delete(visit_medication)
        db.commit()
        return {"message": "Visit task deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

def get_refused_medication(db: Session):
    """Retrieve a visit task by its unique identifier.
    
    Args:
        db (Session): Database session.
        
    
    Returns:
        VisitMedication: The retrieved visit task object if found.
    
    Raises:
        HTTPException: If the visit task is not found.
    """
    try:
        visit_medications = db.query(VisitMedication).filter(VisitMedication.status == MEDICATION_REFUSED).all()
        if not visit_medications:
            raise HTTPException(status_code=404, detail="Visit task not found")
        return visit_medications
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))