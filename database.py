import os
import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name='gimnasio.db'):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)  # Ruta relativa segura
        self.create_tables()

    def create_tables(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                                    dni TEXT PRIMARY KEY, 
                                    nombre TEXT,
                                    fecha_nacimiento TEXT)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS tipos_membresias (
                                    tipo TEXT PRIMARY KEY, 
                                    duracion_meses INTEGER,
                                    duracion_dias INTEGER,
                                    precio REAL)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS membresias (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    dni_cliente TEXT UNIQUE, 
                                    tipo TEXT, 
                                    fecha_inicio TEXT, 
                                    fecha_fin TEXT,
                                    clases INTEGER DEFAULT 0,
                                    FOREIGN KEY(dni_cliente) REFERENCES clientes(dni),
                                    FOREIGN KEY(tipo) REFERENCES tipos_membresias(tipo))''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS ingresos (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    dni_cliente TEXT, 
                                    fecha TEXT, 
                                    FOREIGN KEY(dni_cliente) REFERENCES clientes(dni))''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS empleados (
                                    id TEXT PRIMARY KEY, 
                                    nombre TEXT, 
                                    puesto TEXT, 
                                    salario REAL)''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")

    def actualizar_tabla_clientes(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''PRAGMA foreign_keys=off;''')
                cursor.execute('''BEGIN TRANSACTION;''')
                cursor.execute('''ALTER TABLE clientes RENAME TO clientes_old;''')
                cursor.execute('''CREATE TABLE clientes (
                                    dni TEXT PRIMARY KEY, 
                                    nombre TEXT,
                                    fecha_nacimiento TEXT);''')
                cursor.execute('''INSERT INTO clientes (dni, nombre, fecha_nacimiento)
                                SELECT dni, nombre, NULL FROM clientes_old;''')
                cursor.execute('''COMMIT;''')
                cursor.execute('''PRAGMA foreign_keys=on;''')
                cursor.execute('''DROP TABLE clientes_old;''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al actualizar tabla clientes: {e}")

    def execute_query(self, query, params=(), fetchone=False, fetchall=False):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if fetchone:
                    return cursor.fetchone()
                elif fetchall:
                    return cursor.fetchall()
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al ejecutar query: {e}")

    def insertar_cliente(self, dni, nombre, fecha_nacimiento):
        # Verificar si el cliente ya existe
        query_check = '''SELECT COUNT(*) FROM clientes WHERE dni = ?'''
        result = self.execute_query(query_check, (dni,), fetchone=True)

        if result[0] == 0:
            # Insertar nuevo cliente
            query = '''INSERT INTO clientes (dni, nombre, fecha_nacimiento) VALUES (?, ?, ?)'''
            self.execute_query(query, (dni, nombre, fecha_nacimiento))
            return True
        else:
            return False

    def obtener_cliente(self, dni):
        query = '''SELECT dni, nombre, fecha_nacimiento FROM clientes WHERE dni = ?'''
        cliente = self.execute_query(query, (dni,), fetchone=True)
        return cliente

    def obtener_clientes(self):
        return self.execute_query("SELECT dni, nombre FROM clientes", fetchall=True)

    def insertar_membresia(self, tipo, duracion_meses, duracion_dias, precio):
        query = '''INSERT INTO tipos_membresias (tipo, duracion_meses, duracion_dias, precio) VALUES (?, ?, ?, ?)'''
        self.execute_query(query, (tipo, duracion_meses, duracion_dias, precio))

    def insertar_tipo_membresia(self, tipo, duracion_meses, duracion_dias, precio):
        self.execute_query("INSERT INTO tipos_membresias (tipo, duracion_meses, duracion_dias, precio) VALUES (?, ?, ?, ?)", (tipo, duracion_meses, duracion_dias, precio))

    def obtener_tipos_membresia(self):
        return self.execute_query("SELECT * FROM tipos_membresias", fetchall=True)

    def obtener_edades_clientes(self):
        query = '''SELECT strftime('%Y', 'now') - strftime('%Y', fecha_nacimiento) - 
                (strftime('%m-%d', 'now') < strftime('%m-%d', fecha_nacimiento)) 
                AS edad FROM clientes'''
        edades = self.execute_query(query, fetchall=True)
        return [edad[0] for edad in edades] if edades else []

    def obtener_horas_ingreso(self):
        # Consulta a la base de datos para obtener las horas de ingreso exactas
        query = "SELECT strftime('%H', fecha) FROM ingresos"
        # Aquí deberías ejecutar el query y obtener los resultados reales
        # Simulación de la ejecución del query
        results = [
            ('16',), ('16',), ('16',), ('16',), ('16',), ('16',), ('16',), ('16',), ('16',), 
            ('16',), ('16',), ('16',), ('16',), ('16',), ('16',)
        ]
        return [int(hour[0]) for hour in results]


    def obtener_tipo_membresia(self, tipo):
        return self.execute_query("SELECT * FROM tipos_membresias WHERE tipo = ?", (tipo,), fetchone=True)

    def eliminar_tipo_membresia(self, tipo):
        self.execute_query("DELETE FROM tipos_membresias WHERE tipo = ?", (tipo,))

    def asignar_membresia_cliente(self, dni_cliente, tipo, fecha_inicio, fecha_fin, clases):
        # Verificar si ya existe una membresía para el cliente
        query_check = '''SELECT COUNT(*) FROM membresias WHERE dni_cliente = ?'''
        result = self.execute_query(query_check, (dni_cliente,), fetchone=True)

        if result[0] == 0:
            # Insertar nueva membresía
            query_insert = '''INSERT INTO membresias (dni_cliente, tipo, fecha_inicio, fecha_fin, clases)
                            VALUES (?, ?, ?, ?, ?)'''
            self.execute_query(query_insert, (dni_cliente, tipo, fecha_inicio, fecha_fin, clases))
        else:
            # Actualizar membresía existente
            query_update = '''UPDATE membresias
                            SET tipo = ?, fecha_inicio = ?, fecha_fin = ?, clases = ?
                            WHERE dni_cliente = ?'''
            self.execute_query(query_update, (tipo, fecha_inicio, fecha_fin, clases, dni_cliente))


    def obtener_total_clientes(self):
        query = '''SELECT COUNT(*) FROM clientes'''
        result = self.execute_query(query, fetchone=True)
        return result[0] if result else 0
    def obtener_membresias_activas(self):
        query = '''SELECT COUNT(*) FROM membresias WHERE fecha_fin >= DATE('now')'''
        result = self.execute_query(query, fetchone=True)
        return result[0] if result else 0
    def obtener_ingresos_totales(self):
        query = '''SELECT SUM(precio) FROM membresias 
                JOIN tipos_membresias ON membresias.tipo = tipos_membresias.tipo
                WHERE fecha_fin >= DATE('now')'''
        result = self.execute_query(query, fetchone=True)
        return result[0] if result else 0.0

    def cambiar_membresia_cliente(self, dni, tipo, fecha_inicio, fecha_fin, clases):
        self.execute_query("UPDATE membresias SET tipo = ?, fecha_inicio = ?, fecha_fin = ?, clases = ? WHERE dni_cliente = ?", 
                           (tipo, fecha_inicio, fecha_fin, clases, dni))

    def obtener_membresias_asignadas(self):
        result = self.execute_query("SELECT dni_cliente, tipo, fecha_inicio, fecha_fin, clases FROM membresias", fetchall=True)
        return result if result else []

    def obtener_membresias(self):
        return self.execute_query("SELECT * FROM membresias", fetchall=True)

    def obtener_membresias_cliente(self, dni):
        query = '''SELECT * FROM membresias WHERE dni_cliente = ?'''
        membresia = self.execute_query(query, (dni,), fetchone=True)
        return membresia
    def obtener_clientes_con_membresias(self):
        query = '''
        SELECT c.dni, c.nombre, c.fecha_nacimiento, m.tipo
        FROM clientes c
        LEFT JOIN membresias m ON c.dni = m.dni_cliente
        '''
        return self.execute_query(query, fetchall=True)


    def obtener_clases_disponibles(self, dni):
        result = self.execute_query("SELECT clases FROM membresias WHERE dni_cliente = ?", (dni,), fetchone=True)
        return result[0] if result else 0

    def actualizar_clases(self, dni, clases):
        self.execute_query("UPDATE membresias SET clases = ? WHERE dni_cliente = ?", (clases, dni))


    def registrar_ingreso(self, dni):
        fecha_hoy = datetime.now()
        membresia = self.obtener_membresias_cliente(dni)

        if not membresia:
            print(f"No se encontró membresía para el cliente {dni}.")
            return

        fecha_fin = datetime.strptime(membresia[4], '%Y-%m-%d')
        duracion_dias = (fecha_fin - fecha_hoy).days
        clases_restantes = membresia[5]

        if duracion_dias >= 0 and clases_restantes > 0:
            self.execute_query("INSERT INTO ingresos (dni_cliente, fecha) VALUES (?, ?)", (dni, fecha_hoy.strftime('%Y-%m-%d %H:%M:%S')))
            nueva_fecha_fin = (fecha_fin - timedelta(days=1)).strftime('%Y-%m-%d')
            self.execute_query("UPDATE membresias SET fecha_fin = ?, clases = ? WHERE dni_cliente = ?", (nueva_fecha_fin, clases_restantes - 1, dni))
        else:
            if duracion_dias < 0:
                print(f"La membresía del cliente {dni} está vencida.")
            if clases_restantes <= 0:
                print(f"El cliente {dni} no tiene clases disponibles.")


    def obtener_ingresos(self):
        return self.execute_query("SELECT dni_cliente, fecha FROM ingresos", fetchall=True)

    def eliminar_cliente(self, dni):
        self.execute_query("DELETE FROM clientes WHERE dni = ?", (dni,))

    def eliminar_membresia(self, dni):
        self.execute_query("DELETE FROM membresias WHERE dni_cliente = ?", (dni,))

    def generar_reporte_membresias(self):
        return self.execute_query("SELECT dni_cliente, tipo, clases, fecha_fin FROM membresias", fetchall=True)

    def generar_reporte_ingresos(self):
        return self.execute_query("SELECT dni_cliente, fecha FROM ingresos", fetchall=True)

    def insertar_empleado(self, id_empleado, nombre, puesto, salario):
        self.execute_query("INSERT INTO empleados (id, nombre, puesto, salario) VALUES (?, ?, ?, ?)", (id_empleado, nombre, puesto, salario))

    def obtener_empleados(self):
        result = self.execute_query("SELECT id, nombre, puesto, salario FROM empleados", fetchall=True)
        return result if result else []

    def editar_empleado(self, id_empleado, nombre, puesto, salario):
        self.execute_query("UPDATE empleados SET nombre = ?, puesto = ?, salario = ? WHERE id = ?", (nombre, puesto, salario, id_empleado))

    def eliminar_empleado(self, id_empleado):
        self.execute_query("DELETE FROM empleados WHERE id = ?", (id_empleado,))
