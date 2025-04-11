from controllers.client import get_client, get_all_clients
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def verify_client(tenant, client_id):
   """
   verifies wether user exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      client = get_client(db, client_id)
      if (not client) or (not client.is_active):
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag

def get_all_clients_by_tenant(tenant):
   """
   returns all client to the users
   """
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      clients = get_all_clients(db, skip=0, limit=1000)
      active_clients = list()
      for client in clients:
         if client.is_active:
            active_clients.append(client)
   except:
      active_clients = []
   finally:
      db.close()
      return active_clients
   