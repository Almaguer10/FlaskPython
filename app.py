from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#Session Settings
app.secret_key = 'mysecretkey'

#Rutas
@app.route("/")
def inicio():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Contactos')
    data = cur.fetchall()
                                                   #Pasando Contactos
    return render_template("Contactos/index.html", contactos = data)

@app.route('/Nuevo', methods=['POST'])
def nuevo_contacto():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        telefono = request.form['Tel']
        email = request.form['Email']

        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO contactos (Nombre, Telefono, Correo) VALUES(%s,%s,%s)', (nombre, telefono, email))
        
        mysql.connection.commit()

        flash("Contacto Agregado Satisfactoriamente")

        return redirect(url_for('inicio')) #Funcion que llama la ruta donde queramos ir

@app.route('/Editar/<int:id>')
def editar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Contactos WHERE ID = {0}'.format(id))
    data = cur.fetchall()
    return render_template('Contactos/editar.html', Contactos = data[0])
    
    #return f"{data[0]}"
@app.route('/Editado/<id>', methods = ['POST'])
def Editado(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Telefono = request.form['Telefono']
        Email = request.form['Email']
        cur = mysql.connection.cursor()
        #Elegibilidad del codigo más comoda ######
        cur.execute("""
                    UPDATE contactos
                    SET Nombre = %s,
                        Telefono = %s,
                        Correo = %s
                    WHERE id = %s
                """, (Nombre, Telefono, Email, id))
        mysql.connection.commit()
        flash('Contacto Actualizado Satisfactoriamente')
        return redirect(url_for('inicio'))


@app.route('/Eliminar/<string:id>')
def eliminar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado Satisfactoriamente')
    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)