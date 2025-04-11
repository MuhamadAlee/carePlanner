from config.parameters import *
from sqlalchemy import text
from controllers.tenant import get_tenant_by_name, get_tenant
from config.database import engine, Base, get_db, SessionLocal

def get_super_tenant_id():
   """
   provides the super tenant id of application
   """
   db= SessionLocal()
   tenant = get_tenant_by_name(db=db, tenant_slug_name=SLUG)
   if tenant:
      tenant_id = tenant.tenant_id
   db.close()
   return tenant_id


def verify_tenant(tenant_slug):
   """
   provides the super tenant id of application
   """
   db= SessionLocal()
   tenant = get_tenant_by_name(db=db, tenant_slug_name=tenant_slug)
   if tenant:
      return True
   return False
   


def is_tenant_active(tenant_slug):
   """
   checks wether tenant is active or not
   """
   if tenant_slug ==PUBLIC_TENANT:
      return True
   db= SessionLocal()
   db.execute(text(f"SET search_path TO {PUBLIC_TENANT}"))
   tenant = get_tenant_by_name(db=db, tenant_slug_name=tenant_slug)
   flag = False
   if tenant.subscription_status =='active':
      flag = True
   db.close()
   return flag