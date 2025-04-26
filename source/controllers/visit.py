from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.visit import Visit
from schemas.visit import VisitCreate, VisitUpdate, VisitClockedOUtUpdate, VisitCreateClockIn
from utils.client_util import verify_client
from utils.user_util import verify_user
from utils.roster_util import verify_roster, get_my_roster
from utils.role_util import verify_role_assignment
from utils.visit_med_util import verify_visit_medications
from utils.visit_task_util import verify_visit_tasks
from config.parameters import *
from datetime import date
from sqlalchemy import text
from sqlalchemy import func


def get_visit(db: Session, user_id:int, role_id:int, visit_id: int):
    """Retrieve a visit by its unique identifier.
    
    Args:
        db (Session): Database session.
        visit_id (int): Unique identifier of the visit.
        
    
    Returns:
        Visit: The retrieved visit object if found.
    
    Raises:
        HTTPException: If the visit is not found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment( tenant, role_id)
        if role_name == CARER:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id, Visit.user_id==user_id).first()
        else:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_visit_by_client_id(db: Session, user_id:int, role_id:int, client_id: int):
    """Retrieve a visit by client ID."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            visit = db.query(Visit).filter(Visit.client_id == client_id, Visit.user_id==user_id).all()
        else:
            visit = db.query(Visit).filter(Visit.client_id == client_id).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_visit_by_roster_id(db: Session, user_id:int, role_id:int, roster_id: int):
    """Retrieve a visit by Roster ID."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            visit = db.query(Visit).filter(Visit.roster_id == roster_id, Visit.user_id==user_id).all()
        else:
            visit = db.query(Visit).filter(Visit.roster_id == roster_id).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_visit_by_user_id(db: Session, user_id: int):
    """Retrieve a visit by user ID."""
    try:
        visit = db.query(Visit).filter(Visit.user_id == user_id).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def create_visit(db: Session, user_id:int, role_id:int, visit_data: VisitCreate):
    """Create a new visit in the database.
    
    Args:
        db (Session): Database session.
        visit_data (VisitCreate): Visit creation data.
        
    
    Returns:
        Visit: The newly created visit object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if ((not verify_user(tenant, visit_data.user_id)) or 
            (not verify_client(tenant, visit_data.client_id)) or 
            (not verify_roster(tenant, user_id, role_id, visit_data.roster_id))):
            raise HTTPException(status_code=400, detail="Either Client, User or Roster does not found")
        visit = Visit(**visit_data.dict())
        visit.status = VISIT_REVIEW_PENDING
        db.add(visit)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit)
        return visit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def create_visit_for_clockin(db: Session, role_id:int, visit_data: VisitCreateClockIn, user_id: int):
    """Create a new visit in the database.
    
    Args:
        db (Session): Database session.
        visit_data (VisitCreateClockIn): Visit creation data.
        
    
    Returns:
        Visit: The newly created visit object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if ((not verify_client(tenant, visit_data.client_id)) or 
            (not verify_roster(tenant, user_id, role_id, visit_data.roster_id))):
            raise HTTPException(status_code=400, detail="Either Client, User or Roster does not found")
        
        visit = Visit(**visit_data.dict(), user_id=user_id, clock_out_location=None, clock_out=None)
        visit.status =VISIT_REVIEW_PENDING
        db.add(visit)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit)
        return visit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
def get_all_visits(db: Session, user_id:int, role_id:int, skip: int = 0, limit: int = 10):
    """Retrieve all visits with optional pagination.

    Args:
        db (Session): Database session.
        
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[Visit]: List of visits.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            return db.query(Visit).filter(Visit.user_id==user_id).offset(skip).limit(limit).all()
        return db.query(Visit).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def update_visit(db: Session, visit_id: int, update_data: VisitUpdate):
    """Update an existing visit's details.
    
    Args:
        db (Session): Database session.
        visit_id (int): Unique identifier of the visit to be updated.
        update_data (VisitUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Visit: The updated visit object.
    
    Raises:
        HTTPException: If the visit is not found or update fails.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if ((not verify_user(tenant, update_data.user_id)) or 
            (not verify_client(tenant, update_data.client_id)) or 
            (not verify_roster(tenant, update_data.roster_id))):
            raise HTTPException(status_code=400, detail="Either Client, User or Roster does not found")
        visit = get_visit(db, visit_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(visit, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit)
        return visit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update_clockout_visit(db: Session,user_id:int, role_id:int, visit_id: int, update_data: VisitClockedOUtUpdate):
    """Update an existing visit's details.
    
    Args:
        db (Session): Database session.
        visit_id (int): Unique identifier of the visit to be updated.
        update_data (VisitClockedOUtUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Visit: The updated visit object.
    
    Raises:
        HTTPException: If the visit is not found or update fails.
    """
    try:
        visit = get_visit(db,user_id, role_id, visit_id)
        visit.status = VISIT_REVIEW_PENDING
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        roster = get_my_roster(tenant, user_id, role_id, visit.roster_id)
        medication_check = verify_visit_medications(tenant, roster.service_id)
        db.execute(text(f"SET search_path TO {tenant}"))
        tasks_check = verify_visit_tasks(tenant, roster.service_id)
        db.execute(text(f"SET search_path TO {tenant}"))
        if not medication_check:
            raise HTTPException(status_code=404, detail ="Service Medications not Given")
        if not tasks_check:
            raise HTTPException(status_code=404, detail ="Service Tasks not completed")
        
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(visit, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit)
        return visit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_visit(db: Session, visit_id: int):
    """Delete a visit from the database.
    
    Args:
        db (Session): Database session.
        visit_id (int): Unique identifier of the visit to be deleted.
        
    
    Returns:
        dict: Message confirming visit deletion.
    
    Raises:
        HTTPException: If the visit is not found or deletion fails.
    """
    try:
        visit = get_visit(db, visit_id)
        db.delete(visit)
        db.commit()
        return {"message": "Visit deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_visit_by_client_id_and_date(db: Session, user_id: int, role_id: int, client_id: int, visit_date: date):
    """Retrieve a visit by client ID and a specific date."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            visit = db.query(Visit).filter(
                Visit.client_id == client_id,
                Visit.user_id == user_id,
                Visit.date == visit_date
            ).all()
        else:
            visit = db.query(Visit).filter(
                Visit.client_id == client_id,
                Visit.date == visit_date
            ).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_visit_by_user_id_and_date(db: Session, user_id: int, visit_date: date):
    """Retrieve a visit by user ID and a specific date."""
    try:
        visit = db.query(Visit).filter(
            Visit.user_id == user_id,
            Visit.date == visit_date
        ).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_visit_by_client_id_and_date_range(db: Session, user_id: int, role_id: int, client_id: int, start_date: date, end_date: date):
    """Retrieve visits by client ID and a date range."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            visit = db.query(Visit).filter(
                Visit.client_id == client_id,
                Visit.user_id == user_id,
                Visit.date.between(start_date, end_date)
            ).all()
        else:
            visit = db.query(Visit).filter(
                Visit.client_id == client_id,
                Visit.date.between(start_date, end_date)
            ).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_visit_by_client_id_and_date_range_without_user(db: Session, client_id: int, start_date: date, end_date: date):
    """Retrieve visits by client ID and a date range."""
    try:
       
        visit = db.query(Visit).filter(
            Visit.client_id == client_id,
            Visit.date.between(start_date, end_date)
        ).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_visit_by_user_id_and_date_range(db: Session, user_id: int, start_date: date, end_date: date):
    """Retrieve visits by user ID and a date range."""
    try:
        visit = db.query(Visit).filter(
            Visit.user_id == user_id,
            Visit.date.between(start_date, end_date)
        ).all()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_pending_visits_by_date_range(db: Session, start_date: date, end_date: date):
    """Retrieve all pending visits within a date range."""
    try:
        visits = db.query(Visit).filter(
            Visit.status == VISIT_REVIEW_PENDING,
            Visit.date.between(start_date, end_date)
        ).all()
        if not visits:
            raise HTTPException(status_code=404, detail="No pending visits found")
        return visits
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

def get_pending_visits_by_user_id_and_date_range(db: Session, user_id: int, start_date: date, end_date: date):
    """Retrieve pending visits by user ID and a date range."""
    try:
        visits = db.query(Visit).filter(
            Visit.user_id == user_id,
            Visit.status == VISIT_REVIEW_PENDING,
            Visit.date.between(start_date, end_date)
        ).all()
        if not visits:
            raise HTTPException(status_code=404, detail="No pending visits found for this user")
        return visits
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

def get_pending_visits_by_client_id_and_date_range(db: Session, client_id: int, start_date: date, end_date: date):
    """Retrieve pending visits by client ID and a date range."""
    try:
        visits = db.query(Visit).filter(
            Visit.client_id == client_id,
            Visit.status == VISIT_REVIEW_PENDING,
            Visit.date.between(start_date, end_date)
        ).all()
        if not visits:
            raise HTTPException(status_code=404, detail="No pending visits found for this client")
        return visits
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def approve_visit(db:Session, visit_id:int):
    """
    approves the visit based on the visit id
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
        visit.status = VISIT_REVIEW_APPROVAL
        db.flush()
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(visit)
        return visit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
def get_visits_with_missing_or_short_notes(db: Session):
    """
    Retrieve visits where notes are either missing or shorter than the specified min_length.
    """
    try:
        visits = db.query(Visit).filter(
            (Visit.notes == None) | 
            (Visit.notes == "") |
            (func.length(Visit.notes) < 10)
        ).all()
        if not visits:
            raise HTTPException(status_code=404, detail="No visits found with missing or short notes")
        return visits
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


