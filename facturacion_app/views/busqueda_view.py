import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext

class BusquedaView:
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.frame, text="Buscar Facturas")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame de búsqueda
        frame_busqueda = ttk.LabelFrame(self.frame, text="Buscar Factura por ID", padding="10")
        frame_busqueda.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        ttk.Label(frame_busqueda, text="ID Factura:").grid(row=0, column=0, padx=5, pady=5)
        self.id_factura_entry = ttk.Entry(frame_busqueda, width=20)
        self.id_factura_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_buscar = ttk.Button(frame_busqueda, text="Buscar Factura", command=self.buscar_factura)
        btn_buscar.grid(row=0, column=2, padx=10, pady=5)

        # Área de información
        frame_info = ttk.LabelFrame(self.frame, text="Información de la Factura", padding="10")
        frame_info.grid(row=1, column=0, padx=5, pady=10, sticky='nsew')
        frame_info.rowconfigure(0, weight=1)
        frame_info.columnconfigure(0, weight=1)

        self.info_text = scrolledtext.ScrolledText(
            frame_info, width=100, height=25, wrap=tk.WORD,
            font=('Courier New', 9)
        )
        self.info_text.grid(row=0, column=0, sticky='nsew')
        self.info_text.config(state='disabled')

        # Configurar tags de estilo
        self.info_text.tag_config('titulo', font=('Courier New', 12, 'bold'), justify='center')
        self.info_text.tag_config('subtitulo', font=('Courier New', 10, 'bold'), underline=True)
        self.info_text.tag_config('cabecera', font=('Courier New', 9, 'bold'))
        self.info_text.tag_config('totales', font=('Courier New', 9, 'bold'), justify='right')
        self.info_text.tag_config('error', foreground='red')

    def buscar_factura(self):
        factura_id = self.id_factura_entry.get()
        try:
            factura, items = self.controller.buscar_factura(factura_id)
            
            self.info_text.config(state='normal')
            self.info_text.delete(1.0, 'end')
            
            if not factura:
                self.info_text.insert('end', f"No se encontró factura con ID {factura_id}\n", 'error')
                self.info_text.config(state='disabled')
                messagebox.showwarning("No Encontrada", f"No se encontró factura con ID {factura_id}")
                return
                
            self.mostrar_factura(factura, items)
            self.info_text.config(state='disabled')
            
        except ValueError as e:
            messagebox.showwarning("Entrada Inválida", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar factura:\n{str(e)}")

    def mostrar_factura(self, factura, items):
        # Encabezado de la empresa
        self.info_text.insert('end', "            *** MI EMPRESA S.A.S. ***\n", 'titulo')
        self.info_text.insert('end', "                NIT: 900.123.456-7\n")
        self.info_text.insert('end', "            Dirección: Calle Falsa 123, Ciudad\n")
        self.info_text.insert('end', "               Teléfono: (4) 555 6789\n")
        self.info_text.insert('end', "------------------------------------------------------------------------------------------\n")

        # Información de la factura
        self.info_text.insert('end', f"FACTURA DE VENTA No: {factura.NumeroFactura}\n", 'subtitulo')
        self.info_text.insert('end', f"Fecha y Hora: {factura.FechaEmision.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Datos del cliente
        self.info_text.insert('end', "DATOS DEL CLIENTE:\n", 'subtitulo')
        self.info_text.insert('end', f" Nombre:         {factura.NombreCliente}\n")
        self.info_text.insert('end', f" Identificación: {factura.IdCliente}\n")
        self.info_text.insert('end', f" Dirección:      {factura.Direccion or 'N/A'}\n")
        self.info_text.insert('end', f" Teléfono:       {factura.Telefono or 'N/A'}\n")
        self.info_text.insert('end', f" Correo E.:      {factura.CorreoElectronico or 'N/A'}\n")
        self.info_text.insert('end', "------------------------------------------------------------------------------------------\n")

        # Detalles de items
        self.info_text.insert('end', "DETALLE DE PRODUCTOS/SERVICIOS:\n", 'subtitulo')
        self.info_text.insert('end', f"{'Código':<10} {'Producto':<30} {'Cant.':>6} {'Vr. Unit.':>12} {'Desc.':>8} {'Subtotal':>14}\n", 'cabecera')
        self.info_text.insert('end', "="*90 + "\n", 'cabecera')

        if not items:
            self.info_text.insert('end', "*** No hay items registrados para esta factura ***\n")
        else:
            for item in items:
                self.info_text.insert('end',
                    f"{item.CodigoProducto:<10} {item.NombreProducto[:30]:<30} {item.Cantidad:>6} "
                    f"{item.PrecioUnitario:>12,.2f} {item.Descuento*100:>7.1f}% {item.Subtotal:>14,.2f}\n"
                )
                
        self.info_text.insert('end', "------------------------------------------------------------------------------------------\n")

        # Totales
        self.info_text.insert('end', "TOTALES:\n", 'subtitulo')
        self.info_text.insert('end', f"{'Subtotal Bruto:':<73}{factura.TotalBruto:>16,.2f}\n", 'totales')
        self.info_text.insert('end', f"{'Total Descuento:':<73}{factura.TotalDescuento:>16,.2f}\n", 'totales')
        self.info_text.insert('end', f"{'Subtotal Neto (Antes Imp):':<73}{(factura.TotalBruto - factura.TotalDescuento):>16,.2f}\n", 'totales')
        self.info_text.insert('end', f"{'Total Impuestos:':<73}{factura.TotalImpuestos:>16,.2f}\n", 'totales')
        self.info_text.insert('end', f"{'TOTAL A PAGAR:':<73}{factura.TotalNeto:>16,.2f}\n", 'totales')
        self.info_text.insert('end', "="*90 + "\n")

        # Pie de página
        self.info_text.insert('end', "\nGracias por su compra.\n")
        self.info_text.insert('end', "Resolución DIAN No. XXXX de Fecha YYYY/MM/DD.\n")
        self.info_text.insert('end', "Régimen Común / Responsable de IVA.\n")