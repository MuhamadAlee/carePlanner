from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.serviceTask import ServiceTask
from schemas.serviceTask import ServiceTaskCreate, ServiceTaskUpdate
from utils.service_util import verify_service
from utils.roster_util import get_current_roster
from sqlalchemy import text

def get_service_task(db: Session, task_id: int):
    """Retrieve a service task by its unique identifier.
    
    Args:
        db (Session): Database session.
        task_id (int): Unique identifier of the service task.
        
    
    Returns:
        ServiceTask: The retrieved service task object if found.
    
    Raises:
        HTTPException: If the service task is not found.
    """
    try:
        service_task = db.query(ServiceTask).filter(ServiceTask.task_id == task_id).first()
        if not service_task:
            raise HTTPException(status_code=404, detail="service Task not found")
        return service_task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

def get_service_task_by_service_id(db: Session, service_id: int):
    """Retrieve a service task by its unique identifier.
    
    Args:
        db (Session): Database session.
        service_id (int): Unique identifier of the service task.
        
    
    Returns:
        ServiceTask: The retrieved service task object if found.
    
    Raises:
        HTTPException: If the service task is not found.
    """
    try:
        service_task = db.query(ServiceTask).filter(ServiceTask.service_id == service_id).all()
        if not service_task:
            raise HTTPException(status_code=404, detail="service Task not found")
        return service_task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_service_task_by_roster_id(db: Session, user_id:int, role_id:int, roster_id: int):
    """Retrieve a service task by its unique identifier.
    
    Args:
        db (Session): Database session.
        roster_id (int): Unique identifier of the service task.
        
    
    Returns:
        ServiceTask: The retrieved service task object if found.
    
    Raises:
        HTTPException: If the service task is not found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        roster = get_current_roster(tenant, user_id, role_id, roster_id)
        db.execute(text(f"SET search_path TO {tenant}"))
        if roster:
            service_task = db.query(ServiceTask).filter(ServiceTask.service_id == roster.service_id).all()
            if not service_task:
                raise HTTPException(status_code=404, detail="service Task not found")
            return service_task
        raise HTTPException(status_code=404, detail="service Task not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_service_tasks(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all service tasks with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[ServiceTask]: List of service tasks.
    """
    try:
        return db.query(ServiceTask).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_service_task(db: Session, service_task_data: ServiceTaskCreate):
    """Create a new service task in the database.
    
    Args:
        db (Session): Database session.
        service_task_data (ServiceTaskCreate): service task creation data.
        
    
    Returns:
        ServiceTask: The newly created service task object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_service(tenant, service_task_data.service_id):
            raise HTTPException(status_code=404, detail='Unable to find service')
        service_task = ServiceTask(**service_task_data.dict())
        db.add(service_task)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(service_task)
        return service_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_service_task(db: Session, task_id: int, update_data: ServiceTaskUpdate):
    """Update an existing service task's details.
    
    Args:
        db (Session): Database session.
        task_id (int): Unique identifier of the service task to be updated.
        update_data (ServiceTaskUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        ServiceTask: The updated service task object.
    
    Raises:
        HTTPException: If the service task is not found or update fails.
    """
    try:
        service_task = get_service_task(db, task_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(service_task, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(service_task)
        return service_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_service_task(db: Session, task_id: int):
    """Delete a service task from the database.
    
    Args:
        db (Session): Database session.
        task_id (int): Unique identifier of the service task to be deleted.
        
    
    Returns:
        dict: Message confirming service task deletion.
    
    Raises:
        HTTPException: If the service task is not found or deletion fails.
    """
    try:
        service_task = get_service_task(db, task_id)
        db.delete(service_task)
        db.commit()
        return {"message": "service Task deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
