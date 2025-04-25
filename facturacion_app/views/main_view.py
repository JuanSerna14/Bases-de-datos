from tkinter import messagebox, ttk
from facturacion_app.views.cliente_view import ClienteView
from facturacion_app.views.producto_view import ProductoView
from facturacion_app.views.factura_view import FacturaView
from facturacion_app.views.busqueda_view import BusquedaView
from facturacion_app.controllers.base_controller import BaseController

class SistemaFacturacion(BaseController):
    def __init__(self, root):
        super().__init__()  # Esto ya llama a _conectar_base_datos() en BaseController
        self.root = root
        self.root.title("Sistema de Facturación")
        self.root.geometry("1000x700")
        self.inicializar_interfaz()
        # Elimina la línea: self.conectar_base_datos()
        
    def inicializar_interfaz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Importaciones dentro del método para evitar circulares
        from facturacion_app.controllers.cliente_controller import ClienteController
        from facturacion_app.controllers.producto_controller import ProductoController
        from facturacion_app.controllers.factura_controller import FacturaController
        from facturacion_app.controllers.busqueda_controller import BusquedaController
        
        # Verifica la conexión antes de crear las vistas
        if not self.verificar_conexion():
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return
            
        # Crear vistas con sus controladores
        self.cliente_view = ClienteView(self.notebook, ClienteController())
        self.producto_view = ProductoView(self.notebook, ProductoController())
        self.factura_view = FacturaView(self.notebook, FacturaController())
        self.busqueda_view = BusquedaView(self.notebook, BusquedaController())
        
        self.configurar_estilos()
        
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Titulo.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Subtitulo.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        style.configure('.', font=('Arial', 10))
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))