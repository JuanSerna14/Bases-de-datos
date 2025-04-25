import decimal
import traceback
from tkinter import messagebox
from facturacion_app.models.item_factura import ItemFactura
from facturacion_app.controllers.base_controller import BaseController
import pyodbc

class FacturaController(BaseController):
    def __init__(self):
        super().__init__()
        self.cliente_id_factura = None
        self.items_factura = []
        
    def buscar_cliente(self, identificacion):
        if self.db_connection_failed or not self.conexion:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return None

        if not identificacion:
            messagebox.showwarning("Campo Vacío", "Ingrese una identificación de cliente para buscar.")
            return None

        try:
            cursor = self.conexion.cursor()
            sql = "SELECT ClienteID, Nombre FROM Clientes WHERE Identificacion = ?"
            cursor.execute(sql, (identificacion,))
            return cursor.fetchone()
        except pyodbc.Error as ex:
            print(f"Error de BD al buscar cliente: {ex}")
            messagebox.showerror("Error de Base de Datos", f"Error al buscar cliente: {ex}")
            return None

    def agregar_item(self, codigo, cantidad, descuento_porcentaje):
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
                
            descuento_tasa = decimal.Decimal(descuento_porcentaje) / 100
            if not (0 <= descuento_tasa <= 1):
                raise ValueError("El descuento debe estar entre 0 y 100.")
        except (ValueError, decimal.InvalidOperation) as e:
            messagebox.showwarning("Dato Inválido", f"Datos incorrectos: {e}")
            return None

        try:
            cursor = self.conexion.cursor()
            sql = "SELECT ProductoID, Nombre, PrecioUnitario, TasaImpuesto FROM Productos WHERE Codigo = ?"
            cursor.execute(sql, (codigo,))
            producto = cursor.fetchone()

            if not producto:
                messagebox.showwarning("No Encontrado", f"Producto con código '{codigo}' no encontrado.")
                return None

            return ItemFactura(
                producto_id=producto.ProductoID,
                codigo=codigo,
                nombre=producto.Nombre,
                cantidad=cantidad,
                precio_unitario=producto.PrecioUnitario,
                descuento_tasa=descuento_tasa,
                tasa_impuesto=producto.TasaImpuesto
            )
        except pyodbc.Error as ex:
            print(f"Error de BD al buscar producto: {ex}")
            messagebox.showerror("Error de Base de Datos", f"Error al buscar producto: {ex}")
            return None

    def crear_factura(self):
        if not self.cliente_id_factura or not self.items_factura:
            return None

        try:
            cursor = self.conexion.cursor()
            
            # Insertar cabecera de factura
            sql_insert_factura = """
            INSERT INTO Facturas (ClienteID, FechaEmision)
            OUTPUT inserted.FacturaID
            VALUES (?, GETDATE());
            """
            cursor.execute(sql_insert_factura, (self.cliente_id_factura,))
            factura_id = cursor.fetchone()[0]
            
            # Generar número de factura
            numero_factura = f"FAC-{factura_id:06d}"
            cursor.execute("UPDATE Facturas SET NumeroFactura = ? WHERE FacturaID = ?", (numero_factura, factura_id))
            
            # Insertar detalles y calcular totales
            total_bruto = decimal.Decimal(0)
            total_descuento = decimal.Decimal(0)
            total_impuestos = decimal.Decimal(0)
            
            sql_insert_detalle = """
            INSERT INTO DetalleFactura
            (FacturaID, ProductoID, Cantidad, PrecioUnitario, Descuento, Subtotal, Impuesto)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            for item in self.items_factura:
                subtotal_bruto = decimal.Decimal(item.cantidad) * item.precio_unitario
                descuento = subtotal_bruto * item.descuento_tasa
                subtotal_neto = subtotal_bruto - descuento
                impuesto = subtotal_neto * item.tasa_impuesto
                
                cursor.execute(sql_insert_detalle, (
                    factura_id,
                    item.producto_id,
                    item.cantidad,
                    item.precio_unitario,
                    item.descuento_tasa,
                    subtotal_neto,
                    impuesto
                ))
                
                total_bruto += subtotal_bruto
                total_descuento += descuento
                total_impuestos += impuesto
            
            total_neto = total_bruto - total_descuento + total_impuestos
            
            # Actualizar totales en la factura
            sql_update_totales = """
            UPDATE Facturas SET
            TotalBruto = ?, TotalDescuento = ?, TotalImpuestos = ?, TotalNeto = ?
            WHERE FacturaID = ?
            """
            cursor.execute(sql_update_totales, (
                total_bruto,
                total_descuento,
                total_impuestos,
                total_neto,
                factura_id
            ))
            
            self.conexion.commit()
            return numero_factura
            
        except pyodbc.Error as ex:
            print(f"Error de BD al crear factura: {ex}")
            traceback.print_exc()
            if self.conexion:
                self.conexion.rollback()
            raise ex
        except Exception as e:
            print(f"Error inesperado al crear factura: {e}")
            traceback.print_exc()
            if self.conexion:
                self.conexion.rollback()
            raise e

    def limpiar_factura(self):
        self.cliente_id_factura = None
        self.items_factura = []