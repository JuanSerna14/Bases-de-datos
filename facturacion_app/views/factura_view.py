import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext

class FacturaView:
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.frame, text="Nueva Factura")
        self.frame.columnconfigure(0, weight=1)
        self.crear_interfaz()

    def crear_interfaz(self):
        self.crear_seccion_cliente()
        self.crear_seccion_items()
        self.crear_seccion_totales()
        self.crear_botones_accion()

    def crear_seccion_cliente(self):
        frame_cliente = ttk.LabelFrame(self.frame, text="1. Datos del Cliente", padding="10")
        frame_cliente.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        ttk.Label(frame_cliente, text="Identificación Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.identificacion_entry = ttk.Entry(frame_cliente, width=25)
        self.identificacion_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        btn_buscar = ttk.Button(frame_cliente, text="Buscar Cliente", command=self.buscar_cliente)
        btn_buscar.grid(row=0, column=2, padx=5, pady=5)

        self.nombre_cliente_label = ttk.Label(frame_cliente, text="Cliente: (Ninguno seleccionado)", font=('Arial', 10, 'italic'))
        self.nombre_cliente_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')

    def crear_seccion_items(self):
        frame_items = ttk.LabelFrame(self.frame, text="2. Items de Factura", padding="10")
        frame_items.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        frame_items.columnconfigure(1, weight=1)
        frame_items.rowconfigure(1, weight=1)

        # Formulario para agregar items
        add_item_frame = ttk.Frame(frame_items)
        add_item_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky='ew')

        ttk.Label(add_item_frame, text="Código Producto:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_entry = ttk.Entry(add_item_frame, width=15)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_item_frame, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5)
        self.cantidad_entry = ttk.Entry(add_item_frame, width=8)
        self.cantidad_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(add_item_frame, text="Desc (%):").grid(row=0, column=4, padx=5, pady=5)
        self.descuento_entry = ttk.Entry(add_item_frame, width=8)
        self.descuento_entry.grid(row=0, column=5, padx=5, pady=5)
        self.descuento_entry.insert(0, "0")

        btn_agregar = ttk.Button(add_item_frame, text="Agregar Item", command=self.agregar_item)
        btn_agregar.grid(row=0, column=6, padx=10, pady=5)

        # Tabla de items
        columns = ('Codigo', 'Nombre', 'Cantidad', 'PrecioUnit', 'Descuento', 'Subtotal')
        self.tree_items = ttk.Treeview(frame_items, columns=columns, show='headings')

        col_defs = {
            'Codigo': {'text': 'Código', 'width': 80},
            'Nombre': {'text': 'Nombre Producto', 'width': 250},
            'Cantidad': {'text': 'Cant.', 'width': 60, 'anchor': 'center'},
            'PrecioUnit': {'text': 'Precio Unit.', 'width': 100, 'anchor': 'e'},
            'Descuento': {'text': 'Desc. (%)', 'width': 80, 'anchor': 'center'},
            'Subtotal': {'text': 'Subtotal', 'width': 120, 'anchor': 'e'}
        }

        for col in columns:
            defs = col_defs[col]
            self.tree_items.heading(col, text=defs['text'], anchor=defs.get('anchor', 'w'))
            self.tree_items.column(col, width=defs['width'], stretch=(col=='Nombre'), anchor=defs.get('anchor', 'w'))

        self.tree_items.grid(row=1, column=0, padx=(5,0), pady=5, sticky='nsew')

        scrollbar = ttk.Scrollbar(frame_items, orient="vertical", command=self.tree_items.yview)
        scrollbar.grid(row=1, column=1, sticky='ns', pady=5, padx=(0,5))
        self.tree_items.configure(yscrollcommand=scrollbar.set)

    def crear_seccion_totales(self):
        frame_totales = ttk.LabelFrame(self.frame, text="3. Totales", padding="10")
        frame_totales.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        frame_totales.columnconfigure(1, weight=1)
        frame_totales.columnconfigure(3, weight=1)

        self.labels_totales = {}
        totales_info = [
            ("Subtotal Bruto:", "total_bruto"),
            ("Total Descuento:", "total_descuento"),
            ("Subtotal Neto:", "subtotal_neto"),
            ("Total Impuestos:", "total_impuestos"),
            ("TOTAL NETO A PAGAR:", "total_neto_pagar")
        ]

        for i, (texto, attr) in enumerate(totales_info):
            row = i
            label_texto = ttk.Label(frame_totales, text=texto, 
                                  font=('Arial', 10, 'bold' if 'PAGAR' in texto else 'normal'))
            label_texto.grid(row=row, column=0 if i % 2 == 0 else 2, padx=(10,5), pady=3, sticky='w')

            label_valor = ttk.Label(frame_totales, text="0.00", 
                                   font=('Arial', 10, 'bold' if 'PAGAR' in texto else 'normal'), 
                                   anchor='e')
            label_valor.grid(row=row, column=1 if i % 2 == 0 else 3, padx=(0,10), pady=3, sticky='ew')
            self.labels_totales[attr] = label_valor

    def crear_botones_accion(self):
        action_frame = ttk.Frame(self.frame, padding="5")
        action_frame.grid(row=3, column=0, pady=10, sticky='ew')
        action_frame.columnconfigure(0, weight=1)

        btn_limpiar = ttk.Button(action_frame, text="Limpiar Factura", command=self.limpiar_factura)
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        btn_crear = ttk.Button(action_frame, text="Crear Factura", command=self.crear_factura, style='Accent.TButton')
        btn_crear.pack(side=tk.RIGHT, padx=5)

    def buscar_cliente(self):
        identificacion = self.identificacion_entry.get()
        cliente = self.controller.buscar_cliente(identificacion)
        
        if cliente:
            self.controller.cliente_id_factura = cliente.ClienteID
            self.nombre_cliente_label.config(text=f"Cliente: {cliente.Nombre} (ID: {cliente.ClienteID})")
        elif cliente is None:  # None significa que hubo un error
            pass
        else:
            self.nombre_cliente_label.config(text="Cliente: (No encontrado)")
            messagebox.showwarning("No Encontrado", f"No se encontró cliente con identificación '{identificacion}'")

    def agregar_item(self):
        codigo = self.codigo_entry.get()
        cantidad = self.cantidad_entry.get()
        descuento = self.descuento_entry.get()
        
        item = self.controller.agregar_item(codigo, cantidad, descuento)
        if item:
            self.controller.items_factura.append(item)
            self.tree_items.insert('', 'end', values=(
                item.codigo,
                item.nombre,
                item.cantidad,
                f"{item.precio_unitario:.2f}",
                f"{item.descuento_tasa * 100:.1f}%",
                f"{item.calcular_subtotal():.2f}"
            ))
            self.actualizar_totales()
            self.limpiar_campos_item()

    def actualizar_totales(self):
        total_bruto = sum(item.calcular_subtotal() / (1 - item.descuento_tasa) for item in self.controller.items_factura)
        total_descuento = sum((item.calcular_subtotal() / (1 - item.descuento_tasa)) * item.descuento_tasa for item in self.controller.items_factura)
        subtotal_neto = sum(item.calcular_subtotal() for item in self.controller.items_factura)
        total_impuestos = sum(item.calcular_impuesto() for item in self.controller.items_factura)
        total_neto = subtotal_neto + total_impuestos

        self.labels_totales['total_bruto'].config(text=f"{total_bruto:.2f}")
        self.labels_totales['total_descuento'].config(text=f"{total_descuento:.2f}")
        self.labels_totales['subtotal_neto'].config(text=f"{subtotal_neto:.2f}")
        self.labels_totales['total_impuestos'].config(text=f"{total_impuestos:.2f}")
        self.labels_totales['total_neto_pagar'].config(text=f"{total_neto:.2f}")

    def crear_factura(self):
        if not self.controller.cliente_id_factura:
            messagebox.showwarning("Sin Cliente", "Seleccione un cliente antes de crear la factura.")
            return

        if not self.controller.items_factura:
            messagebox.showwarning("Sin Items", "Agregue al menos un producto a la factura.")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de crear esta factura?"):
            return

        try:
            numero_factura = self.controller.crear_factura()
            messagebox.showinfo("Éxito", f"Factura creada exitosamente.\nNúmero: {numero_factura}")
            self.limpiar_factura()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la factura:\n{str(e)}")

    def limpiar_factura(self):
        self.controller.limpiar_factura()
        self.identificacion_entry.delete(0, 'end')
        self.nombre_cliente_label.config(text="Cliente: (Ninguno seleccionado)")
        self.limpiar_campos_item()
        self.tree_items.delete(*self.tree_items.get_children())
        for label in self.labels_totales.values():
            label.config(text="0.00")
        self.identificacion_entry.focus()

    def limpiar_campos_item(self):
        self.codigo_entry.delete(0, 'end')
        self.cantidad_entry.delete(0, 'end')
        self.descuento_entry.delete(0, 'end')
        self.descuento_entry.insert(0, "0")
        self.codigo_entry.focus()