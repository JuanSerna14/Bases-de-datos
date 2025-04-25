import pyodbc

class Database:
    def __init__(self, server, database, driver):
        self.connection_string = (
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        self.connection = None
        
    def connect(self):
        try:
            self.connection = pyodbc.connect(self.connection_string)
            return True
        except pyodbc.Error as ex:
            print(f"Error de conexión a la base de datos: {ex}")
            return False
            
    def close(self):
        if self.connection:
            self.connection.close()
            
    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except pyodbc.Error as ex:
            print(f"Error al ejecutar consulta: {ex}")
            raise ex