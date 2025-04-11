from utils.visit_util import get_current_month_visit_for_carer
from utils.location import estimate_travel_time, find_coordinates, get_distance_in_miles
from utils.user_util import get_carer_users, get_non_carer_users
from datetime import datetime, timedelta
from itertools import groupby
from operator import attrgetter
from config.parameters import *
from schemas.payroll import PayrollCreate
from utils.payroll_util import add_payroll, check_payroll
from utils.email_sender import send_email


def get_month_cutoff_dates(first_day_of_month):
    today = datetime.today()
    today = today.replace(year=first_day_of_month.year, month=first_day_of_month.month, day=first_day_of_month.day)
    start_date = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)  # Ensures we move to the next month
    end_date = next_month.replace(day=1) - timedelta(days=1)  # Last day of the current month
    
    return start_date.date(), end_date.date()

def generate(tenant, user, hours_type, travel_type, first_day_of_month):
    """
    Generates the payroll of carers and non-carer users.
    """
    status_lst = list()
    carer_users = get_carer_users(tenant)
    non_carer_users = get_non_carer_users(tenant)  # You need this function

    all_users = carer_users + non_carer_users
    start_date, end_date = get_month_cutoff_dates(first_day_of_month)

    for user in all_users:
        travel_time = []
        milage = []
        calls = 0
        durations = 0

        if check_payroll(tenant, user.user_id, start_date):
            msg = f"User with user_id: {user.user_id} Payroll for {start_date} already generated"
            status_lst.append(msg)
            print(msg)
            continue

        if user in carer_users:
            visits = get_current_month_visit_for_carer(tenant, user.user_id, start_date, end_date)
            visits.sort(key=lambda x: x.clock_in)

            for date, visit_group in groupby(visits, key=attrgetter("date")):
                start_location = None
                end_location = None
                for daily_visit in visit_group:
                    calls += 1
                    durations += int(daily_visit.duration)
                    end_location = daily_visit.clock_in_location
                    if start_location:
                        start_coordinates = find_coordinates(start_location)
                        end_coordinates = find_coordinates(end_location)
                        travel_time.append(estimate_travel_time(start_coordinates, end_coordinates, daily_visit.clock_in))
                        milage.append(get_distance_in_miles(start_coordinates, end_coordinates))
                    start_location = end_location

            if hours_type == WORK_HOURS:
                hours = durations / 60
            else:
                hours = user.working_hours

            if travel_type == TIME_BASED:
                travel_wage = sum(travel_time) * int(user.travel_rate)
            else:
                travel_wage = sum(milage) * int(user.travel_rate)
        else:
            # Non-carer logic
            hours = user.working_hours
            travel_wage = 0

        hourly_wage = hours * int(user.working_hour_rate)
        grand_total = hourly_wage + travel_wage

        payroll_data = {
            "user_id": user.user_id,
            "calls_entertained": calls,
            "start_date": start_date,
            "end_date": end_date,
            "total_milage": sum(milage) if user in carer_users else 0,
            "total_hours_travelled": sum(travel_time) if user in carer_users else 0,
            "total_hours_worked": hours,
            "grand_total": grand_total
        }

        payroll_check = add_payroll(tenant, PayrollCreate(**payroll_data))
        if payroll_check:
            msg = f"Payroll added for {user.user_id}"
        else:
            msg = f"Unable to add payroll for {user.user_id}"
        status_lst.append(msg)
        print(msg)

    send_email(user.email, "Payroll Generation Update", "\n".join(status_lst))
    return {"response": "Payroll generated"}



        

                
                
                
                


