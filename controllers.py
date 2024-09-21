from models import Usuario, db

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

    # @staticmethod
    # def editar_usuario(nombre,correo,clave):
    #     pass
    #     # Usuario.obtener_por_correo(correo=correo)
    #     # if not usuario:
        
    # #def obtener_usuarios()
    # #def borrar_usuario()