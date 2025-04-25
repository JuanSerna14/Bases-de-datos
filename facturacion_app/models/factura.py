import decimal
from datetime import datetime
from models.cliente import Cliente
from models.item_factura import ItemFactura

class Factura:
    def __init__(self, factura_id=None, numero_factura=None, fecha_emision=None,
                 cliente=None, items=None, total_bruto=None, total_descuento=None,
                 total_impuestos=None, total_neto=None):
        self.factura_id = factura_id
        self.numero_factura = numero_factura
        self.fecha_emision = fecha_emision if isinstance(fecha_emision, datetime) else datetime.now()
        self.cliente = cliente if isinstance(cliente, Cliente) else None
        self.items = items or []
        self.total_bruto = decimal.Decimal(total_bruto) if total_bruto else decimal.Decimal(0)
        self.total_descuento = decimal.Decimal(total_descuento) if total_descuento else decimal.Decimal(0)
        self.total_impuestos = decimal.Decimal(total_impuestos) if total_impuestos else decimal.Decimal(0)
        self.total_neto = decimal.Decimal(total_neto) if total_neto else decimal.Decimal(0)

    def agregar_item(self, item):
        if isinstance(item, ItemFactura):
            self.items.append(item)
            self.calcular_totales()
            return True
        return False

    def calcular_totales(self):
        self.total_bruto = sum(item.calcular_subtotal() / (1 - item.descuento_tasa) for item in self.items)
        self.total_descuento = sum((item.calcular_subtotal() / (1 - item.descuento_tasa)) * item.descuento_tasa for item in self.items)
        subtotal_neto = sum(item.calcular_subtotal() for item in self.items)
        self.total_impuestos = sum(item.calcular_impuesto() for item in self.items)
        self.total_neto = subtotal_neto + self.total_impuestos

    def to_dict(self):
        return {
            'factura_id': self.factura_id,
            'numero_factura': self.numero_factura,
            'fecha_emision': self.fecha_emision.isoformat(),
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'items': [item.to_dict() for item in self.items],
            'total_bruto': str(self.total_bruto),
            'total_descuento': str(self.total_descuento),
            'total_impuestos': str(self.total_impuestos),
            'total_neto': str(self.total_neto)
        }