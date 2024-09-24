from models import Usuario, db
from werkzeug.security import generate_password_hash, check_password_hash

class ControladorUsuarios:
    @staticmethod
    def crear_usuario(nombre,correo,clave):
        usuario = Usuario()
        usuario.nombre = nombre
        usuario.correo = correo
        usuario.establecer_clave(clave)

        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def editar_usuario(id, nombre, correo, clave):
        usuario = Usuario.query.get(id)
        if not usuario:
            return None
        # Verifica si el correo es único
        if Usuario.query.filter_by(correo=correo).first() and correo != usuario.correo:
            return {'error': 'El correo ya está en uso.'}
        usuario.nombre = nombre
        usuario.correo = correo
        # Hash de la nueva clave si se proporciona
        if clave:
            usuario.clave = generate_password_hash(clave)
        db.session.commit()
        return usuario

    # #def obtener_usuarios()
    # #def borrar_usuario()