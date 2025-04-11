from config.parameters import *
from controllers.invoice import create_invoice, get_invoice_by_month
from config.database import engine, Base, get_db, SessionLocal
from sqlalchemy import text

def add_invoice(tenant, data):
    """
    add rota invoice to the system 
    """
    
    flag = True
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        invoice = create_invoice(db, data)
        if invoice:
            flag= True
    except:
        flag = False
    finally:
        db.close()
        return flag
    

def check_invoice(tenant, client_id, date):
    """
    get rota invoice to the system 
    """
    
    flag = True
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        invoice = get_invoice_by_month(db,client_id, date)
        if invoice:
            flag= True
    except:
        flag = False
    finally:
        db.close()
        return flag