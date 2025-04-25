import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class ProductoView:
    def __init__(self, notebook, controller):
        self.controller = controller
        self.frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.frame, text="Productos")
        self.crear_interfaz()
        
    def crear_interfaz(self):
        form_frame = ttk.LabelFrame(self.frame, text="Registrar Nuevo Producto", padding="10")
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        campos = [
            ("Código:", "codigo"),
            ("Nombre:", "nombre"),
            ("Descripción:", "descripcion"),
            ("Precio Unitario:", "precio"),
            ("Unidad de Medida:", "unidad"),
            ("Tasa de Impuesto (%):", "impuesto")
        ]

        self.entries = {}
        for i, (texto, attr) in enumerate(campos):
            ttk.Label(form_frame, text=texto).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            self.entries[attr] = entry

        btn_registrar = ttk.Button(form_frame, text="Registrar Producto", command=self.registrar_producto)
        btn_registrar.grid(row=len(campos), column=1, pady=10, padx=5, sticky='e')

        table_frame = ttk.LabelFrame(self.frame, text="Productos Registrados", padding="10")
        table_frame.grid(row=1, column=0, padx=5, pady=10, sticky='nsew')
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.crear_tabla_productos(table_frame)
        
    def crear_tabla_productos(self, frame):
        columnas_defs = {
            'ID': {'text': 'ID', 'width': 50, 'anchor': 'center'},
            'Codigo': {'text': 'Código', 'width': 100},
            'Nombre': {'text': 'Nombre', 'width': 250},
            'Precio': {'text': 'Precio', 'width': 100, 'anchor': 'e'},
            'Impuesto': {'text': 'Impuesto (%)', 'width': 100, 'anchor': 'e'}
        }
        column_ids = list(columnas_defs.keys())

        self.tree = ttk.Treeview(frame, columns=column_ids, show='headings')
        for col_id in column_ids:
            details = columnas_defs[col_id]
            self.tree.heading(col_id, text=details['text'], anchor=details.get('anchor', 'w'))
            self.tree.column(col_id, width=details['width'], stretch=tk.YES if col_id == 'Nombre' else tk.NO, 
                            anchor=details.get('anchor', 'w'))

        self.tree.grid(row=0, column=0, sticky='nsew')
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def registrar_producto(self):
        datos = {attr: entry.get() for attr, entry in self.entries.items()}
        try:
            if self.controller.registrar_producto(datos):
                messagebox.showinfo("Registro Exitoso", "Producto registrado correctamente.")
                self.controller.cargar_productos(self.tree)
                self.limpiar_campos()
        except pyodbc.IntegrityError as ex:
            messagebox.showerror("Error de Integridad", 
                f"No se pudo registrar el producto.\nPosiblemente el código ya existe.\nError: {ex}")
        except pyodbc.Error as ex:
            messagebox.showerror("Error de Base de Datos", f"No se pudo registrar el producto.\nError: {ex}")
            
    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')