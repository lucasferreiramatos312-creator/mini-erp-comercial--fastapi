import pyodbc

def conectar():
    conexao = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=SistemaEstudos;"
        "Trusted_Connection=yes;"
    )
    return conexao