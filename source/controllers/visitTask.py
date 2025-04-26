from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.visitTask import VisitTask
from schemas.visitTask import VisitTaskCreate, VisitTaskUpdate
from utils.visit_util import verify_visit
from utils.task_util import verify_task
from sqlalchemy import text

def get_visit_task(db: Session, visit_task_id: int):
    """Retrieve a visit task by its unique identifier.
    
    Args:
        db (Session): Database session.
        visit_task_id (int): Unique identifier of the visit task.
        
    
    Returns:
        VisitTask: The retrieved visit task object if found.
    
    Raises:
        HTTPException: If the visit task is not found.
    """
    try:
        visit_task = db.query(VisitTask).filter(VisitTask.visit_task_id == visit_task_id).first()
        if not visit_task:
            raise HTTPException(status_code=404, detail="Visit task not found")
        return visit_task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_visit_task_by_visit_id(db: Session, visit_id: int):
    """Retrieve a visit task by visit ID."""
    try:
        visit_task = db.query(VisitTask).filter(VisitTask.visit_id == visit_id).all()
        if not visit_task:
            raise HTTPException(status_code=404, detail="Visit task not found by visit ID")
        return visit_task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_visit_task_by_task_id(db: Session, task_id: int):
    """Retrieve a visit task by task ID."""
    try:
        visit_task = db.query(VisitTask).filter(VisitTask.task_id == task_id).all()
        if not visit_task:
            raise HTTPException(status_code=404, detail="Visit task not found by task ID")
        return visit_task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_visit_task(db: Session, user_id, role_id, visit_task_data: VisitTaskCreate):
    """Create a new visit task in the database.
    
    Args:
        db (Session): Database session.
        visit_task_data (VisitTaskCreate): Visit task creation data.
        
    
    Returns:
        VisitTask: The newly created visit task object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if (not verify_task(tenant, visit_task_data.task_id) or 
            not verify_visit(tenant, user_id, role_id, visit_task_data.visit_id)):
            raise HTTPException(status_code=400, detail="Either Task or Visit not found")
        
        visit_task = VisitTask(**visit_task_data.dict())
        db.add(visit_task)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit_task)
        return visit_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_all_visit_tasks(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all visit tasks with optional pagination.

    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[VisitTask]: List of visit tasks.
    """
    try:
        return db.query(VisitTask).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_visit_task(db: Session, visit_task_id: int, update_data: VisitTaskUpdate):
    """Update an existing visit task's details.
    
    Args:
        db (Session): Database session.
        visit_task_id (int): Unique identifier of the visit task to be updated.
        update_data (VisitTaskUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        VisitTask: The updated visit task object.
    
    Raises:
        HTTPException: If the visit task is not found or update fails.
    """
    try:
        visit_task = get_visit_task(db, visit_task_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(visit_task, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit_task)
        return visit_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_visit_task(db: Session, visit_task_id: int):
    """Delete a visit task from the database.
    
    Args:
        db (Session): Database session.
        visit_task_id (int): Unique identifier of the visit task to be deleted.
        
    
    Returns:
        dict: Message confirming visit task deletion.
    
    Raises:
        HTTPException: If the visit task is not found or deletion fails.
    """
    try:
        visit_task = get_visit_task(db, visit_task_id)
        db.delete(visit_task)
        db.commit()
        return {"message": "Visit task deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))