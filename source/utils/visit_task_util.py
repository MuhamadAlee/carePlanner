from controllers.serviceTask import get_service_task_by_service_id
from config.database import engine, Base, get_db, SessionLocal
from models.visitTask import VisitTask
from sqlalchemy import text


def verify_visit_tasks(tenant, service_id):
   """
   verifies weather staff had completed all tasks for the patient or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      service_tasks = get_service_task_by_service_id(db, service_id)
      db.execute(text(f"SET search_path TO '{tenant}'"))
      for task in service_tasks:
         visit_provided_tasks = db.query(VisitTask).filter(VisitTask.task_id == task.task_id).all()
         db.execute(text(f"SET search_path TO '{tenant}'"))
         if len(visit_provided_tasks) == 0:
            flag = False
         break
   except:
      flag = False
   finally:
      db.close()
      return flag