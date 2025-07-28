from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_mysqldb import MySQL
from functools import wraps
import os

nodo = os.getenv("NODO", "desconocido")

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

app.config['MYSQL_HOST'] = 'db'  # cambia a 'localhost' si no usas docker
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'inventario'

mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Por favor, inicia sesión para acceder.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html', nodo=nodo)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()
    if user:
        session['user_email'] = email
        flash(f'Bienvenido {email}!')
        return redirect(url_for('dashboard'))
    else:
        flash('Credenciales incorrectas')
        return render_template('login.html', nodo=nodo)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    print("Productos:", productos)  # debug
    return render_template('dashboard.html', productos=productos, email=session.get('user_email'), nodo=nodo)

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        unidad = request.form['unidad']
        categoria = request.form['categoria']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
        if cur.fetchone():
            flash('Código duplicado')
            return render_template('registrar_producto.html', nodo=nodo)
        cur.execute("INSERT INTO productos (nombre, codigo, descripcion, unidad, categoria) VALUES (%s, %s, %s, %s, %s)",
                    (nombre, codigo, descripcion, unidad, categoria))
        mysql.connection.commit()
        flash('Producto registrado correctamente')
        return redirect(url_for('dashboard'))
    return render_template('registrar_producto.html', nodo=nodo)

@app.route('/consultar')
@login_required
def consultar():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


