import mysql.connector
from datetime import datetime
def conectar_db():
    # Estabelece a conexão com o banco de dados.
    try:
        return mysql.connector.connect(
            host='localhost',  
            user='marina',    
            password='projeto123',  
            database='projeto_despesas' 
        )
    except mysql.connector.Error as err:
        print(f'Erro na conexão: {err}')
        return None

conn = conectar_db()

def inserir_dados(tipo, data, valor):
    data_formatada = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
    #Cadastra uma nova despesa no banco de dados.
    cursor = None
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            sql = 'INSERT INTO despesas (Tipo, Dt, Valor) VALUES (%s, %s, %s)'
            values = (tipo, data_formatada, valor)
            cursor.execute(sql, values)
            conn.commit()
            return True
    except mysql.connector.Error as err:
        print(f'Erro ao inserir dados: {err}')
        return False
    finally:
        if cursor is not None:
            cursor.close()

def listar_despesas():
    #Retorna uma lista de todas as despesas no banco de dados.
    cursor = None
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT ID, Tipo, Dt, Valor FROM despesas;')
            despesas = cursor.fetchall()
            return despesas if despesas else []
    except mysql.connector.Error as e:
        print(f'Erro ao listar despesas: {e}')
    finally:
        if cursor is not None:
            cursor.close()
    return []
