from flask import Flask, render_template, flash, redirect, request
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

# Se crea una instancia de Flask y se configura con una clave secreta y la URI de la base de datos.
app = Flask(__name__)
app.config["SECRET_KEY"] = 'Ultra_Super_Secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/deginnex'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# Se inicializa el gestor de sesiones y se define la vista de inicio de sesión.
login_manager = LoginManager(app)
login_manager.login_view = "auth"

# importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso, FormularioValidar
from models import Usuario, Proveedor
from controllers import ControladorUsuarios

# Inicialización de versiones de la bases de datos
Migrate(app,db)

# Inicialización de login_manager y configuración de
# función que carga un usuario a partir de su ID, necesaria para la gestión de sesiones.
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))

# Evita que las respuestas sean almacenadas en caché.
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
#************************************************** Manejo registro/login **************************************************

# Verifica si el usuario ya está autenticado. Si lo está, redirige a la página de inicio.
# Si no, muestra los formularios de registro y acceso.
@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if current_user.is_authenticated:
        return redirect("/inicio")

    if form_registro == None:
        form_registro = FormularioRegistro()

    if form_acceso == None:
        form_acceso = FormularioAcceso()
    return render_template("auth.html", form_registro=form_registro, form_acceso=form_acceso)

# Maneja la creación de nuevos usuarios, recibe un formulario y guarda en la base de datos.
# Valida los datos del formulario y proporciona mensajes de error si es necesario.
@app.route("/register", methods=["POST"])
def register():
    form   = FormularioRegistro()
    error  = None

    #################### Validación del formulario. ####################
    # Comprobar si el correo ya está registrado; Si no, se crea el usuario.
    if form.validate_on_submit():
        print("form valido")
        flash("Form valido")
        nombre   = form.nombre.data
        apellido = form.apellido.data
        correo   = form.correo.data
        clave    = form.clave.data

        # Consultamos si existe en la db.
        usuario = Usuario().obtener_por_correo(correo)
        if usuario is not None:
            error = f"El correo {correo} ya se encuentra registrado"
            print(error)
            flash(error)
            return(redirect("/"))
        else:
            flash(f'Registro solicitado para el usuario { nombre }')
            # Utilización de un controlador entre Vista y Modelo.
            ControladorUsuarios().crear_usuario(nombre, apellido, correo, clave)
            # Generamos una instancia de datos.
            return redirect("/")
    else:
        print("form invalido")
        flash("Form invalido")
        return auth(form_registro=form)

#################### Validar el acceso del usuario. ####################
# Si es exitoso, iniciar sesión.
@app.route("/login", methods=["POST"])
def login():
    # Recibimos los datos del login en frontend.
    form_acceso = FormularioAcceso()
    if form_acceso.validate_on_submit():
        flash(f"Acceso solicitado para el usuario { form_acceso.correo.data }")
        # Consultamos por el correo en la db
        usuario = Usuario().obtener_por_correo(form_acceso.correo.data)
        # Si el usuario no es nada (entonces existe en la db)
        if usuario is not None:
            if usuario.chequeo_clave(form_acceso.clave.data):
                login_user(usuario)
                return(redirect("/inicio"))
            else:
                flash(f"Clave incorrecta")
                print(f"Clave incorrecta")
                return(redirect("/"))
        else:
            flash(f"El usuario no esta registrado")
            print(f"El usuario no esta registrado")
            return(redirect("/"))

#************************************************** Rutas principales. **************************************************

#################### Página Principal ####################
@app.route('/inicio')
def index():
    return render_template('index.html')

#################### Selección de categorias ####################
@app.route('/section/<string:categoria>')
def selecionar_categorias(categoria):
    # Renderiza diferentes plantillas según la categoría
    if   categoria == 'videos':                         # Categoría video.
        return render_template ('cat_video.html')
    elif categoria == 'diseño-grafico':                 # Categoría Diseño Grafico.
        return render_template ('cat_imagenes.html')
    elif categoria == 'audio':                          # Categoría audio.  #? Posible retiro.
        return render_template ('cat_audio.html')
    elif categoria == 'sitios-web':                     # Categoría sitios web.
        return render_template ('cat_web.html')
    else:
        return render_template('404.html')


# perfi/view

#################### Ver perfil propio ####################
@app.route("/perfil/me")
@login_required
def perfil():
    # Muestra solo la sesión activa.
    return render_template("perfil_v2.html", usuario=current_user)

#################### editar perfil propio ####################

@app.route('/perfil/me/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'GET':
        return render_template('editar_usuario.html', usuario=current_user)

    if request.method == 'POST':
        error = False
        idq       = current_user.id
        nombre   = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo   = request.form.get('correo')
        
        # if current_user.miembro == True:
        #     id_miembro = Proveedor.id
        #     prover = Proveedor.obtener_miembro_por_id(id_miembro)
        #     return prover

        resultado = ControladorUsuarios.editar_usuario(idq,nombre,apellido,correo)
        if 'error' in resultado:
            # si hay error en resultado, devuelve un diccionario con el error.
            flash (resultado['mensaje'])
            print (resultado['mensaje'])
        else:
            flash("Perfil actualizado con éxito")
            print("Perfil actualizado con éxito")
            
        return redirect('/perfil')  # Redirige a la ruta de acción, si se usa POST
    

#################### Convertirse en proveedor ####################
@app.route('/perfil/me/verificar')
@login_required
def crear_miembro():
    form_validar = FormularioValidar()
    return render_template('validar_proveedor.html', form_validar=form_validar)


#************************************************** Opciones de usuario **************************************************

# Edita datos del usuario (nombre, apellido, correo)
# @app.route('/editar', methods=['POST'])
# @login_required
# def accion():



#################### Crea la tabla de proveedores ####################
@app.route('/validar', methods=["POST", "GET"])
@login_required
def validar_perfil():
    form_validar = FormularioValidar()
    id           = current_user.id
    nombre       = current_user.nombre
    apellido     = current_user.apellido
    edad         = request.form.get('edad')
    correo       = current_user.correo
    telefono     = request.form.get('telefono')
    tipo         = request.form.get('tipo')
    
    if form_validar.validate_on_submit():
        ControladorUsuarios.crear_miembro(id, nombre, apellido, edad, correo, telefono, tipo)
        return redirect('/perfilv2')

#################### Cierra la sesión del usuario actual. ####################
# (No se borra de la db)
@app.route("/cuenta/logout")
def logout():
    logout_user()
    flash(f"El usuario ha cerrado sesión")
    print(f"El usuario ha cerrado sesión")
    return(redirect("/"))

#################### Elimina al usuario actual de la db.  ####################
@app.route('/cuenta/eliminar')
@login_required
def eliminar():
    user_id = current_user.id
    ControladorUsuarios.borrar_usuario(user_id)
    flash ("usuario eliminado")
    return redirect('/')


#TODO ************************************************** Rutas de prueba **************************************************
@app.route('/pov')
def prueba():
    usuarios = Proveedor().obtener_todos()
    return render_template ('private/all_users.html', usuarios=usuarios)

@app.route('/comprobante')
def comp():
    return render_template ('validar_proveedor.html')

@app.route('/all_users')
def all_users():
    usuarios = Usuario.obtener_todos()
    return render_template('private/all_users.html', usuarios=usuarios)

@app.route('/perfilv2')
@login_required
def perfilv2():
    usuario = current_user
    return render_template('perfil_v2.html', usuario=usuario )

#! ************************************************** Manejo de errores **************************************************

#################### Página no encontrada. ####################
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

