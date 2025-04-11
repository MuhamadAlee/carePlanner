from utils.client_util import get_all_clients_by_tenant
from utils.user_util import get_carer_users
from utils.rota_util import clients_rota
from utils.roster_util import add_rota_roster, check_availability, get_ending_roster_for_time, check_existing_rota
from utils.availability_util import check_availability_with_scheduled_hours
from utils.location import get_distance, find_coordinates
from schemas.roster import RosterCreate
from datetime import datetime, timedelta
from collections import defaultdict
import heapq
from utils.email_sender import send_email
import time



def get_sorted_dates_with_days(first_day_of_month):
    
    today = datetime.today()
    today = today.replace(year=first_day_of_month.year, month=first_day_of_month.month, day=first_day_of_month.day)
    year, month = today.year, today.month
    first_day = datetime(year, month, 1)

    dates = []
    current_day = first_day
    while current_day.month == month:
        dates.append((current_day.strftime("%Y-%m-%d"), current_day.strftime("%A")))
        current_day += timedelta(days=1)

    dates_with_days = sorted(dates)
    day_to_dates = defaultdict(list)
    for date, weekday in dates_with_days:
        day_to_dates[weekday].append(date)

    return day_to_dates

def add_rota( tenant, user_id, client_id, rota_id, start_time, end_time, day, date):
    """
    Adds a rota Roster for a user-client assignment.
    
    Args:
        user_id (str): The ID of the assigned user.
        client_id (str): The ID of the client.
        rota_id (str): The ID of the rota schedule.
        start_time (str): The starting time of the shift.
        end_time (str): The ending time of the shift.
        day (str): The day of the week for the shift.
        date(date): date of the current day

    Returns:
        dict: Response from the add_rota_roster function.
    """
    data = {
        "user_id": user_id,
        "client_id": client_id,
        "rota_id": rota_id,
        "start_time": start_time,
        "end_time": end_time,
        "day": day,
        "date": date
    }
    return add_rota_roster(tenant, RosterCreate(**data))


def schedule(tenant, first_day_of_month):
    """
    Schedules users to clients based on the shortest travel distance.

    Args:
        first_day_of_month (str): first_day_of_month.

    Returns:
        dict: Response indicating scheduling is complete.
    """
    status_lst = list()
    # Get all users (carers) and clients for the given tenant
    users = get_carer_users(tenant)
    # working hour limit logic need to be placed here
    clients = get_all_clients_by_tenant(tenant)

    # Precompute each user's home location coordinates to avoid redundant calculations
    # user_coordinates = {user.user_id: find_coordinates(user.address) for user in users}
    user_coordinates = {user.user_id: (time.sleep(60), find_coordinates(user.address))[1] for user in users}
    # current month with days
    day_with_dates = get_sorted_dates_with_days(first_day_of_month)
    for client in clients:
        # Get all rotas assigned to the current client
        client_all_rotas = clients_rota(tenant, client.client_id)
        if not client_all_rotas:
            continue  # Skip clients with no rota

        # Compute client location coordinates once
        client_location_coordinates = find_coordinates(client.location)

        for rota in client_all_rotas:
            staff_requirement = int(rota.staff_required)  # Number of staff required
            day = rota.day_of_week
            for date in day_with_dates.get(day):

                start_time, end_time, rota_id = rota.start_time, rota.end_time, rota.rota_id
                user_distances = []  # List to store (distance, user) tuples

                if not check_existing_rota(tenant, rota.client_id, rota.day_of_week, rota.start_time, rota.end_time, date):
                    msg = f"Rota for Client with client_id : {rota.client_id} on {rota.day_of_week} from {rota.start_time} to {rota.end_time} already existed"
                    status_lst.append(msg)
                    print(msg)
                    continue

                for user in users:
                    # Check if the user is available at the given day and time
                    if not check_availability(tenant, day, start_time, end_time, date, user.user_id):
                        continue
                    if not check_availability_with_scheduled_hours (tenant, day, start_time, end_time, user.user_id):
                        continue

                    # Determine the last Rosterned location for the user, if any
                    last_roster_location = get_ending_roster_for_time(tenant, day, start_time, date, user.user_id)

                    # Use the last Roster's location if available; otherwise, use the home address
                    user_location_coordinates = (
                        find_coordinates(last_roster_location) if last_roster_location else user_coordinates[user.user_id]
                    )

                    # Compute distance between user location and client location
                    distance = get_distance(client_location_coordinates, user_location_coordinates)
                    user_distances.append((distance, user))

                if user_distances:
                    # Select the closest available users based on the required staff count
                    selected_users = [user for _, user in heapq.nsmallest(staff_requirement, user_distances)]

                    # Assign selected users to the rota
                    for selected_user in selected_users:
                        added_rota = add_rota(tenant, selected_user.user_id, client.client_id, rota_id, start_time, end_time, day, date)
                        if add_rota:
                            msg = f"Roster Added for {client.client_id} with {selected_user.user_id} on {day}:{date} from {start_time} to {end_time}"
                            status_lst.append(msg)
                            print(msg)
                        else:
                            msg = f"Unable to add Roster for {client.client_id} with {selected_user.user_id} on {day}:{date} from {start_time} to {end_time}"
                            status_lst.append(msg)
                            print(msg)

                else:
                    msg = f"Unable to add Roster for {client.client_id} on {day}:{date} from {start_time} to {end_time}"
                    status_lst.append(msg)
                    print(msg)

    send_email(user.email, "Rota Scheduling", "\n".join(status_lst))
    return {"response": "Schedule done"}
