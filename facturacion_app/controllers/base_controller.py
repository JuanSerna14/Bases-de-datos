import pyodbc
from tkinter import messagebox
import logging
from typing import Optional, List, Tuple, Any
from dataclasses import dataclass

@dataclass
class DBConfig:
    server: str = 'DESKTOP-92PTT9C'
    database: str = 'SistemaFacturacion'
    driver: str = 'SQL Server'
    trusted_connection: str = 'yes'
    timeout: int = 30

class BaseController:
    def __init__(self, config: Optional[DBConfig] = None):
        self.config = config if config else DBConfig()
        self.conexion: Optional[pyodbc.Connection] = None
        self.db_connection_failed: bool = False  # Atributo añadido
        self._establecer_logger()
        self._conectar_base_datos()

    def _establecer_logger(self):
        """Configuración mejorada del logger"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Configurar handlers
        file_handler = logging.FileHandler('facturacion_db.log')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _conectar_base_datos(self) -> bool:
        try:
            conn_str = (
                f"DRIVER={{{self.config.driver}}};"
                f"SERVER={self.config.server};"
                f"DATABASE={self.config.database};"
                f"Trusted_Connection={self.config.trusted_connection};"
                f"Connection Timeout={self.config.timeout};"
            )
            self.conexion = pyodbc.connect(conn_str)
            self.conexion.autocommit = False
            self.db_connection_failed = False
            self.logger.info(f"Conexión exitosa a {self.config.database}")
            return True
        except pyodbc.Error as e:
            self.db_connection_failed = True
            self.logger.error(f"Error de conexión: {str(e)}")
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{str(e)}")
            return False

    def verificar_conexion(self) -> bool:
        """Versión mejorada con manejo de errores"""
        if self.db_connection_failed or not self.conexion:
            return False
            
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except pyodbc.Error as e:
            self.db_connection_failed = True
            self.logger.error(f"Error al verificar conexión: {str(e)}")
            return False

    # ... (resto de métodos se mantienen igual)
    def ejecutar_consulta(
        self, 
        query: str, 
        params: Optional[Tuple] = None, 
        commit: bool = False
    ) -> Optional[List[Tuple]]:
        """
        Ejecuta una consulta de forma segura
        
        Args:
            query: Consulta SQL con parámetros ?
            params: Tupla de parámetros
            commit: Si es True, guarda los cambios
            
        Returns:
            Lista de tuplas con resultados o None si hay error
        """
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params or ())
                
                if commit:
                    self.conexion.commit()
                    
                if cursor.description:  # Si es SELECT
                    return cursor.fetchall()
                return []
                
        except pyodbc.Error as e:
            self.logger.error(f"Error en consulta: {str(e)}")
            self.conexion.rollback()
            messagebox.showerror(
                "Error en Base de Datos", 
                f"No se pudo ejecutar la consulta:\n{str(e)}"
            )
            return None

    def cerrar_conexion(self):
        """Cierra la conexión de forma segura"""
        if self.conexion:
            try:
                self.conexion.close()
                self.logger.info("Conexión cerrada correctamente")
            except pyodbc.Error as e:
                self.logger.error(f"Error al cerrar conexión: {str(e)}")
            finally:
                self.conexion = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar_conexion()

    def __del__(self):
        self.cerrar_conexion()