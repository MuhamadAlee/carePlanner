from controllers.rotaMedication import get_rota_medication
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text
def verify_medication(tenant, medication_id):
   """
   verifies wether rota exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      medication = get_rota_medication(db, medication_id)
      if not medication:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag