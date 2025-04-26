import os
from dotenv import load_dotenv

load_dotenv()

# database params
DATABASE_USER_NAME = os.getenv('DATABASE_USER_NAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT= os.getenv('DATABASE_PORT')

# tenant parameters
PUBLIC_TENANT = 'public'
USER_NAME = os.getenv('USER_NAME')
SLUG = os.getenv('SLUG')
EMAIL = os.getenv('EMAIL')
SUBSCRIPTION_PLAN = os.getenv('SUBSCRIPTION_PLAN')
SUBSCRIPTION_STATUS= os.getenv('SUBSCRIPTION_STATUS')

# ROLE params
ROLE_NAME = os.getenv('ROLE_NAME')
ROLE_DESCRIPTION = os.getenv('ROLE_DESCRIPTION')

# Super user Params
SUPER_USER_NAME = os.getenv('SUPER_USER_NAME')
SUPER_USER_EMAIL = os.getenv('SUPER_USER_EMAIL')
SUPER_USER_PASSWORD = os.getenv('SUPER_USER_PASSWORD')

SUPER_USER_CONTACT = os.getenv('SUPER_USER_CONTACT')
SUPER_USER_ADDRESS = {
                        "line1": os.getenv('SUPER_USER_ADDRESS_LINE1'),
                        "line2": os.getenv('SUPER_USER_ADDRESS_LINE2'),
                        "postcode": os.getenv('SUPER_USER_ADDRESS_POSTCODE'),
                        "city": os.getenv('SUPER_USER_ADDRESS_CITY'),
                        "county": os.getenv('SUPER_USER_ADDRESS_COUNTY'),
                        "country": os.getenv('SUPER_USER_ADDRESS_COUNTRY')
                    }
SUPER_USER_EMPLOYEE_TYPE =os.getenv('SUPER_USER_EMPLOYEE_TYPE')
SUPER_USER_HOURS = os.getenv('SUPER_USER_HOURS')

# auth params
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

# Roles

SUPER_ADMIN = os.getenv('ROLE_NAME')
ADMIN = 'admin'
OFFICE_USER = 'office_user' #no finanace
CARE_COORDINATOR = 'care_coordinator' # no finance, no user_creation
SUPERVISOR = 'supervisor' # only scheduling thing, rota thing, inspection note (future use)
MONITOR = 'monitor' # reports, statitcs.
CARER = 'carer' # clock in , clock out


TENANT_ROLES = [
    {"role_name": ADMIN, "description": "All Preveliges inside system"},
    {"role_name": OFFICE_USER, "description": "All preveliges excluding Finance"},
    {"role_name": CARE_COORDINATOR, "description": "All preveliges excluding Finanance and User Mgmt"},
    {"role_name": SUPERVISOR, "description": "only scheduling thing, rota thing, inspection note"},
    {"role_name": MONITOR, "description": "reports, statitcs view"},
    {"role_name": CARER, "description": "clock in , clock out and visits to clients"},
]


SUPER_TENANT_ROLES = [
    {"role_name": SUPER_ADMIN, "description": "Manages Tenants"},
    {"role_name": ADMIN, "description": "All Preveliges inside system"},
    {"role_name": OFFICE_USER, "description": "All preveliges excluding Finance"},
    {"role_name": CARE_COORDINATOR, "description": "All preveliges excluding Finanance and User Mgmt"},
    {"role_name": SUPERVISOR, "description": "only scheduling thing, rota thing, inspection note"},
    {"role_name": MONITOR, "description": "reports, statitcs view"},
    {"role_name": CARER, "description": "clock in , clock out and visits to clients"},
]

ROLES = [ROLE_NAME, ADMIN, OFFICE_USER, CARE_COORDINATOR, SUPERVISOR, MONITOR, CARER]

# clocking
CLOCKEDIN = 'clockedIn'
ClOCKEDOUT = 'clockedOut'

# payroll type
WORK_HOURS = 'logged_hours'
SCHEDULED_HOURS =  'scheduled_hours'

# travel type
TIME_BASED = 'travel_time'
MILAGE_BASED   = 'travel_milage'

# mailing parameters

SMTP_SERVER = os.getenv('SMTP_SERVER') 
SMTP_PORT = int(os.getenv('SMTP_PORT') )
SMTP_USERNAME = os.getenv('EMAIL_ADDRESS')
SMTP_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Email Details
FROM_EMAIL = os.getenv('EMAIL_ADDRESS')

# Approval of visit
VISIT_REVIEW_PENDING = 'Pending'
VISIT_REVIEW_APPROVAL = 'Approved'

# Medication
MEDICATION_REFUSED =  'Refused'

#Employee type

EMPLOYEE_TYPE = ['Permanent', 'Contract', 'Zero-Hour Contract']


