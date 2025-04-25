import sys
import tkinter as tk
from tkinter import messagebox
import traceback
from pathlib import Path

# Configuración esencial del path (esto soluciona los problemas de imports)
sys.path.insert(0, str(Path(__file__).parent))

try:
    from facturacion_app.views.main_view import SistemaFacturacion
except ImportError as e:
    messagebox.showerror("Error de Configuración", 
                       f"Error al importar módulos:\n{str(e)}\n\n"
                       "Verifique que:\n"
                       "1. La estructura de carpetas es correcta\n"
                       "2. Todos los __init__.py existen\n"
                       "3. Los imports son consistentes")
    sys.exit(1)

def on_closing():
    """Maneja el evento de cierre de la ventana principal"""
    if 'app' in globals() and hasattr(app, 'cerrar_db'):
        try:
            app.cerrar_db()
        except Exception as e:
            messagebox.showerror("Error al cerrar", 
                               f"Error al cerrar recursos:\n{str(e)}")
    root.destroy()

if __name__ == "__main__":
    root = None
    try:
        root = tk.Tk()
        app = SistemaFacturacion(root)
        
        # Configuración de la ventana principal
        root.title("Sistema de Facturación - v1.0")
        root.geometry("1024x768")
        root.minsize(800, 600)
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Estilo visual consistente
        root.tk_setPalette(background='#f0f0f0', foreground='black',
                          activeBackground='#d9d9d9', activeForeground='black')
        
        root.mainloop()
        
    except ImportError as e:
        traceback.print_exc()
        messagebox.showerror("Error de Importación", 
                           f"Falta módulo requerido:\n{str(e)}\n\n"
                           "Ejecute: pip install -r requirements.txt")
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error Inesperado", 
                           f"Error crítico:\n{str(e)}\n\n"
                           "Revise el log de errores")
    finally:
        print("Aplicación finalizada")
        if root:
            try:
                root.destroy()
            except tk.TclError:
                pass