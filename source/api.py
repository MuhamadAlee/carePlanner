import os
import shutil
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.tenant import tenant_router
from routes.role import role_router
from routes.user import user_router
from routes.auth import auth_router
from routes.training import training_router
from routes.client import client_router
from routes.contact import contact_router
from routes.roster import roster_router
from routes.service import service_router
from routes.serviceStaff import service_staff_router
from routes.serviceTask import service_task_router
from routes.serviceMedication import service_medication_router
from routes.visit import visit_router
from routes.visitTask import visit_task_router
from routes.visitMedication import visit_medication_router
from routes.visitAccident import visit_accident_router
from routes.invoice import invoice_router
from routes.holidayQuota import holiday_quota_router
from routes.holiday import holiday_router
from routes.payroll import payroll_router
from routes.userAvailability import availability_router
from fastapi.openapi.utils import get_openapi


from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="API with JWT authentication",
        routes=app.routes,
    )

    # Define global Bearer auth security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add BearerAuth to every endpoint's method
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema



load_dotenv()
app = FastAPI()
app.openapi = custom_openapi


# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(tenant_router)
app.include_router(role_router)
app.include_router(user_router)
app.include_router(availability_router)
app.include_router(auth_router)
app.include_router(training_router)
app.include_router(client_router)
app.include_router(contact_router)
app.include_router(service_router)
app.include_router(service_staff_router)
app.include_router(service_task_router)
app.include_router(service_medication_router)
app.include_router(roster_router)
app.include_router(visit_router)
app.include_router(visit_task_router)
app.include_router(visit_medication_router)
app.include_router(visit_accident_router)
app.include_router(invoice_router)
app.include_router(holiday_quota_router)
app.include_router(holiday_router)
app.include_router(payroll_router)


if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    uvicorn.run(app=app, host=host, port=port)
