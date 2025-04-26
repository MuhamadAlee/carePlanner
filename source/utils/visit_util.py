from controllers.visit import get_visit, get_visit_by_user_id_and_date_range, get_visit_by_client_id_and_date_range_without_user
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def verify_visit(tenant, user_id, role_id, visit_id):
   """
   verifies wether rota exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      visit = get_visit(db, user_id, role_id, visit_id)
      if not visit:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag
   
def get_current_month_visit_for_carer(tenant, user_id, start_date, end_date):
   """
   fetch all the visits of the users and client
   """
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      visits = get_visit_by_user_id_and_date_range(db, user_id, start_date, end_date)
      if not visits:
         visits = []
   except:
      visits =[]
   finally:
      db.close()
      return visits
   

def get_current_month_visit_for_client(tenant, client_id, start_date, end_date):
   """
   fetch all the visits of the users and client
   """
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      visits = get_visit_by_client_id_and_date_range_without_user(db, client_id, start_date, end_date)
      if not visits:
         visits = []
   except:
      visits =[]
   finally:
      db.close()
      return visits

