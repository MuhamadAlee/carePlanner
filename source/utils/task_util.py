from controllers.rotaTask import get_rota_task
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text
def verify_task(tenant, task_id):
   """
   verifies wether rota exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      task = get_rota_task(db, task_id)
      if not task:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag