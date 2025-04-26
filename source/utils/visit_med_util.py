from controllers.serviceMedication import get_service_medication_by_service_id
from config.database import engine, Base, get_db, SessionLocal
from models.visitMedication import VisitMedication
from sqlalchemy import text


def verify_visit_medications(tenant, service_id):
   """
   verifies weather staff had provided all medication to the patient or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      service_medications = get_service_medication_by_service_id(db, service_id)
      db.execute(text(f"SET search_path TO '{tenant}'"))
      for med in service_medications:
         visit_medication = db.query(VisitMedication).filter(VisitMedication.medication_id == med.medication_id).all()
         db.execute(text(f"SET search_path TO '{tenant}'"))
         if len(visit_medication) == 0:
            flag = False
         break
   except:
      flag = False
   finally:
      db.close()
      return flag