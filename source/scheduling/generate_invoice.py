
from utils.client_util import get_all_clients_by_tenant
from datetime import datetime, timedelta
from itertools import groupby
from operator import attrgetter
from config.parameters import *
from schemas.invoice import InvoiceCreate
from utils.visit_util import get_current_month_visit_for_client
from utils.roster_util import get_current_month_rotas_for_client
from utils.invoice_util import add_invoice, check_invoice
from utils.email_sender import send_email


def get_month_cutoff_dates(first_day_of_month):
    today = datetime.today()
    today = today.replace(year=first_day_of_month.year, month=first_day_of_month.month, day=first_day_of_month.day)
    start_date = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)  # Ensures we move to the next month
    end_date = next_month.replace(day=1) - timedelta(days=1)  # Last day of the current month
    seventh_date = today.replace(day=7)  # 7th of the same month
    return start_date.date(), end_date.date(), seventh_date.date()

def time_difference(start_time, end_time):
    
    start_time = start_time.hour*60 + start_time.minute
    end_time = end_time.hour*60 + end_time.minute

    diff = end_time - start_time

    return diff

def minutes_to_hours(minutes):
    hours = minutes / 60
    return hours

def generate(tenant, user, hours_type, first_day_of_month):
    """
    generates the payroll of carers
    """
    status_lst = list()
    clients = get_all_clients_by_tenant(tenant)
    start_date, end_date, seventh_date = get_month_cutoff_dates(first_day_of_month)

    for client in clients:
        if (check_invoice(tenant, client.client_id, start_date)):
            msg = f"User with client_id : {client.client_id} Invoice for {start_date} already generated"
            status_lst.append(msg)
            print(msg)
            continue
        calculated_time = 0
        if hours_type==WORK_HOURS:
            visits = get_current_month_visit_for_client(tenant, client.client_id, start_date, end_date)
            for visit in visits:
                calculated_time += time_difference(visit.clock_in, visit.clock_out)
        else:
            rotas = get_current_month_rotas_for_client(tenant, client.client_id, start_date, end_date)
            for rota in rotas:
                calculated_time += time_difference(rota.start_time, rota.end_time)

        grand_total = minutes_to_hours(calculated_time) * client.charge_rate
        invoice_data = {
            "client_id": client.client_id,
            "start_date": start_date,
            "end_date": end_date,
            "due_date": seventh_date,
            "authority": "Admin",
            "billable_amount": grand_total,
            "payment_status": "Pending"
            }
        invoice_check = add_invoice(tenant, InvoiceCreate(**invoice_data))
        if invoice_check:
            msg = f"Invoice Added for {client.client_id}"
            status_lst.append(msg)
            print(msg)
        else:
            msg = f"Unable to Add Invoice for {client.client_id}"
            status_lst.append(msg)
            print(msg)
    send_email(user.email, "Invoice Generation Update", "\n".join(status_lst))
    return {"response": "Invoice generated"}

