from config.parameters import *
from controllers.client import get_client
from controllers.roster import get_roster
from controllers.roster import create_roster, get_matching_rosters, \
    get_matching_rosters_based_on_end_time, get_rosters_by_filters, \
    get_rosters_by_client_id_and_date_range, get_matching_rosters_with_buffer_at_end, \
    get_matching_rosters_with_buffer_at_start, get_roster
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def verify_roster(tenant, user_id, role_id, roster_id):
   """
   verifies wether roster exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      roster = get_roster(db, user_id, role_id, roster_id)
      if not roster:
         flag = False
   except:
      flag=False
   finally:
      db.close()
      return flag
   
def get_my_roster(tenant, user_id, role_id, roster_id):
   """
   verifies wether roster exists in the tenant or not
   """
   flag = True
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      roster = get_roster(db, user_id, role_id, roster_id)
   except:
      roster=None
   finally:
      db.close()
      return roster

def add_rota_roster(tenant, data):
    """
    add rota roster to the system 
    """
    
    flag = True
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        roster = create_roster(db, data)
        if roster:
            flag= True
    except:
        flag = False
    finally:
        db.close()
        return flag
    

def check_existing_rota(tenant, client_id, day_of_week,start_time, end_time, date):
    """
    check weather rota for client already existed or not
    """
    flag = True
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        rosters = get_rosters_by_filters(db, client_id, day_of_week,start_time, end_time,date)
        if len(rosters)>0:
            flag = False
    except:
        flag = True
    finally:
        db.close()
        return flag

def check_availability(tenant, day, start_time, end_time, date, user_id):
    """
    check the availability of the user based on the day, start time and end time
    """
    flag = True
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        rosters = get_matching_rosters(db, day, start_time, end_time, date, user_id)
        start_rosters = get_matching_rosters_with_buffer_at_start(db, day, start_time, date, user_id)
        end_rosters = get_matching_rosters_with_buffer_at_end(db, day, end_time, date, user_id)
        if (len(rosters)>0) or (len(start_rosters)>0) or (len(end_rosters)>0):
            flag = True
    except:
        flag = False
    finally:
        db.close()
        return flag

def get_ending_roster_for_time(tenant, day, start_time, date, user_id):
    """
    provides the ending roster for users
    """
    roster_location = None
    try:
        db = SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        rosters = get_matching_rosters_based_on_end_time(db, day, start_time, date, user_id)
        for roster in rosters:
            client = get_client(db, roster.client_id)
            roster_location = client.location 
    except:
        roster_location = None
    finally:
        db.close()
        return roster_location
    
def get_current_month_rotas_for_client(tenant, client_id, start_date, end_date):
   """
   fetch all the rotas of the users and client
   """
   try:
      db= SessionLocal()
      db.execute(text(f"SET search_path TO '{tenant}'"))
      rotas = get_rosters_by_client_id_and_date_range(db, client_id, start_date, end_date)
      if not rotas:
         rotas = []
   except:
      rotas =[]
   finally:
      db.close()
      return rotas
   

def get_current_roster(tenant, user_id, role_id, roster_id):
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        roster = get_roster(db,user_id, role_id, roster_id)
    except:
        roster =None
    finally:
        db.close()
        return roster


        

