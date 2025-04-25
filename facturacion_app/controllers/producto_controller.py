import decimal
from tkinter import messagebox
from facturacion_app.controllers.base_controller import BaseController
import pyodbc

class ProductoController(BaseController):
    def __init__(self):
        super().__init__()
        
    def cargar_productos(self, tree_widget):
        if self.db_connection_failed or not self.conexion:
            print("No se pueden cargar productos: conexión fallida o no establecida.")
            return

        self.limpiar_tabla(tree_widget)
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT ProductoID, Codigo, Nombre, PrecioUnitario, TasaImpuesto FROM Productos ORDER BY Nombre")

            for row in cursor.fetchall():
                producto_id, codigo, nombre, precio, tasa_impuesto = row
                precio_formateado = f"{decimal.Decimal(str(precio)):.2f}" if precio is not None else "0.00"
                impuesto_formateado = f"{decimal.Decimal(str(tasa_impuesto)) * 100:.1f}%" if tasa_impuesto is not None else "0.0%"
                values = (producto_id, codigo, nombre, precio_formateado, impuesto_formateado)
                tree_widget.insert('', 'end', values=values)
        except pyodbc.Error as ex:
            print(f"Error al cargar productos: {ex}")
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los productos.\nError: {ex}")

    def registrar_producto(self, datos):
        if self.db_connection_failed or not self.conexion:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return False

        if not datos['codigo'] or not datos['nombre']:
            messagebox.showwarning("Datos Incompletos", "Código y Nombre son obligatorios.")
            return False

        try:
            precio_unitario = decimal.Decimal(datos['precio'])
            tasa_impuesto = decimal.Decimal(datos['impuesto']) / 100
            if not (0 <= tasa_impuesto <= 1):
                raise ValueError("La tasa de impuesto debe estar entre 0 y 100.")
        except (ValueError, decimal.InvalidOperation) as e:
            messagebox.showwarning("Datos Inválidos", f"Precio y Tasa de Impuesto deben ser números válidos.\nError: {e}")
            return False

        try:
            cursor = self.conexion.cursor()
            sql = """
            INSERT INTO Productos (Codigo, Nombre, Descripcion, PrecioUnitario, UnidadMedida, TasaImpuesto)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (
                datos['codigo'],
                datos['nombre'],
                datos['descripcion'],
                precio_unitario,
                datos['unidad'],
                tasa_impuesto
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