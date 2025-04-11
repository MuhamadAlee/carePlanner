from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.role_util import verify_role
from models.user import User
from models.role import Role
from config.parameters import CARER
from schemas.user import UserCreate, UserUpdate
from sqlalchemy import and_
from sqlalchemy import text
from utils.role_util import get_role
from config.parameters import *



def get_user(db: Session, user_id: int):
    """Retrieve a user by its unique identifier.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the user.
       
    
    Returns:
        User: The retrieved user object if found.
    
    Raises:
        HTTPException: If the user is not found.
    """
    try:
        user = db.query(User).filter(User.user_id== user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all users with optional pagination.
    
    Args:
        db (Session): Database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[User]: List of users.
    """
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def get_all_carer_users(db: Session):
    """Retrieve all users with optional pagination.
    
    Args:
        db (Session): Database session.
    
    Returns:
        List[User]: List of users.
    """
    try:
        return db.query(User).join(Role, and_(User.role_id == Role.role_id)).filter( Role.role_name == CARER).all()  
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_all_acitve_users(db: Session):
    """Retrieve all users with optional pagination.
    
    Args:
        db (Session): Database session.
    
    Returns:
        List[User]: List of users.
    """
    try:
        return db.query(User).join(Role, and_(User.role_id == Role.role_id)).filter( Role.role_name != CARER).all()  
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_user_by_email(db: Session, email: str):
    """Retrieve a user by their unique email address.
    
    Args:
        db (Session): Database session.
        email (str): Email address of the user.
       
    
    Returns:
        User: The retrieved user object if found.
    
    Raises:
        HTTPException: If the user is not found.
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_user(db: Session, user_data: UserCreate):
    """Create a new user in the database.
    
    Args:
        db (Session): Database session.
        user_data (UserCreate): User creation data.
       
    
    Returns:
        User: The newly created user object.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        tenant = tenant.split(',')[-1].strip()
        if not verify_role(tenant, user_data.role_id):
            raise HTTPException(status_code=404, detail='Role Does not exist')
        user = User(**user_data.dict())
        db.add(user)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def update_user(db: Session, user_role:str, user_id: int, update_data: UserUpdate):
    """Update an existing user's details.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the user to be updated.
        update_data (UserUpdate): Data containing the fields to update (partial updates allowed).
       
    
    Returns:
        User: The updated user object.
    
    Raises:
        HTTPException: If the user is not found or update fails.
    """
    try:
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        user = get_user(db, user_id)
        user_to_be_updated_role = get_role(db, user.role_id).role_name 
        if user_to_be_updated_role is ADMIN:
            raise HTTPException(status_code=404, detail="Admin's previlleges cannot be changed")
        if user_role == user_to_be_updated_role:
            raise HTTPException(status_code=404, detail="you cannnot update the user")
        if not verify_role(tenant, update_data.role_id):
            raise HTTPException(status_code=404, detail='Role Does not exist')
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_user(db: Session, user_id: int):
    """Delete a user from the database.
    
    Args:
        db (Session): Database session.
        user_id (int): Unique identifier of the user to be deleted.
       
    
    Returns:
        dict: Message confirming user deletion.
    
    Raises:
        HTTPException: If the user is not found or deletion fails.
    """
    try:
        user = get_user(db, user_id)
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))