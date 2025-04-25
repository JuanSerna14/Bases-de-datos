import decimal

class Producto:
    def __init__(self, producto_id=None, codigo=None, nombre=None, descripcion=None,
                 precio_unitario=None, unidad_medida=None, tasa_impuesto=None):
        self.producto_id = producto_id
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_unitario = decimal.Decimal(precio_unitario) if precio_unitario else None
        self.unidad_medida = unidad_medida
        self.tasa_impuesto = decimal.Decimal(tasa_impuesto) if tasa_impuesto else None
        
    def to_dict(self):
        return {
            'producto_id': self.producto_id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_unitario': str(self.precio_unitario),
            'unidad_medida': self.unidad_medida,
            'tasa_impuesto': str(self.tasa_impuesto)
        }