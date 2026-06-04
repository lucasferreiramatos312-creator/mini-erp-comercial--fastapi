from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request, HTTPException

async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "sucesso": False,
            "erro": exc.detail
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):

    erros = []

    for erro in exc.errors():
        erros.append(erro["msg"])

    return JSONResponse(
        status_code=422,
        content={
            "sucesso": False,
            "erro": erros
        }
    )