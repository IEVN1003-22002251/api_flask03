from flask import Flask, jsonfy, request
from flask_mysql import MySQL
from flask_cors import CORS

from config import config

app = Flask(__name__)

conexion=MySQL(app)

@app.route('/alumnos', methods=['GET'])
def listar_alumnos():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos=[]
        for fila in datos:
            alumnos={'matricula' :fila[0], 'nombre':fila[1],'apellido': fila[2], 'correo' :[3]}
            alumnos.append(alumno)
        return jsonfy({'alumnos':alumnos, 'mensaje':'Alumnos encontrados', "exito":True})
    except Exception as ex:
        return jsonfy({'mensaje':'Error al listar alumno:{} '+srt(ex), "exito":False})
    
def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

def leer_alumno_bd(matricula):
    try:
        cursor = conexion.connection.cursor()
        sql ="SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos WHERE matricula = {0}".format(matricula)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            alumno = {'matricula' : datos[0], 'nombre': datos[1], 'apaterno' : datos[2], 'amaterno': datos[3], 'correo': datos[4]}
            return alumno
        else:
            return None
    except Exception as ex:

        @app.route('/alumnos/<mat>', methods=['GET'])
        def leer_curso(mat):
            try:
                alumno = leer_alumno_bd(mat)
                if alumno != None:
                    return jsonfy({'alumno': alumno, 'mensaje': "Alumno encontrado", 'exito': True})
                else:
                    return jsonfy({'mensaje': "Alumno no encontrado", 'exito':False})
            except Exception as ex:
                return jsonfy({'mensaje': "Error", 'exito': False})

@app.route("/alumnos",methods=['POST'])
def registrar_alumno():
    try:
        alumno=leer_alumno_bd(request.json['matricula'])
        if alumno != None:
            return jsonify({'mensaje':"Alumno ya existe, no se puede duplicar",
                            'exito':False})
        else:
            cursor=conexion.connection.cursor()
            sql="""insert into alumnos (matricula,nombre,apaterno,amaterno,correo)
            values ('{0}','{1}','{2}','{3}','{4}')""".format(request.json['matricula'],
                request.json['nombre'],request.json['apaterno'],request.json['amaterno'],
                request.json['correo'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':"Alumno registrado","exito":True})
       
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/alumnos/<mat>', methods=['PUT'])
def actualizar_curso(mat):
        try:
            alumno = leer_alumno_bd(mat)
            if alumno != None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno='{2}', correo='{3}'
                WHERE matricula = {4}""".format(request.json['nombre'], request.json['apaterno'], request.json['amaterno'],request.json['correo'], mat)
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error {0} ".format(ex), 'exito': False})
        
@app.route('/alumnos/<mat>', methods=['DELETE'])
def eliminar_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(mat)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})