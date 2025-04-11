from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.client import Client
from schemas.client import ClientCreate, ClientUpdate
from sqlalchemy import create_engine, MetaData, text


def get_client(db: Session, client_id: int):
    """Retrieve a client by its unique identifier.

    Args:
        db (Session): Database session.
        client_id (int): Unique identifier of the client.
        

    Returns:
        Client: The retrieved client object if found.

    Raises:
        HTTPException: If the client is not found.
    """
    try:
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_client_by_name(db: Session, client_name: str):
    """Retrieve a client by its unique identifier.

    Args:
        db (Session): Database session.
        client_name (str): name of the client.
        

    Returns:
        Client: The retrieved client object if found.

    Raises:
        HTTPException: If the client is not found.
    """
    try:
        client = db.query(Client).filter(
            Client.name.ilike(f"%{client_name}%")
            ).all()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_clients(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all clients with optional pagination.

    Args:
        db (Session): Database session.
        
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[Client]: List of clients.
    """
    try:
        return db.query(Client).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_client(db: Session, client_data: ClientCreate):
    """Create a new client in the database.

    Args:
        db (Session): Database session.
        client_data (ClientCreate): Client creation data.
        

    Returns:
        Client: The newly created client object.
    """
    try:
        client = Client(**client_data.dict())
        db.add(client)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(client)
        return client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_client(db: Session, client_id: int, update_data: ClientUpdate):
    """Update an existing client's details.

    Args:
        db (Session): Database session.
        client_id (int): Unique identifier of the client to be updated.
        update_data (ClientUpdate): Data containing the fields to update (partial updates allowed).
        

    Returns:
        Client: The updated client object.

    Raises:
        HTTPException: If the client is not found or update fails.
    """
    try:
        client = get_client(db, client_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(client, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(client)
        return client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_client(db: Session, client_id: int):
    """Delete a client from the database.

    Args:
        db (Session): Database session.
        client_id (int): Unique identifier of the client to be deleted.
        

    Returns:
        dict: Message confirming client deletion.

    Raises:
        HTTPException: If the client is not found or deletion fails.
    """
    try:
        client = get_client(db, client_id)
        db.delete(client)
        db.commit()
        return {"message": "Client deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
