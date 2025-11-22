from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

from config import config

app = Flask(__name__)
CORS(app, resources={r"/alumnos/*": {"origins": "http://localhost:4200"}})

def get_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )


@app.route('/alumnos', methods=['GET'])
def listar_alumnos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos")
        datos = cursor.fetchall()

        alumnos = []
        for fila in datos:
            alumnos.append({
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            })

        cursor.close()
        conn.close()
        return jsonify({'alumnos': alumnos, 'mensaje': 'Alumnos encontrados'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al listar alumnos: ' + str(ex), "exito": False})


def leer_alumno_bd(matricula):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos WHERE matricula=%s"
        cursor.execute(sql, (matricula,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()

        if fila:
            return {
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            }
        else:
            return None
    except Exception as ex:
        print("Error al leer alumno:", ex)
        return None


@app.route('/alumnos/<matricula>', methods=['GET'])
def obtener_alumno(matricula):
    try:
        alumno = leer_alumno_bd(matricula)
        if alumno:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado'})
        else:
            return jsonify({'mensaje': 'Alumno no encontrado', "exito": False})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al obtener alumno: ' + str(ex), "exito": False})


@app.route('/alumnos', methods=['POST'])
def registrar_alumno():
    try:
        alumno = leer_alumno_bd(request.json['matricula'])
        if alumno != None:
            return jsonify({'mensaje': 'La matrícula ya existe', "exito": False})

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo)
        VALUES (%s, %s, %s, %s, %s)
        """

        datos = (
            request.json['matricula'],
            request.json['nombre'],
            request.json['apaterno'],
            request.json['amaterno'],
            request.json['correo']
        )

        cursor.execute(sql, datos)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Alumno registrado correctamente', "exito": True})

    except Exception as ex:
        return jsonify({'mensaje': 'Error ' + str(ex), "exito": False})


def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe...</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
