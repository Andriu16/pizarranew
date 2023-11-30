from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = '123456'
socketio = SocketIO(app)

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host='sql10.freemysqlhosting.net',
    user='sql10666575',
    password='wP8fxdDPyZ',
    database='sql10666575'
)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Buscar el usuario en la base de datos
    cur.execute('SELECT * FROM cliente WHERE correo=%s AND contrasena=%s', (username, password))
    usuario = cur.fetchone()
    
    if usuario:
        # Inicio de sesión exitoso
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        # Inicio de sesión fallido
        flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')
        return redirect(url_for('index'))#s

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('pizarras.html')
    else:
        # Redirigir a la página de inicio de sesión si el usuario no está autenticado
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Cerrar sesión y redirigir a la página de inicio
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route('/nueva_pizarra')
def nueva_pizarra():
  return render_template('pizarraexecute.html')

@app.route('/trueValidacion')
def truevalidate():
    return render_template('index.html')

@app.route('/Exit')
def salir():
    return render_template('login.html')

#@app.route('/Register')
#def register():
#return render_template('register.html')

@app.route('/registerFunc', methods=['POST'])
def registerFunc():
    if request.method == 'POST':
        # Obtén los datos del formulario de registro
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        password = request.form['password']
        
        # Aquí puedes realizar la validación de los datos del formulario.
        # Por razones de seguridad, asegúrate de encriptar la contraseña antes de guardarla en la base de datos.
        # Luego, guarda los datos en la base de datos.
        
        # Ejemplo de cómo ejecutar una consulta para insertar datos en la base de datos
        cur.execute('INSERT INTO cliente (nombre, apellido, correo, contrasena) VALUES (%s, %s, %s, %s)',
                    (nombre, apellido, correo, password))
        conn.commit()  # Guarda los cambios en la base de datos
        
        # Redirige al usuario a la página de inicio de sesión o muestra un mensaje de registro exitoso.
        return redirect(url_for('index'))
    else:
        # Si la solicitud no es de tipo POST, redirige al usuario a la página de registro.
        return render_template('register.html')

@socketio.on('message')
def handle_message(message):
    socketio.emit('message', message) 

if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app)