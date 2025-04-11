from utils.util import hash_password
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.auth import Token
from config.database import get_db_auth, get_db_by_tenant
from models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import LoginRequest
from utils.tenant_util import verify_tenant
from config.parameters import *
from controllers.auth import create_access_token, revoke_token, get_current_user, get_current_token




auth_router = APIRouter(tags=['authentication'])


@auth_router.post("/login/", response_model=Token)
def login(userdetails: LoginRequest, db: Session = Depends(get_db_auth)):
    tenant_schema = userdetails.tenant
    if userdetails.tenant == SLUG:
        tenant_schema = PUBLIC_TENANT
    db_pkg = get_db_by_tenant(tenant_schema)
    db = next(db_pkg)

    if not verify_tenant(userdetails.tenant):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Tenant does not exist')

    user = db.query(User).filter(User.email == userdetails.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist')
    
    if user.password != hash_password(userdetails.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong Password')
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Disabled User')
    
    return create_access_token(data=user, tenant=tenant_schema)


@auth_router.post("/logout", dependencies=[Depends(get_current_user), Depends(get_current_token)])
async def report_scanner(token: str = Depends(get_current_token)):
    return revoke_token(token)

