from controllers.service import get_service, get_service_by_client_id
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def verify_service(tenant, service_id):
   """
   verifies wether service exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      service = get_service(db, service_id)
      if not service:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag

def clients_service(tenant, client_id):
   """
   fetches out the service id of the client
   """
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      services = get_service_by_client_id(db, client_id)
   except:
      services = []
   finally:
      db.close()
      return services