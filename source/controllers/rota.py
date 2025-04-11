from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.rota import Rota
from schemas.rota import RotaCreate, RotaUpdate
from utils.client_util import verify_client
from sqlalchemy import func
from sqlalchemy import text

def get_rota(db: Session, rota_id: int):
    """Retrieve a rota by its unique identifier.
    
    Args:
        db (Session): Database session.
        rota_id (int): Unique identifier of the rota.
        
    
    Returns:
        Rota: The retrieved rota object if found.
    
    Raises:
        HTTPException: If the rota is not found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        rota = db.query(Rota).filter(Rota.rota_id == rota_id).first()
        if not rota:
            raise HTTPException(status_code=404, detail="Rota not found")
        if not verify_client(tenant, rota.client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        return rota
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_rota_by_client_id(db: Session, client_id: int):
    """Retrieve a rota by its unique identifier.
    
    Args:
        db (Session): Database session.
        
        client_id (int): Client to which the rota belongs.
    
    Returns:
        Rota: The retrieved rota object if found.
    
    Raises:
        HTTPException: If the rota is not found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        db.execute(text(f"SET search_path TO '{tenant}'"))
        rota = db.query(Rota).filter( Rota.client_id==client_id).all()
        if not rota:
            raise HTTPException(status_code=404, detail="Rota not found")
        return rota
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_rota_by_day_of_week(db: Session, client_id: int, day_of_week: str):
    """Retrieve rotas for a specific day and client.
    
    Args:
        db (Session): Database session.
        
        client_id (int): Client to which the rota belongs.
        day_of_week (str): Day of the week to filter rotas.
    
    Returns:
        List[Rota]: List of matching rotas.
    
    Raises:
        HTTPException: If no rotas are found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        db.execute(text(f"SET search_path TO '{tenant}'"))
        rotas = (
            db.query(Rota)
            .filter(
                Rota.client_id == client_id,
                func.lower(Rota.day_of_week) == day_of_week.lower()  # Case-insensitive comparison
            )
            .all()
        )
        if not rotas:
            raise HTTPException(status_code=404, detail="No rotas found for the given client and day")
        return rotas
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_rota_by_visit_type(db: Session, client_id: int, visit_type: str):
    """Retrieve rotas for a specific visit type and client.
    
    Args:
        db (Session): Database session.
        
        client_id (int): Client to which the rota belongs.
        visit_type (str): Visit type to filter rotas.
    
    Returns:
        List[Rota]: List of matching rotas.
    
    Raises:
        HTTPException: If no rotas are found.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        db.execute(text(f"SET search_path TO '{tenant}'"))
        rotas = (
            db.query(Rota)
            .filter(
                Rota.client_id == client_id,
                func.lower(Rota.visit_type) == visit_type.lower()  # Case-insensitive comparison
            )
            .all()
        )
        if not rotas:
            raise HTTPException(status_code=404, detail="No rotas found for the given client and visit type")
        return rotas
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_rotas(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all rotas with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Rota]: List of rotas.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        rotas = db.query(Rota).offset(skip).limit(limit).all()
        active_rotas = list()
        for rota in rotas:
            if verify_client(tenant, rota.client_id):
                active_rotas.append(rota)
        return active_rotas
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_rota(db: Session, rota_data: RotaCreate):
    """Create a new rota in the database.
    
    Args:
        db (Session): Database session.
        rota_data (RotaCreate): Rota creation data.
        
    
    Returns:
        Rota: The newly created rota object.
    """
    try:    
        rota = Rota(**rota_data.dict())
        db.add(rota)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota)
        return rota
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_rota(db: Session, rota_id: int, update_data: RotaUpdate):
    """Update an existing rota's details.
    
    Args:
        db (Session): Database session.
        rota_id (int): Unique identifier of the rota to be updated.
        update_data (RotaUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Rota: The updated rota object.
    
    Raises:
        HTTPException: If the rota is not found or update fails.
    """
    try:
        rota = get_rota(db, rota_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(rota, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(rota)
        return rota
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_rota(db: Session, rota_id: int):
    """Delete a rota from the database.
    
    Args:
        db (Session): Database session.
        rota_id (int): Unique identifier of the rota to be deleted.
        
    
    Returns:
        dict: Message confirming rota deletion.
    
    Raises:
        HTTPException: If the rota is not found or deletion fails.
    """
    try:
        rota = get_rota(db, rota_id)
        db.delete(rota)
        db.commit()
        return {"message": "Rota deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
