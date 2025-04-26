from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.ServiceMedication import ServiceMedication
from schemas.serviceMedication import ServiceMedicationCreate, ServiceMedicationUpdate
from utils.service_util import verify_service
from utils.roster_util import get_current_roster
from sqlalchemy import text

def get_service_medication(db: Session, medication_id: int):
    """Retrieve a service medication by its unique identifier.
    
    Args:
        db (Session): Database session.
        medication_id (int): Unique identifier of the service medication.
        
    
    Returns:
        ServiceMedication: The retrieved service medication object if found.
    
    Raises:
        HTTPException: If the service medication is not found.
    """
    try:
        service_medication = db.query(ServiceMedication).filter(ServiceMedication.medication_id == medication_id).first()
        if not service_medication:
            raise HTTPException(status_code=404, detail="service Medication not found")
        return service_medication
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_service_medication_by_service_id(db: Session, service_id: int):
    """Retrieve a service medication by its unique identifier.
    
    Args:
        db (Session): Database session.
        service_id (int): Unique identifier of the service medication.
        
    
    Returns:
        ServiceMedication: The retrieved service medication object if found.
    
    Raises:
        HTTPException: If the service medication is not found.
    """
    try:
        service_medication = db.query(ServiceMedication).filter(ServiceMedication.service_id == service_id).all()
        if not service_medication:
            raise HTTPException(status_code=404, detail="service Medication not found")
        return service_medication
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_service_medication_by_roster_id(db: Session, user_id:int, role_id:int, roster_id: int):
    """Retrieve a service medication by its unique identifier.
    
    Args:
        db (Session): Database session.
        roster_id (int): Unique identifier of the service medication.
        
    
    Returns:
        ServiceMedication: The retrieved service medication object if found.
    
    Raises:
        HTTPException: If the service medication is not found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        roster = get_current_roster(tenant, user_id, role_id, roster_id)
        db.execute(text(f"SET search_path TO {tenant}"))
        if roster:
            service_medication = db.query(ServiceMedication).filter(ServiceMedication.service_id == roster.service_id).all()
            if not service_medication:
                raise HTTPException(status_code=404, detail="service Medication not found")
            return service_medication
        raise HTTPException(status_code=404, detail="service Medication not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    


def get_all_service_medications(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all service medications with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[ServiceMedication]: List of service medications.
    """
    try:
        return db.query(ServiceMedication).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_service_medication(db: Session, service_medication_data: ServiceMedicationCreate):
    """Create a new service medication in the database.
    
    Args:
        db (Session): Database session.
        service_medication_data (ServiceMedicationCreate): service medication creation data.
        
    
    Returns:
        ServiceMedication: The newly created service medication object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_service(tenant, service_medication_data.service_id):
            raise HTTPException(status_code=404, detail='Unable to find service')
        service_medication = ServiceMedication(**service_medication_data.dict())
        db.add(service_medication)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(service_medication)
        return service_medication
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_service_medication(db: Session, medication_id: int, update_data: ServiceMedicationUpdate):
    """Update an existing service medication's details.
    
    Args:
        db (Session): Database session.
        medication_id (int): Unique identifier of the service medication to be updated.
        update_data (ServiceMedicationUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        ServiceMedication: The updated service medication object.
    
    Raises:
        HTTPException: If the service medication is not found or update fails.
    """
    try:
        service_medication = get_service_medication(db, medication_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(service_medication, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(service_medication)
        return service_medication
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_service_medication(db: Session, medication_id: int):
    """Delete a service medication from the database.
    
    Args:
        db (Session): Database session.
        medication_id (int): Unique identifier of the service medication to be deleted.
        
    
    Returns:
        dict: Message confirming service medication deletion.
    
    Raises:
        HTTPException: If the service medication is not found or deletion fails.
    """
    try:
        service_medication = get_service_medication(db, medication_id)
        db.delete(service_medication)
        db.commit()
        return {"message": "service Medication deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
