from sqlalchemy import text
from config.database import engine, Base, get_db, SessionLocal
from controllers.userAvailability import get_single_user_availabilities_on_day
def check_availability_with_scheduled_hours(tenant, day, start_time, end_time, user_id):
    """
    check the availability of the user based on the day, start time and end time
    """
    flag = False
    try:
        db= SessionLocal()
        db.execute(text(f"SET search_path TO '{tenant}'"))
        availability = get_single_user_availabilities_on_day(db, user_id, day)
        if availability:
            scheduled_start_time = availability.start_time
            scheduled_end_time = availability.end_time
            if scheduled_start_time <= start_time and end_time <= scheduled_end_time:
                flag = True
            else:
                flag = False
    except:
        flag = False
    finally:
        db.close()
        return flag