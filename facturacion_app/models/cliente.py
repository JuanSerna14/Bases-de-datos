class Cliente:
    def __init__(self, cliente_id=None, nombre=None, identificacion=None, 
                 direccion=None, correo=None, telefono=None):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.identificacion = identificacion
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono
        
    def to_dict(self):
        return {
            'cliente_id': self.cliente_id,
            'nombre': self.nombre,
            'identificacion': self.identificacion,
            'direccion': self.direccion,
            'correo': self.correo,
            'telefono': self.telefono
        }