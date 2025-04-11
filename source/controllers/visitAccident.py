from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.visitAccident import VisitAccident
from schemas.visitAccident import VisitAccidentCreate, VisitAccidentUpdate
from utils.visit_util import verify_visit
from utils.medication_util import verify_medication
from sqlalchemy import text

def get_visit_accident(db: Session, visit_accident_id: int):
    """Retrieve a visit task by its unique identifier.
    
    Args:
        db (Session): Database session.
        visit_accident_id (int): Unique identifier of the visit task.
        
    
    Returns:
        VisitAccident: The retrieved visit task object if found.
    
    Raises:
        HTTPException: If the visit task is not found.
    """
    try:
        visit_accident = db.query(VisitAccident).filter(VisitAccident.visit_accident_id == visit_accident_id).first()
        if not visit_accident:
            raise HTTPException(status_code=404, detail="Visit task not found")
        return visit_accident
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_visit_accident_by_visit_id(db: Session, visit_id: int):
    """Retrieve a visit task by its unique identifier.
    
    Args:
        db (Session): Database session.
        visit_id (int): Unique identifier of the visit task.
        
    
    Returns:
        VisitAccident: The retrieved visit task object if found.
    
    Raises:
        HTTPException: If the visit task is not found.
    """
    try:
        visit_accident = db.query(VisitAccident).filter(VisitAccident.visit_id == visit_id).all()
        if not visit_accident:
            raise HTTPException(status_code=404, detail="Visit task not found")
        return visit_accident
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_visit_accident(db: Session, visit_accident_data: VisitAccidentCreate):
    """Create a new visit task in the database.
    
    Args:
        db (Session): Database session.
        visit_accident_data (VisitAccidentCreate): Visit task creation data.
        
    
    Returns:
        VisitAccident: The newly created visit task object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if (not verify_visit(tenant, visit_accident_data.visit_id)):
            raise HTTPException(status_code=400, detail="Either Task or Visit not found")
        
        visit_accident = VisitAccident(**visit_accident_data.dict())
        db.add(visit_accident)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit_accident)
        return visit_accident
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_all_visit_accidents(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all visit tasks with optional pagination.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[VisitAccident]: List of visit tasks.
    """
    try:
        return db.query(VisitAccident).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_visit_accident(db: Session, visit_accident_id: int, update_data: VisitAccidentUpdate):
    """Update an existing visit task's details.
    
    Args:
        db (Session): Database session.
        visit_accident_id (int): Unique identifier of the visit task to be updated.
        update_data (VisitAccidentUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        VisitAccident: The updated visit task object.
    
    Raises:
        HTTPException: If the visit task is not found or update fails.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if (not verify_visit(tenant, update_data.visit_id)):
            raise HTTPException(status_code=400, detail="Either Task or Visit not found")
        visit_accident = get_visit_accident(db, visit_accident_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(visit_accident, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit_accident)
        return visit_accident
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_visit_accident(db: Session, visit_accident_id: int):
    """Delete a visit task from the database.
    
    Args:
        db (Session): Database session.
        visit_accident_id (int): Unique identifier of the visit task to be deleted.
        
    
    Returns:
        dict: Message confirming visit task deletion.
    
    Raises:
        HTTPException: If the visit task is not found or deletion fails.
    """
    try:
        visit_accident = get_visit_accident(db, visit_accident_id)
        db.delete(visit_accident)
        db.commit()
        return {"message": "Visit task deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))