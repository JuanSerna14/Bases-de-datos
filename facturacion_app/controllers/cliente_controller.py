from facturacion_app.controllers.base_controller import BaseController  # Import absoluto corregido
from tkinter import messagebox
import pyodbc

class ClienteController(BaseController):
    def __init__(self):
        super().__init__()
        
    def cargar_clientes(self, tree_widget):
        if self.db_connection_failed or not self.conexion:
            print("No se pueden cargar clientes: conexión fallida o no establecida.")
            return

        self.limpiar_tabla(tree_widget)
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT ClienteID, Nombre, Identificacion, Telefono FROM Clientes ORDER BY Nombre")

            for row in cursor.fetchall():
                values = [str(val) if val is not None else "" for val in row]
                tree_widget.insert('', 'end', values=values)
        except pyodbc.Error as ex:
            print(f"Error al cargar clientes: {ex}")
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los clientes.\nError: {ex}")

    def registrar_cliente(self, datos):
        if self.db_connection_failed or not self.conexion:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return False

        if not datos['nombre'] or not datos['identificacion']:
            messagebox.showwarning("Datos Incompletos", "El Nombre y la Identificación son obligatorios.")
            return False

        try:
            cursor = self.conexion.cursor()
            sql = """
            INSERT INTO Clientes (Nombre, Identificacion, Direccion, CorreoElectronico, Telefono, FechaRegistro)
            VALUES (?, ?, ?, ?, ?, GETDATE())
            """
            params = (
                datos['nombre'],
                datos['identificacion'],
                datos['direccion'],
                datos['correo'],
                datos['telefono']
            )
            cursor.execute(sql, params)
            self.conexion.commit()
            return True
        except pyodbc.IntegrityError as ex:
            self.conexion.rollback()
            raise ex
        except pyodbc.Error as ex:
            self.conexion.rollback()
            raise ex

    @staticmethod
    def limpiar_tabla(tree_widget):
        if tree_widget.get_children():
            tree_widget.delete(*tree_widget.get_children())