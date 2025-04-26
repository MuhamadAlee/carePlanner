from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.service import Service
from schemas.service import ServiceCreate, ServiceUpdate
from utils.client_util import verify_client
from sqlalchemy import func
from sqlalchemy import text

def get_service(db: Session, service_id: int):
    """Retrieve a service by its unique identifier.
    
    Args:
        db (Session): Database session.
        service_id (int): Unique identifier of the service.
        
    
    Returns:
        service: The retrieved service object if found.
    
    Raises:
        HTTPException: If the service is not found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        service = db.query(Service).filter(Service.service_id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="service not found")
        if not verify_client(tenant, service.client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        return service
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_service_by_client_id(db: Session, client_id: int):
    """Retrieve a service by its unique identifier.
    
    Args:
        db (Session): Database session.
        
        client_id (int): Client to which the service belongs.
    
    Returns:
        service: The retrieved service object if found.
    
    Raises:
        HTTPException: If the service is not found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        db.execute(text(f"SET search_path TO '{tenant}'"))
        service = db.query(Service).filter( Service.client_id==client_id).all()
        if not service:
            raise HTTPException(status_code=404, detail="service not found")
        return service
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_service_by_day_of_week(db: Session, client_id: int, day_of_week: str):
    """Retrieve services for a specific day and client.
    
    Args:
        db (Session): Database session.
        
        client_id (int): Client to which the service belongs.
        day_of_week (str): Day of the week to filter services.
    
    Returns:
        List[Service]: List of matching services.
    
    Raises:
        HTTPException: If no services are found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        db.execute(text(f"SET search_path TO '{tenant}'"))
        services = (
            db.query(Service).filter(Service.client_id == client_id,
                func.lower(Service.day_of_week) == day_of_week.lower()  # Case-insensitive comparison
            )
            .all()
        )
        if not services:
            raise HTTPException(status_code=404, detail="No services found for the given client and day")
        return services
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_service_by_visit_type(db: Session, client_id: int, visit_type: str):
    """Retrieve services for a specific visit type and client.
    
    Args:
        db (Session): Database session.
        
        client_id (int): Client to which the service belongs.
        visit_type (str): Visit type to filter services.
    
    Returns:
        List[service]: List of matching services.
    
    Raises:
        HTTPException: If no services are found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        db.execute(text(f"SET search_path TO '{tenant}'"))
        services = (
            db.query(Service)
            .filter(
                Service.client_id == client_id,
                func.lower(Service.visit_type) == visit_type.lower()  # Case-insensitive comparison
            )
            .all()
        )
        if not services:
            raise HTTPException(status_code=404, detail="No services found for the given client and visit type")
        return services
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_services(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all services with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Service]: List of services.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        services = db.query(Service).offset(skip).limit(limit).all()
        active_services = list()
        for service in services:
            if verify_client(tenant, service.client_id):
                active_services.append(Service)
        return active_services
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_service(db: Session, service_data: ServiceCreate):
    """Create a new service in the database.
    
    Args:
        db (Session): Database session.
        service_data (ServiceCreate): Service creation data.
        
    
    Returns:
        service: The newly created service object.
    """
    try:    
        service = Service(**service_data.dict())
        db.add(service)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(service)
        return service
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_service(db: Session, service_id: int, update_data: ServiceUpdate):
    """Update an existing service's details.
    
    Args:
        db (Session): Database session.
        service_id (int): Unique identifier of the service to be updated.
        update_data (serviceUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        service: The updated service object.
    
    Raises:
        HTTPException: If the service is not found or update fails.
    """
    try:
        service = get_service(db, service_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(service, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(Service)
        return service
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_service(db: Session, service_id: int):
    """Delete a service from the database.
    
    Args:
        db (Session): Database session.
        service_id (int): Unique identifier of the service to be deleted.
        
    
    Returns:
        dict: Message confirming service deletion.
    
    Raises:
        HTTPException: If the service is not found or deletion fails.
    """
    try:
        service = get_service(db, service_id)
        db.delete(service)
        db.commit()
        return {"message": "service deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
