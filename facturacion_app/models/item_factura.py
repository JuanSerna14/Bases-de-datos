import decimal
from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemFactura:
    producto_id: Optional[int] = None
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    cantidad: int = 1
    precio_unitario: Optional[decimal.Decimal] = None
    descuento_tasa: decimal.Decimal = decimal.Decimal(0)
    tasa_impuesto: Optional[decimal.Decimal] = None

    def __post_init__(self):
        """Conversión y validación de tipos"""
        self.cantidad = int(self.cantidad)
        self.precio_unitario = self._convert_to_decimal(self.precio_unitario)
        self.descuento_tasa = self._convert_to_decimal(self.descuento_tasa) or decimal.Decimal(0)
        self.tasa_impuesto = self._convert_to_decimal(self.tasa_impuesto)

    @staticmethod
    def _convert_to_decimal(value) -> Optional[decimal.Decimal]:
        """Convierte valores a Decimal de forma segura"""
        if value is None:
            return None
        try:
            return decimal.Decimal(str(value))
        except (decimal.InvalidOperation, TypeError):
            return None

    def calcular_subtotal(self) -> decimal.Decimal:
        """Calcula el subtotal neto (con descuento aplicado)"""
        if None in (self.precio_unitario, self.cantidad):
            return decimal.Decimal(0)
            
        subtotal_bruto = decimal.Decimal(self.cantidad) * self.precio_unitario
        descuento = subtotal_bruto * self.descuento_tasa
        return subtotal_bruto - descuento
        
    def calcular_impuesto(self) -> decimal.Decimal:
        """Calcula el valor del impuesto"""
        subtotal_neto = self.calcular_subtotal()
        if not self.tasa_impuesto:
            return decimal.Decimal(0)
        return subtotal_neto * self.tasa_impuesto
        
    def to_dict(self) -> dict:
        """Serializa el objeto a diccionario"""
        return {
            'producto_id': self.producto_id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio_unitario': str(self.precio_unitario),
            'descuento_tasa': str(self.descuento_tasa),
            'tasa_impuesto': str(self.tasa_impuesto),
            'subtotal': str(self.calcular_subtotal()),
            'impuesto': str(self.calcular_impuesto()),
            'total': str(self.calcular_subtotal() + self.calcular_impuesto())
        }

    def validar(self) -> bool:
        """Valida que el item tenga los datos mínimos requeridos"""
        return all([
            self.producto_id is not None,
            self.cantidad > 0,
            self.precio_unitario is not None,
            self.precio_unitario > decimal.Decimal(0)
        ])