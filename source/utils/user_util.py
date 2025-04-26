from controllers.user import get_user, get_all_carer_users, get_all_acitve_users
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import create_engine, MetaData, text

def verify_user(tenant, user_id):
   """
   verifies wether user exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      user = get_user(db, user_id)
      if not user:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag
   
def fetch_user(tenant, user_id):
   """
   verifies wether user exists in the tenant or not
   """
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      user = get_user(db, user_id)
      
   except:
      user = None
   finally:
      db.close()
      return user

def is_user_active(tenant, user_id):
   """
   verifies wether user active in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      user = get_user(db, user_id)
      if not user.is_active:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag

def get_carer_users(tenant):
   """
   fetches the carer users of tenant
   """
   db= SessionLocal()
   db.execute(text(f"SET search_path TO '{tenant}'"))
   try:
      users = get_all_carer_users(db)
      active_users = [user for user in users if (user.dbs_status and user.is_active)]
   except:
      active_users = []
   finally:
      db.close()
      return active_users
   

def get_non_carer_users(tenant):
   """
   fetches the carer users of tenant
   """
   db= SessionLocal()
   db.execute(text(f"SET search_path TO '{tenant}'"))
   try:
      users = get_all_acitve_users(db)
   except:
      users = []
   finally:
      db.close()
      return users
   