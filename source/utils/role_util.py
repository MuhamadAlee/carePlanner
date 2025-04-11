from config.parameters import *
from controllers.role import get_role_by_name, get_role
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def get_super_role_id():
   """
   provides the super role of application
   """
   db= SessionLocal()
   role = get_role_by_name(db=db, role_name=ROLE_NAME)
   if role:
      role_id = role.role_id
   db.close()
   return role_id

def verify_role( tenant, role_id):
   """
   verifies wether role exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      role = get_role(db, role_id)
      if not role:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag

def verify_role_assignment(tenant, role_id):
   """
   verifies wether role exists in the tenant or not
   """
   role_name= None
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      role = get_role(db, role_id)
      if role:
         role_name = role.role_name
   except:
      role_name=None
   finally:
      db.close()
      return role_name