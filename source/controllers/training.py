from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.training import Training
from utils.user_util import verify_user
from schemas.training import TrainingCreate, TrainingUpdate
from sqlalchemy import text
from utils.email_sender import send_email
from utils.user_util import fetch_user

def get_training(db: Session, training_id: int):
    """Retrieve a training record by its unique identifier.
    
    Args:
        db (Session): Database session.
        training_id (int): Unique identifier of the training record.
    
    Returns:
        Training: The retrieved training object if found.
    
    Raises:
        HTTPException: If the training record is not found.
    """
    try:
        training = db.query(Training).filter(Training.training_id == training_id).all()
        if not training:
            raise HTTPException(status_code=404, detail="Training record not found")
        return training
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    

def get_raining_by_user(db: Session, user_id:int):
    """Retrieve a training record by its unique identifier.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the user.
        training_id (int): Unique identifier of the training record.
        
    
    Returns:
        Training: The retrieved training object if found.
    
    Raises:
        HTTPException: If the training record is not found.
    """
    try:
        training = db.query(Training).filter( Training.user_id==user_id).all()
        if not training:
            raise HTTPException(status_code=404, detail="Training record not found")
        return training
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_trainings(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all training records with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Training]: List of training records.
    """
    try:
        return db.query(Training).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_training(db: Session, training_data: TrainingCreate):
    """Create a new training record in the database.
    
    Args:
        db (Session): Database session.
        training_data (TrainingCreate): Training creation data.
        
    
    Returns:
        Training: The newly created training object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        if not verify_user(tenant, training_data.user_id):
            raise HTTPException(status_code=404, detail='User does not exist in the tenant')
        training = Training(**training_data.dict())
        db.add(training)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(training)
        user = fetch_user(tenant, training.user_id)
        send_email(user.email, "Traning Scheduled", f"Respected staff your training <b>{training.training_name}</b> is scheduled and due till {training.expiry_date}.")
        return training
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_training(db: Session, training_id: int, update_data: TrainingUpdate):
    """Update an existing training record.
    
    Args:
        db (Session): Database session.
        training_id (int): Unique identifier of the training record to be updated.
        update_data (TrainingUpdate): Data containing the fields to update (partial updates allowed).
        
    
    Returns:
        Training: The updated training object.
    
    Raises:
        HTTPException: If the training record is not found or update fails.
    """
    try:

        training = get_training(db, training_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(training, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(training)
        return training
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_training(db: Session, training_id: int):
    """Delete a training record from the database.
    
    Args:
        db (Session): Database session.
        training_id (int): Unique identifier of the training record to be deleted.
        
    
    Returns:
        dict: Message confirming training record deletion.
    
    Raises:
        HTTPException: If the training record is not found or deletion fails.
    """
    try:
        training = get_training(db, training_id)
        db.delete(training)
        db.commit()
        return {"message": "Training record deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
