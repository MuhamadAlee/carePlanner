from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.rotaTask import RotaTask
from schemas.rotaTask import RotaTaskCreate, RotaTaskUpdate
from utils.rota_util import verify_rota
from sqlalchemy import text

def get_rota_task(db: Session, task_id: int):
    """Retrieve a rota task by its unique identifier.
    
    Args:
        db (Session): Database session.
        task_id (int): Unique identifier of the rota task.
        
    
    Returns:
        RotaTask: The retrieved rota task object if found.
    
    Raises:
        HTTPException: If the rota task is not found.
    """
    try:
        rota_task = db.query(RotaTask).filter(RotaTask.task_id == task_id).first()
        if not rota_task:
            raise HTTPException(status_code=404, detail="Rota Task not found")
        return rota_task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

def get_rota_task_by_rota_id(db: Session, rota_id: int):
    """Retrieve a rota task by its unique identifier.
    
    Args:
        db (Session): Database session.
        rota_id (int): Unique identifier of the rota task.
        
    
    Returns:
        RotaTask: The retrieved rota task object if found.
    
    Raises:
        HTTPException: If the rota task is not found.
    """
    try:
        rota_task = db.query(RotaTask).filter(RotaTask.rota_id == rota_id).all()
        if not rota_task:
            raise HTTPException(status_code=404, detail="Rota Task not found")
        return rota_task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_rota_tasks(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all rota tasks with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[RotaTask]: List of rota tasks.
    """
    try:
        return db.query(RotaTask).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_rota_task(db: Session, rota_task_data: RotaTaskCreate):
    """Create a new rota task in the database.
    
    Args:
        db (Session): Database session.
        rota_task_data (RotaTaskCreate): Rota task creation data.
        
    
    Returns:
        RotaTask: The newly created rota task object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_rota(tenant, rota_task_data.rota_id):
            raise HTTPException(status_code=404, detail='Unable to find Rota')
        rota_task = RotaTask(**rota_task_data.dict())
        db.add(rota_task)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota_task)
        return rota_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_rota_task(db: Session, task_id: int, update_data: RotaTaskUpdate):
    """Update an existing rota task's details.
    
    Args:
        db (Session): Database session.
        task_id (int): Unique identifier of the rota task to be updated.
        update_data (RotaTaskUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        RotaTask: The updated rota task object.
    
    Raises:
        HTTPException: If the rota task is not found or update fails.
    """
    try:
        rota_task = get_rota_task(db, task_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(rota_task, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota_task)
        return rota_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_rota_task(db: Session, task_id: int):
    """Delete a rota task from the database.
    
    Args:
        db (Session): Database session.
        task_id (int): Unique identifier of the rota task to be deleted.
        
    
    Returns:
        dict: Message confirming rota task deletion.
    
    Raises:
        HTTPException: If the rota task is not found or deletion fails.
    """
    try:
        rota_task = get_rota_task(db, task_id)
        db.delete(rota_task)
        db.commit()
        return {"message": "Rota Task deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
