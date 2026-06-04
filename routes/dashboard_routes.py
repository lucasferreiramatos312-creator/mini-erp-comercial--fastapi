from fastapi import APIRouter, Depends, HTTPException, status
from security.auth import get_current_user
from services.dashboard_service import resumo_dashboard
from utils.logger import logger

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
def dashboard(mes: int = None, ano: int = None, usuario=Depends(get_current_user)):
    
    return resumo_dashboard(usuario, mes, ano)