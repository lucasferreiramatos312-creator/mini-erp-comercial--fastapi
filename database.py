import pyodbc

def conectar():
    conexao = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=SistemaVendas;"
        "Trusted_Connection=yes;"
    )
    return conexao