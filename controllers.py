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
    def editar_usuario(id, nombre, correo):
        # verifica el usuario por la id en db.
        usuario = Usuario.query.get(id)
        if not usuario:
            resultado = {
                'error' : True,
                'mensaje' : f"El usuario {id} no existe en la db"
            }
            return resultado

        # Verifica si el correo existe en la db
        if Usuario.query.filter_by(correo=correo).first() and correo != usuario.correo:
            resultado = {
                'error' : True,
                'mensaje' : f"El correo {correo} ya esta en uso"
            }
            return resultado

        usuario.nombre = nombre
        usuario.correo = correo
        db.session.commit()
        return {'usuario' : usuario}  # Retorna el usuario dentro de un diccionario

    @staticmethod
    def borrar_usuario(id):
        usuario = Usuario.query.get(id)
        if not usuario:
            resultado = {
                'error' : True,
                'mensaje' : f"El usuario {id} no existe en la db"
            }
            return resultado
        
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return {'mensaje': "usuario eliminado"}
    # #def obtener_usuarios()
    # #def borrar_usuario()
    