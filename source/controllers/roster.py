from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.roster import Roster
from utils.role_util import verify_role_assignment
from schemas.roster import RosterCreate, RosterUpdate
from config.parameters import *
from datetime import date, timedelta
from sqlalchemy import text


def get_month_start_end(some_date):
    start_date = some_date.replace(day=1)  # First day of the month
    next_month = some_date.month % 12 + 1  # Get next month
    next_year = some_date.year + (some_date.month // 12)  # Adjust year if needed
    end_date = date(next_year, next_month, 1) - timedelta(days=1)  # Last day of the month
    return start_date, end_date


def get_roster(db: Session, user_id:int, role_id:int, roster_id: int):
    """Retrieve a Roster by its unique identifier."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            roster = db.query(Roster).filter(Roster.roster_id == roster_id, Roster.user_id==user_id).first()
        else:
            roster = db.query(Roster).filter(Roster.roster_id == roster_id).first()
        if not roster:
            raise HTTPException(status_code=404, detail="Roster not found")
        return roster
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_roster_by_client_id(db: Session,user_id:int, role_id:int, client_id: int, first_day_of_month:date):
    """Retrieve rosters by client ID."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        start_date, end_date =  get_month_start_end(first_day_of_month)
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            rosters = db.query(Roster).filter(
                Roster.client_id == client_id,
                Roster.user_id == user_id,
                Roster.date.between(start_date, end_date)  # Filter for date range
            ).all()
        else:
            rosters = db.query(Roster).filter(
                Roster.client_id == client_id,
                Roster.date.between(start_date, end_date)  # Filter for date range
            ).all()
        if not rosters:
            raise HTTPException(status_code=404, detail="No rosters found for the client")
        return rosters
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_rosters_by_client_id_and_date_range(db: Session, client_id: int, start_date: date, end_date: date):
    """Retrieve roster by user ID and a date range."""
    try:
        rotas = db.query(Roster).filter(
            Roster.client_id == client_id,
            Roster.date.between(start_date, end_date)
        ).all()
        if not rotas:
            raise HTTPException(status_code=404, detail="Visit not found")
        return rotas
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_rosters_by_filters(db: Session, client_id: int, day_of_week: str, start_time: str, end_time: str, date:date):
    """Retrieve rosters based on client_id, day_of_week, start_time, and end_time."""
    try:
        rosters = db.query(Roster).filter(
            Roster.client_id == client_id,
            Roster.day == day_of_week,
            Roster.start_time >= start_time,
            Roster.end_time <= end_time,
            Roster.date == date
        ).all()

        if not rosters:
            raise HTTPException(status_code=404, detail="No matching rosters found")

        return rosters
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    


def get_roster_by_user_id(db: Session, user_id: int, first_day_of_month:date):
    """Retrieve all rosters associated with a specific user."""
    try:
        start_date, end_date = get_month_start_end(first_day_of_month)
        rosters = db.query(Roster).filter(
                Roster.user_id == user_id,
                Roster.date.between(start_date, end_date)  # Filter for date range
            ).all()
        if not rosters:
            raise HTTPException(status_code=404, detail="No rosters found for the user")
        return rosters
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_roster_by_rota_id(db: Session,user_id:int, role_id:int, rota_id: int, first_day_of_month:date):
    """Retrieve all rosters associated with a specific rota."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        role_name = verify_role_assignment(tenant, role_id)
        start_date, end_date = get_month_start_end(first_day_of_month)
        if role_name == CARER:
            rosters = db.query(Roster).filter(
                Roster.rota_id == rota_id,
                Roster.user_id == user_id,
                Roster.date.between(start_date, end_date)  # Filter for date range
            ).all()
        else:
            rosters = db.query(Roster).filter(
                Roster.rota_id == rota_id,
                Roster.date.between(start_date, end_date)  # Filter for date range
            ).all()
        if not rosters:
            raise HTTPException(status_code=404, detail="No rosters found for the rota")
        return rosters
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_rosters(db: Session, user_id:int, role_id:int, first_day_of_month:date, skip: int = 0, limit: int = 10):
    """Retrieve all rosters with pagination."""
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        start_date, end_date = get_month_start_end(first_day_of_month)
        role_name = verify_role_assignment(tenant, role_id)
        if role_name == CARER:
            rosters = db.query(Roster).filter(
                Roster.user_id == user_id,
                Roster.date.between(start_date, end_date)  # Filter for date range
            ).offset(skip).limit(limit).all()
        else:
            rosters = db.query(Roster).filter(
                Roster.date.between(start_date, end_date)  # Filter for date range
            ).offset(skip).limit(limit).all()
        return rosters
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_roster(db: Session, Roster_data: RosterCreate):
    """Create a new Roster."""
    try:
       
        roster = Roster(**Roster_data.dict())
        db.add(roster)
        db.flush()
        db.commit()
        db.refresh(roster)
        return roster
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_roster(db: Session, roster_id: int, update_data: RosterUpdate):
    """Update an existing Roster."""
    try:
        roster = db.query(Roster).filter(Roster.roster_id == roster_id).first()
        if not roster:
            raise HTTPException(status_code=404, detail="Roster not found")

        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(roster, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(roster)
        return roster
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_roster(db: Session, user_id:int, role_id:int, roster_id: int):
    """Delete a Roster."""
    try:
        roster = get_roster(db, user_id, role_id, roster_id)
        db.delete(roster)
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        return {"message": "Roster deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def get_matching_rosters(db: Session, day: str, start_time: str, end_time: str, date:date, user_id: int):
    """
    Fetches rosters that match the given day, start time, end time, and user ID.

    Args:
        db (Session): Database session.
        day (str): The day of the Roster.
        start_time (str): The start time of the Roster.
        end_time (str): The end time of the Roster.
        date (date): The date of the Roster.
        user_id (int): The user ID associated with the Roster.

    Returns:
        List[Roster]: A list of matching Roster objects.
    """
    return db.query(Roster).filter(
        Roster.day == day,
        Roster.start_time == start_time,
        Roster.end_time == end_time,
        Roster.user_id == user_id,
        Roster.date == date
    ).all()

def get_matching_rosters_with_buffer_at_start(db: Session, day: str, start_time: str, date:date, user_id: int):
    """
    Fetches rosters that match the given day, start time, end time, and user ID.

    Args:
        db (Session): Database session.
        day (str): The day of the Roster.
        start_time (str): The start time of the Roster.
        date (date): The date of the Roster.
        user_id (int): The user ID associated with the Roster.

    Returns:
        List[Roster]: A list of matching Roster objects.
    """
    return db.query(Roster).filter(
        Roster.day == day,
        Roster.end_time == start_time,
        Roster.user_id == user_id,
        Roster.date == date
    ).all()

def get_matching_rosters_with_buffer_at_end(db: Session, day: str, end_time: str, date:date, user_id: int):
    """
    Fetches rosters that match the given day, start time, end time, and user ID.

    Args:
        db (Session): Database session.
        day (str): The day of the Roster.
        start_time (str): The start time of the Roster.
        date (date): The date of the Roster.
        user_id (int): The user ID associated with the Roster.

    Returns:
        List[Roster]: A list of matching Roster objects.
    """
    return db.query(Roster).filter(
        Roster.day == day,
        Roster.start_time == end_time,
        Roster.user_id == user_id,
        Roster.date == date
    ).all()


def get_matching_rosters_based_on_end_time(db: Session, day: str, end_time: str, date: date, user_id: int):
    """
    Fetches rosters that match the given day, start time, end time, and user ID.

    Args:
        db (Session): Database session.
        day (str): The day of the Roster.
        end_time (str): The end time of the Roster.
        date (date): The date of the Roster.
        user_id (int): The user ID associated with the Roster.

    Returns:
        List[Roster]: A list of matching Roster objects.
    """
    return db.query(Roster).filter(
        Roster.day == day,
        Roster.end_time == end_time,
        Roster.user_id == user_id,
        Roster.date==date
    ).all()


