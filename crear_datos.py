import sys
import sqlite3


# Clase para manejar datos de usuarios
class BaseDatos:
    def __init__(self, file):
        """Constructor, proveer direccion de base de datos"""
        self.file = file

    def create_connection(self):
        """Verificar conexion con la base de datos"""
        connection = None
        try:
            connection = sqlite3.connect(self.file)
        except Exception as e:
            print(e)
        return connection

    def create_user_table(self):
        """Crear tabla de los usuarios"""
        connected = self.create_connection()
        if connected:
            usr = """CREATE TABLE IF NOT EXISTS users(
                            nombre TEXT NOT NULL,
                            clave TEXT NOT NULL,
                            sexo TEXT NOT NULL,
                            edad TEXT NOT NULL,
                            ingresos TEXT NOT NULL
                    );"""
            cursor = connected.cursor()
            cursor.execute(usr)
            connected.close()
            return "Table created"
        else:
            return "No connection"

    def create_registry_table(self):
        """Crear tabla de datos/registros de diagnosticos"""
        connected = self.create_connection()
        if connected:
            log = """CREATE TABLE IF NOT EXISTS logs(
                            nombre TEXT NOT NULL,
                            clave TEXT NOT NULL,
                            sexo TEXT NOT NULL,
                            edad TEXT NOT NULL,
                            ingresos TEXT NOT NULL,
                            diagnostico TEXT NOT NULL,
                            fecha TEXT NOT NULL
                    );"""
            cursor = connected.cursor()
            cursor.execute(log)
            connected.close()
            return "Log created"
        else:
            return "No connection"
    
    def user_signin(self, nombre, clave, sexo, edad, ingresos):
        """Crear un nuevo usuario"""
        sql = """INSERT INTO users(nombre, clave, sexo, edad, ingresos)
                VALUES(?,?,?,?,?)"""
        connected = self.create_connection()
        if connected:
            if nombre != "" and clave != "":
                cursor = connected.cursor()
                ussr = (nombre,)
                cursor.execute("SELECT * FROM users WHERE nombre=?", ussr)
                if not cursor.fetchall():
                    user = (nombre, clave, sexo, edad, ingresos)
                    cursor.execute(sql, user)
                    connected.commit()
                    connected.close()
                    return "Usuario creado correctamente", (nombre, clave, sexo, edad, ingresos)
                else:
                    return "Usuario ya existe", ()
            else:
                return "Usuario/clave vacio", ()
    
    def user_login(self, user, password):
        """Permitir que el usuario ingrese"""
        connected = self.create_connection()
        if connected:
            cursor = connected.cursor()
            ussr = (user,)
            cursor.execute("SELECT * FROM users WHERE nombre=?", ussr)
            all_ = cursor.fetchone()
            if all_ and all_[1]==password:
                return (all_, "Acceso concedido")
            else:
                return ((), "Acceso denegado")
        else:
            return ((), "No hay connexion")
    
    
    def new_log(self, user, diagnostico, fecha):
        """Almacenar diagnostico de paciente"""
        sql = """INSERT INTO logs(nombre, clave, sexo, edad, ingresos, diagnostico, fecha)
                VALUES(?, ?, ?, ?, ?, ?, ?)"""
        connected = self.create_connection()
        if connected:
            cursor = connected.cursor()
            log = (*user, diagnostico, fecha)
            cursor.execute(sql, log)
            connected.commit()
            connected.close()
    
    def ver_datos(self):
        """Ver la base de datos"""
        connected = self.create_connection()
        if connected:
            cursor = connected.cursor()
            cursor.execute("SELECT * FROM users")
            for row in cursor.fetchall():
                print(row)
            print("-----------------------------")
            cursor.execute("SELECT * FROM logs")
            for row in cursor.fetchall():
                print(row)
    
    def ver_usuario(self, user_name):
        """Ver el progreso de un usuario"""
        connected = self.create_connection()
        t = (user_name,)
        if connected:
            cursor = connected.cursor()
            cursor.execute(f"""SELECT
                                    fecha, 
                                    diagnostico, 
                                    nombre 
                                FROM 
                                    logs 
                                WHERE 
                                    nombre=?""", t)
        return cursor.fetchall()
            
 
 
if __name__ == "__main__":
    print(sys.argv[1])
    if len(sys.argv) == 3 and ".db" in sys.argv[1]:
        tem = BaseDatos(sys.argv[1])
        tem.create_registry_table()
        tem.create_user_table()
  
    elif len(sys.argv) == 2 and ".db" in sys.argv[1]:
        tem = BaseDatos(sys.argv[1])
        tem.ver_datos()
    else:
        print("Numero de argumentos incorrecto")
    
    
    
    
    