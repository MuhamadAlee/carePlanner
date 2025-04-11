import jwt
from config.parameters import *
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
def get_tenant_from_token(token: str = Depends(oauth2_scheme)):
    try: 
        token_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM, options={ "verify_exp": True})
        tenant = token_data['tenant']
    except:
        tenant = 'public'
    finally:
        return tenant