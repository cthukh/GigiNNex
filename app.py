from flask import Flask, render_template, flash, redirect
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = '9s12eue3b8rh38edj3xn832u8xn'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/deginnex'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth"

from forms import FormularioRegistro, FormularioAcceso
from models import Usuario
from controllers import ControladorUsuarios

Migrate(app,db)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Ruta que maneja si el usuario ya esta registrado y si tiene sesión abierta.
@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if current_user.is_authenticated:
        return redirect("/inicio")

    if form_registro == None:
        form_registro = FormularioRegistro()

    if form_acceso == None:
        form_acceso = FormularioAcceso()
    return render_template("auth.html", form_registro=form_registro, form_acceso=form_acceso)

# Ruta que maneja el registro de nuevos usuarios
@app.route("/register", methods=["POST"])
def register():
    form   = FormularioRegistro()
    error  = None

    if form.validate_on_submit():
        print("form valido")
        flash("Form valido")
        nombre = form.nombre.data
        correo = form.correo.data 
        clave  = form.clave.data 
        #Consultamos si existe en la db 
        usuario = Usuario().obtener_por_correo(correo)

        if usuario is not None:
            error = f"El correo {correo} ya se encuentra registrado"
            print(error)
            flash(error)
            return(redirect("/"))

        else:
            flash(f'Registro solicitado para el usuario { nombre }')
            #Utilización de un controlador entre Vista y Modelo
            ControladorUsuarios().crear_usuario(nombre, correo, clave)
            #Generamos una instancia de datos
            return redirect("/")

    else:
        print("form invalido")
        flash("Form invalido")
        return auth(form_registro=form)

# Ruta si el usuario ya esta registrado
@app.route("/login", methods=["POST"])
def login():
    form_acceso = FormularioAcceso()
    if form_acceso.validate_on_submit():
        flash(f"Acceso solicitado para el usuario { form_acceso.correo.data }")
        usuario = Usuario().obtener_por_correo(form_acceso.correo.data)
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

# pagina principal
@app.route('/inicio')
def index():
    return render_template('index.html')

# seleccion de categorias
@app.route('/service/<string:categoria>')
def selecionar_categorias(categoria):
    if   categoria == 'videos':
        return render_template ('cat_videos.html')
    elif categoria == 'imagenes':
        return render_template ('cat_imagenes.html')
    elif categoria == 'audio':
        return render_template ('cat_audio.html')
    elif categoria == 'sitios_web':
        return render_template ('cat_web.html')

# opciones de usuario

@app.route("/perfil")
@login_required
def perfil():
    # Ahora deberia recojer los datos solo de la sesion activa y enviarlos a perfil.html
    return render_template("perfil.html", usuario=current_user)

@app.route("/logout")
def logout():
    logout_user()
    flash(f"El usuario ha cerrado sesión")
    print(f"El usuario ha cerrado sesión")
    return(redirect("/"))

@app.route("/userop")
def opciones_usuario():
    return redirect ("/home")

# errores

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/prueba')
def prueba():
    return render_template('indexcalixtro.html')

