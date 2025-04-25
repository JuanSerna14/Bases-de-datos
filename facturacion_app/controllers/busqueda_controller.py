from facturacion_app.controllers.base_controller import BaseController
import pyodbc

class BusquedaController(BaseController):
    def __init__(self):
        super().__init__()
        
    def buscar_factura(self, factura_id):
        try:
            factura_id = int(factura_id)
        except ValueError:
            raise ValueError("El ID de factura debe ser un número entero")

        try:
            cursor = self.conexion.cursor()
            
            # Obtener cabecera de factura
            sql_factura = """
            SELECT
                f.FacturaID, f.NumeroFactura, f.FechaEmision,
                c.Nombre AS NombreCliente, c.Identificacion AS IdCliente, 
                c.Direccion, c.CorreoElectronico, c.Telefono,
                f.TotalBruto, f.TotalImpuestos, f.TotalDescuento, f.TotalNeto
            FROM Facturas f
            JOIN Clientes c ON f.ClienteID = c.ClienteID
            WHERE f.FacturaID = ?
            """
            cursor.execute(sql_factura, (factura_id,))
            factura = cursor.fetchone()
            
            if not factura:
                return None, None
                
            # Obtener items de la factura
            sql_items = """
            SELECT
                p.Codigo AS CodigoProducto, p.Nombre AS NombreProducto,
                df.Cantidad, df.PrecioUnitario, df.Descuento, df.Subtotal, df.Impuesto
            FROM DetalleFactura df
            JOIN Productos p ON df.ProductoID = p.ProductoID
            WHERE df.FacturaID = ?
            ORDER BY df.DetalleID
            """
            cursor.execute(sql_items, (factura_id,))
            items = cursor.fetchall()
            
            return factura, items
            
        except pyodbc.Error as ex:
            print(f"Error de BD al buscar factura: {ex}")
            raise ex