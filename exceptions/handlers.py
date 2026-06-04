from fastapi.responses import JSONResponse
from fastapi import Request

from exceptions.custom_exceptions import ERPException

async def handler_erp_exception(request: Request, exc: ERPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "sucesso": False,
            "erro": exc.mensagem
        }
    )