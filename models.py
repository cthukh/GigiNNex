from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__  = "usuarios"
    id             = db.Column(db.Integer,     primary_key=True)
    nombre         = db.Column(db.String(45),  nullable=False)
    correo         = db.Column(db.String(45),  nullable=False, unique=True)
    clave          = db.Column(db.String(255), nullable=False)
    proveedor      = db.Column(db.Boolean,     nullable=False, default=False)
    created_at     = db.Column(db.DateTime(),  default = datetime.now())

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

# class Categoria(db.Model):
#     __tablename__   = "Categorias"
#     id              = db.Column(db.Interger, primary_key = True)
#     tipo            = db.Column(db.String, db.ForeignKey('id'))
#     tipo            = db.relationship('', back_populates='wishlist')