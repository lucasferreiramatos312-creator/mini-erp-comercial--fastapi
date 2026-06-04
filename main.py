from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, produtos_routes
from routes import clientes_routes
from routes import dashboard_routes
from routes import vendas_routes
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from utils.handlers import (
    http_exception_handler,
    validation_exception_handler
)
from exceptions.handlers import handler_erp_exception
from exceptions.custom_exceptions import ERPException


app = FastAPI()

app.add_exception_handler(
    ERPException,
    handler_erp_exception
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(HTTPException,http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(produtos_routes.router)
app.include_router(auth.router)
app.include_router(clientes_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(vendas_routes.router)