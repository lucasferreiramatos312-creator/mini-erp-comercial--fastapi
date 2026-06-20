import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def conectar():
    conexao = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;")
    
    return conexao