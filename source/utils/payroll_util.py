from config.parameters import *
from controllers.payroll import create_payroll, get_payroll_by_month
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def add_payroll(tenant, data):
    """
    add rota payroll to the system 
    """
    
    flag = True
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        payroll = create_payroll(db, data)
        if payroll:
            flag= True
    except:
        flag = False
    finally:
        db.close()
        return flag
    

def check_payroll(tenant, user_id, date):
    """
    get rota payroll to the system 
    """
    
    flag = True
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        payroll = get_payroll_by_month(db,user_id, date)
        if payroll:
            flag= True
    except:
        flag = False
    finally:
        db.close()
        return flag