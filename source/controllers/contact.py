from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.contact import Contact
from utils.client_util import verify_client
from schemas.contact import ContactCreate, ContactUpdate
from sqlalchemy import create_engine, MetaData, text

def get_contact(db: Session, contact_id: int):
    """Retrieve a contact by its unique identifier.
    
    Args:
        db (Session): Database session.
        contact_id (int): Unique identifier of the contact.
        
    
    Returns:
        Contact: The retrieved contact object if found.
    
    Raises:
        HTTPException: If the contact is not found.
    """
    try:
        contact = db.query(Contact).filter(Contact.contact_id == contact_id).all()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_contact_by_client(db: Session, client_id: int):
    """Retrieve a contact by its unique identifier.
    
    Args:
        db (Session): Database session.
        client_id (int): Unique identifier of the user.
        
    
    Returns:
        Contact: The retrieved contact object if found.
    
    Raises:
        HTTPException: If the contact is not found.
    """
    try:
        contact = db.query(Contact).filter(Contact.client_id == client_id).all()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_contacts(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all contacts with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Contact]: List of contacts.
    """
    try:
        return db.query(Contact).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_contact(db: Session, contact_data: ContactCreate):
    """Create a new contact in the database.
    
    Args:
        db (Session): Database session.
        contact_data (ContactCreate): Contact creation data.
        
    
    Returns:
        Contact: The newly created contact object.
    """
    try:   
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_client(tenant, contact_data.client_id):
            raise HTTPException(status_code=404, detail="Client does not exist in tenant")
        contact = Contact(**contact_data.dict())
        db.add(contact)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(contact)
        return contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_contact(db: Session, contact_id: int, update_data: ContactUpdate):
    """Update an existing contact's details.
    
    Args:
        db (Session): Database session.
        contact_id (int): Unique identifier of the contact to be updated.
        update_data (ContactUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Contact: The updated contact object.
    
    Raises:
        HTTPException: If the contact is not found or update fails.
    """
    try:
        contact_check = db.query(Contact).filter(Contact.contact_id == contact_id).first()
        if not contact_check:
            raise HTTPException(status_code=404, detail="Contact not found")
        contact = get_contact(db, contact_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(contact, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(contact)
        return contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_contact(db: Session, contact_id: int):
    """Delete a contact from the database.
    
    Args:
        db (Session): Database session.
        contact_id (int): Unique identifier of the contact to be deleted.
        
    
    Returns:
        dict: Message confirming contact deletion.
    
    Raises:
        HTTPException: If the contact is not found or deletion fails.
    """
    try:
        contact = get_contact(db, contact_id)
        db.delete(contact)
        db.commit()
        return {"message": "Contact deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
