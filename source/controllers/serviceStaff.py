from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.serviceStaff import ServiceStaff
from utils.service_util import verify_service
from utils.user_util import verify_user
from schemas.serviceStaff import ServiceStaffCreate, ServiceStaffUpdate
from sqlalchemy import text

def get_service_staff(db: Session, service_staff_id: int):
    """Retrieve a service staff entry by its unique identifier.
    
    Args:
        db (Session): Database session.
        service_staff_id (int): Unique identifier of the service staff entry.
        
    
    Returns:
        ServiceStaff: The retrieved service staff object if found.
    
    Raises:
        HTTPException: If the service staff entry is not found.
    """
    try:
        service_staff = db.query(ServiceStaff).filter(
            ServiceStaff.service_staff_id == service_staff_id
        ).first()
        if not service_staff:
            raise HTTPException(status_code=404, detail="service staff entry not found")
        return service_staff
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_service_staff_by_user_id(db: Session, user_id: int):
    """Retrieve a service staff entry by its unique identifier.
    
    Args:
        db (Session): Database session.

        user_id (int): Unique identifier of the user to which service belongs.
        
    
    Returns:
        ServiceStaff: The retrieved service staff object if found.
    
    Raises:
        HTTPException: If the service staff entry is not found.
    """
    try:
        service_staff = db.query(ServiceStaff).filter(
            ServiceStaff.user_id == user_id
        ).all()
        if not service_staff:
            raise HTTPException(status_code=404, detail="service staff entry not found")
        return service_staff
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_service_staff_by_service_id(db: Session, service_id: int):
    """Retrieve a service staff entry by its unique identifier.
    
    Args:
        db (Session): Database session.

        service_id (int): Unique identifier of the service belongs.
        
    
    Returns:
        ServiceStaff: The retrieved service staff object if found.
    
    Raises:
        HTTPException: If the service staff entry is not found.
    """
    try:
        service_staff = db.query(ServiceStaff).filter(
            ServiceStaff.service_id == service_id
        ).all()
        if not service_staff:
            raise HTTPException(status_code=404, detail="service staff entry not found")
        return service_staff
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_service_staff(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all service staff entries with optional pagination.
    
    Args:
        db (Session): Database session.
        
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[ServiceStaff]: List of service staff entries.
    """
    try:
        return db.query(ServiceStaff).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_service_staff(db: Session, service_staff_data: ServiceStaffCreate):
    """Create a new service staff entry in the database.
    
    Args:
        db (Session): Database session.
        service_staff_data (ServiceStaffCreate): service staff creation data.
    
    Returns:
        ServiceStaff: The newly created service staff entry.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_service(tenant, service_staff_data.service_id):
            raise HTTPException(status_code=404, detail='service not found')
        if not verify_user(tenant, service_staff_data.user_id):
            raise HTTPException(status_code=404, detail='service not found')
        service_staff = ServiceStaff(**service_staff_data.dict())
        db.add(service_staff)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(service_staff)
        return service_staff
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_service_staff(db: Session, service_staff_id: int, update_data: ServiceStaffUpdate):
    """Update an existing service staff entry's details.
    
    Args:
        db (Session): Database session.
        service_staff_id (int): Unique identifier of the service staff entry to be updated.
        update_data (ServiceStaffUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        ServiceStaff: The updated service staff object.
    
    Raises:
        HTTPException: If the service staff entry is not found or update fails.
    """
    try:
        service_staff = get_service_staff(db, service_staff_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(service_staff, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(service_staff)
        return service_staff
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_service_staff(db: Session, service_staff_id: int):
    """Delete a service staff entry from the database.
    
    Args:
        db (Session): Database session.
        service_staff_id (int): Unique identifier of the service staff entry to be deleted.
    
    Returns:
        dict: Message confirming service staff deletion.
    
    Raises:
        HTTPException: If the service staff entry is not found or deletion fails.
    """
    try:
        service_staff = get_service_staff(db, service_staff_id)
        db.delete(service_staff)
        db.commit()
        return {"message": "service staff entry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
