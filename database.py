import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('gym_management.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    dni TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS membresias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dni_cliente TEXT,
                    tipo TEXT,
                    clases INTEGER,
                    precio REAL,
                    estado_pago TEXT DEFAULT 'pendiente',
                    FOREIGN KEY (dni_cliente) REFERENCES clientes (dni)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ingresos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dni_cliente TEXT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dni_cliente) REFERENCES clientes (dni)
                )
            """)

    def insertar_cliente(self, dni, nombre):
        with self.conn:
            self.conn.execute("INSERT INTO clientes (dni, nombre) VALUES (?, ?)", (dni, nombre))

    def eliminar_cliente(self, dni):
        with self.conn:
            self.conn.execute("DELETE FROM clientes WHERE dni = ?", (dni,))

    def obtener_clientes(self):
        with self.conn:
            return self.conn.execute("SELECT dni, nombre FROM clientes").fetchall()

    def insertar_membresia(self, dni_cliente, tipo, clases, precio, estado_pago='pendiente'):
        with self.conn:
            self.conn.execute("INSERT INTO membresias (dni_cliente, tipo, clases, precio, estado_pago) VALUES (?, ?, ?, ?, ?)", (dni_cliente, tipo, clases, precio, estado_pago))

    def actualizar_membresia(self, membresia_id, tipo, clases, precio, estado_pago):
        with self.conn:
            self.conn.execute("UPDATE membresias SET tipo = ?, clases = ?, precio = ?, estado_pago = ? WHERE id = ?", (tipo, clases, precio, estado_pago, membresia_id))

    def obtener_membresias(self):
        with self.conn:
            return self.conn.execute("SELECT id, dni_cliente, tipo, clases, precio, estado_pago FROM membresias").fetchall()

    def obtener_membresias_cliente(self, dni_cliente):
        with self.conn:
            return self.conn.execute("SELECT id, dni_cliente, tipo, clases, precio, estado_pago FROM membresias WHERE dni_cliente = ?", (dni_cliente,)).fetchall()

    def descontar_clase(self, dni_cliente):
        with self.conn:
            self.conn.execute("UPDATE membresias SET clases = clases - 1 WHERE dni_cliente = ? AND clases > 0", (dni_cliente,))

    def registrar_ingreso(self, dni_cliente):
        with self.conn:
            # Verifica si el cliente tiene una membresía activa y cuántas clases le quedan
            resultado = self.conn.execute(
                "SELECT clases FROM membresias WHERE dni_cliente = ?", (dni_cliente,)
            ).fetchone()

            if resultado:
                clases_restantes = resultado[0]
                if clases_restantes > 0:
                    # Registra el ingreso y descuenta una clase
                    self.conn.execute("INSERT INTO ingresos (dni_cliente) VALUES (?)", (dni_cliente,))
                    self.conn.execute("UPDATE membresias SET clases = clases - 1 WHERE dni_cliente = ?", (dni_cliente,))
                    return "ingreso_exitoso"
                else:
                    return "sin_clases"  # Indica que el cliente ya no tiene clases
            else:
                return "sin_membresia"  # Indica que el cliente no tiene membresía


    def obtener_ingresos_hoy(self):
        with self.conn:
            return self.conn.execute("""
                SELECT dni_cliente, fecha FROM ingresos 
                WHERE DATE(fecha) = DATE('now')
            """).fetchall()

    def obtener_ingresos_por_mes(self, mes, año):
        with self.conn:
            return self.conn.execute("""
                SELECT dni_cliente, fecha FROM ingresos 
                WHERE strftime('%m', fecha) = ? AND strftime('%Y', fecha) = ?
            """, (f"{mes:02}", str(año))).fetchall()

    def calcular_ganancias(self):
        with self.conn:
            result = self.conn.execute("SELECT SUM(precio) FROM membresias WHERE estado_pago = 'pagado'").fetchone()
            return result[0] if result[0] is not None else 0.0
