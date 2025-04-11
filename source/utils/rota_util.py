from controllers.rota import get_rota, get_rota_by_client_id
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def verify_rota(tenant, rota_id):
   """
   verifies wether rota exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      rota = get_rota(db, rota_id)
      if not rota:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag

def clients_rota(tenant, client_id):
   """
   fetches out the rota id of the client
   """
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      rotas = get_rota_by_client_id(db, client_id)
   except:
      rotas = []
   finally:
      db.close()
      return rotas