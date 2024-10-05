from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__  = "usuarios"
    id             = db.Column(db.Integer,     primary_key=True)
    nombre         = db.Column(db.String(45),  nullable=False)
    apellido       = db.Column(db.String(45),  nullable=False)
    correo         = db.Column(db.String(45),  nullable=False, unique=True)
    clave          = db.Column(db.String(255), nullable=False)
    miembro        = db.Column(db.Boolean,     nullable=False, default=False)
    created_at     = db.Column(db.DateTime(),  default=datetime.now)

    proveedor      = db.relationship('Proveedor', back_populates='usuario', uselist=False)

    def establecer_clave(self, clave):
        self.clave = generate_password_hash(clave)

    def chequeo_clave(self, clave):
        return check_password_hash(self.clave, clave)

    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Usuario)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)
        print("Items de consulta:",all_items_list)
        return(all_items_list)

    @staticmethod
    def obtener_por_correo(correo):
        usuario = Usuario.query.filter_by(correo=correo).first()
        print(f"Consultando por el usuario {usuario} en db")
        return(usuario)

    @staticmethod
    def obtener_por_id(id):
        print(f"Consultando por el usuario con id {id} en db")
        return Usuario.query.get(id)

class Proveedor(db.Model):
    __tablename__  = "proveedores"
    id             = db.Column(db.Integer,     primary_key=True)
    id_usuario     = db.Column(db.Integer,     nullable=False)
    nombre         = db.Column(db.String(50),  nullable=False)
    apellido       = db.Column(db.String(50),  nullable=False)
    edad           = db.Column(db.Integer,     nullable=True)
    correo         = db.Column(db.String(50),  nullable=False)
    telefono       = db.Column(db.String(30),  nullable=False)
    tipo           = db.Column(db.String(30),  nullable=False)
    
    usuario_id     = db.Column(db.ForeignKey('usuarios.id'))
    usuario        = db.relationship('Usuario', back_populates='proveedor')
    
    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Proveedor)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)
        print("Items de consulta:",all_items_list)
        return(all_items_list)
    
    @staticmethod
    def obtener_por_correo(correo):
        usuario = Proveedor.query.filter_by(correo=correo).first()
        print(f"Consultando por el usuario {usuario} en db")
        return(usuario)

    @staticmethod
    def obtener_miembro_por_id(id):
        print(f"Consultando por el usuario con id {id} en db")
        return Proveedor.query.get(id)