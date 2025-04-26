from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.role import Role
from schemas.role import RoleCreate, RoleUpdate
from sqlalchemy import text
from config.parameters import *

def get_role(db: Session, role_id: int):
    """Retrieve a role by its unique identifier.
    
    Args:
        db (Session): Database session.
        role_id (int): Unique identifier of the role.
        
    
    Returns:
        Role: The retrieved role object if found.
    
    Raises:
        HTTPException: If the role is not found.
    """
    try:
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_role_by_name(db: Session, role_name: str):
    """Retrieve a role by its unique name.
    
    Args:
        db (Session): Database session.
        role_name (str): Name of the role.
        
    
    Returns:
        Role: The retrieved role object if found.
    
    Raises:
        HTTPException: If the role is not found.
    """
    try:
        role = db.query(Role).filter(Role.role_name == role_name).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def get_all_roles(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve all roles with optional pagination.
    
    Args:
        db (Session): Database session.
        
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
    
    Returns:
        List[Role]: List of roles.
    """
    try:
        return db.query(Role).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def create_role(db: Session, role_data: RoleCreate):
    """Create a new role in the database.
    
    Args:
        db (Session): Database session.
        role_data (RoleCreate): Role creation data.
        
    
    Returns:
        Role: The newly created role object.
    """
    try:
        if role_data.dict()['role_name'] is SUPER_ADMIN:
            raise HTTPException(status_code=404, detail="This role is not allowed to be added")
        if role_data.dict()['role_name'] not in ROLES:
            raise HTTPException(status_code=404, detail="Role name does not allowed in system")
        role = Role(**role_data.dict())
        db.add(role)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        tenant = tenant.split(',')[-1].strip()
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(role)
        return role
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    
def first_time_bulk_role_creation(db: Session, tenant_type='Normal'):
    """Create predefined roles in the database if they don't already exist.

    Args:
        db (Session): Database session.

    Returns:
        List[Role]: List of created role objects.
    """
    try:
        roles_to_create = []

        if tenant_type =='Normal':
            all_roles = TENANT_ROLES
        else:
            all_roles = SUPER_TENANT_ROLES
        for role in all_roles:
            # Check if role already exists to avoid duplicates
            existing_role = db.query(Role).filter_by(role_name=role["role_name"]).first()
            if not existing_role:
                roles_to_create.append(Role(**role))
        
        if roles_to_create:
            db.add_all(roles_to_create)
            db.flush()
            tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
            db.commit()
            db.execute(text(f"SET search_path TO {tenant}"))

            for role in roles_to_create:
                db.refresh(role)

        return roles_to_create

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update_role(db: Session, role_id: int, update_data: RoleUpdate):
    """Update an existing role's details.
    
    Args:
        db (Session): Database session.
        role_id (int): Unique identifier of the role to be updated.
        update_data (RoleUpdate): Data containing the fields to update (partial updates allowed).
    
    Returns:
        Role: The updated role object.
    
    Raises:
        HTTPException: If the role is not found or update fails.
    """
    try:
        if update_data.dict()['role_name'] not in ROLES:
            raise HTTPException(status_code=404, detail="Role name does not allowed in system")
        role = get_role(db, role_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(role, key, value)
        db.flush()
        tenant = db.execute(text("SHOW search_path")).fetchall()[0][0]
        db.commit()
        db.execute(text(f"SET search_path TO {tenant}"))
        db.refresh(role)
        return role
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

def delete_role(db: Session, role_id: int):
    """Delete a role from the database.
    
    Args:
        db (Session): Database session.
        role_id (int): Unique identifier of the role to be deleted.
        
    
    Returns:
        dict: Message confirming role deletion.
    
    Raises:
        HTTPException: If the role is not found or deletion fails.
    """
    try:
        role = get_role(db, role_id)
        db.delete(role)
        db.commit()
        return {"message": "Role deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
