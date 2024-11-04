import tkinter as tk
from tkinter import messagebox, ttk
from database import Database
from config import COLORS

class GymOwnerApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.config(bg=COLORS['background'])

        # Título de la ventana
        title_label = tk.Label(self.root, text="Gestor de Gimnasio", font=("Arial", 18, "bold"), bg=COLORS['background'], fg=COLORS['text'])
        title_label.pack(pady=10)

        # Crear Notebook de pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        # Pestañas de gestión
        self.tab_clientes = tk.Frame(self.notebook, bg=COLORS['tab_bg'])
        self.notebook.add(self.tab_clientes, text="Gestión de Clientes")
        self.crear_tabla_clientes()

        self.tab_membresias = tk.Frame(self.notebook, bg=COLORS['tab_bg'])
        self.notebook.add(self.tab_membresias, text="Gestión de Membresías")
        self.crear_pestaña_membresias()

        self.tab_ingresos = tk.Frame(self.notebook, bg=COLORS['tab_bg'])
        self.notebook.add(self.tab_ingresos, text="Gestión de Ingresos")
        self.crear_pestaña_ingresos()

    def crear_tabla_clientes(self):
        # Entradas para añadir cliente
        tk.Label(self.tab_clientes, text="DNI:", bg=COLORS['tab_bg'], fg=COLORS['text']).grid(row=0, column=0, padx=5, pady=5)
        self.dni_entry = tk.Entry(self.tab_clientes)
        self.dni_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_clientes, text="Nombre:", bg=COLORS['tab_bg'], fg=COLORS['text']).grid(row=1, column=0, padx=5, pady=5)
        self.nombre_entry = tk.Entry(self.tab_clientes)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botón para agregar cliente
        self.agregar_cliente_btn = tk.Button(self.tab_clientes, text="Agregar Cliente", command=self.agregar_cliente, bg=COLORS['button'], fg=COLORS['button_text'], font=("Arial", 10, "bold"))
        self.agregar_cliente_btn.grid(row=0, column=2, padx=5, pady=5)
        self._hover_button(self.agregar_cliente_btn)

        # Tabla para mostrar clientes
        self.clientes_tree = ttk.Treeview(self.tab_clientes, columns=("DNI", "Nombre"), show="headings")
        self.clientes_tree.heading("DNI", text="DNI")
        self.clientes_tree.heading("Nombre", text="Nombre")
        self.clientes_tree.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

        # Botón para eliminar cliente seleccionado
        self.eliminar_cliente_btn = tk.Button(self.tab_clientes, text="Eliminar Cliente Seleccionado", command=self.eliminar_cliente, bg=COLORS['error'], fg=COLORS['button_text'])
        self.eliminar_cliente_btn.grid(row=4, column=0, columnspan=3, pady=5)
        self._hover_button(self.eliminar_cliente_btn)

        self.actualizar_tabla_clientes()

    def crear_pestaña_membresias(self):
        # Entradas para añadir membresía
        tk.Label(self.tab_membresias, text="DNI Cliente:", bg=COLORS['tab_bg'], fg=COLORS['text']).grid(row=0, column=0, padx=5, pady=5)
        self.dni_cliente_membresia = tk.Entry(self.tab_membresias)
        self.dni_cliente_membresia.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_membresias, text="Tipo:", bg=COLORS['tab_bg'], fg=COLORS['text']).grid(row=1, column=0, padx=5, pady=5)
        self.tipo_membresia = tk.Entry(self.tab_membresias)
        self.tipo_membresia.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.tab_membresias, text="Clases:", bg=COLORS['tab_bg'], fg=COLORS['text']).grid(row=2, column=0, padx=5, pady=5)
        self.clases_membresia = tk.Entry(self.tab_membresias)
        self.clases_membresia.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.tab_membresias, text="Precio:", bg=COLORS['tab_bg'], fg=COLORS['text']).grid(row=3, column=0, padx=5, pady=5)
        self.precio_membresia = tk.Entry(self.tab_membresias)
        self.precio_membresia.grid(row=3, column=1, padx=5, pady=5)

        # Botón para agregar membresía
        self.agregar_membresia_btn = tk.Button(self.tab_membresias, text="Agregar Membresía", command=self.agregar_membresia, bg=COLORS['button'], fg=COLORS['button_text'], font=("Arial", 10, "bold"))
        self.agregar_membresia_btn.grid(row=4, column=0, columnspan=2, pady=10)
        self._hover_button(self.agregar_membresia_btn)

        # Tabla para mostrar membresías
        self.membresias_tree = ttk.Treeview(self.tab_membresias, columns=("ID", "DNI Cliente", "Tipo", "Clases", "Precio"), show="headings")
        self.membresias_tree.heading("ID", text="ID")
        self.membresias_tree.heading("DNI Cliente", text="DNI Cliente")
        self.membresias_tree.heading("Tipo", text="Tipo")
        self.membresias_tree.heading("Clases", text="Clases")
        self.membresias_tree.heading("Precio", text="Precio")
        self.membresias_tree.grid(row=5, column=0, columnspan=3, padx=5, pady=10)

        self.actualizar_tabla_membresias()

    def crear_pestaña_ingresos(self):
        # Botón para ver ingresos de hoy
        self.ver_ingresos_btn = tk.Button(self.tab_ingresos, text="Ver Ingresos de Hoy", command=self.ver_ingresos_hoy, bg=COLORS['button'], fg=COLORS['button_text'], font=("Arial", 10, "bold"))
        self.ver_ingresos_btn.pack(pady=10)
        self._hover_button(self.ver_ingresos_btn)

        # Tabla para mostrar ingresos
        self.ingresos_tree = ttk.Treeview(self.tab_ingresos, columns=("DNI Cliente", "Fecha"), show="headings")
        self.ingresos_tree.heading("DNI Cliente", text="DNI Cliente")
        self.ingresos_tree.heading("Fecha", text="Fecha")
        self.ingresos_tree.pack(expand=True, fill="both", padx=5, pady=10)

    def agregar_cliente(self):
        dni = self.dni_entry.get()
        nombre = self.nombre_entry.get()
        if dni and nombre:
            if not self.db.obtener_membresias_cliente(dni):
                self.db.insertar_cliente(dni, nombre)
                self.dni_entry.delete(0, tk.END)
                self.nombre_entry.delete(0, tk.END)
                messagebox.showinfo("Éxito", "Cliente agregado exitosamente.")
                self.actualizar_tabla_clientes()
            else:
                messagebox.showwarning("Advertencia", "El cliente ya existe.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def eliminar_cliente(self):
        seleccionado = self.clientes_tree.selection()
        if seleccionado:
            dni = self.clientes_tree.item(seleccionado)['values'][0]
            self.db.eliminar_cliente(dni)
            messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
            self.actualizar_tabla_clientes()
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona un cliente para eliminar.")

    def agregar_membresia(self):
        dni = self.dni_cliente_membresia.get()
        tipo = self.tipo_membresia.get()
        clases = self.clases_membresia.get()
        precio = self.precio_membresia.get()
        if dni and tipo and clases and precio:
            self.db.insertar_membresia(dni, tipo, int(clases), float(precio))
            self.dni_cliente_membresia.delete(0, tk.END)
            self.tipo_membresia.delete(0, tk.END)
            self.clases_membresia.delete(0, tk.END)
            self.precio_membresia.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Membresía agregada exitosamente.")
            self.actualizar_tabla_membresias()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def ver_ingresos_hoy(self):
        # Implementar lógica para ver ingresos de hoy
        pass

    def actualizar_tabla_clientes(self):
        # Limpiar la tabla antes de actualizar
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        clientes = self.db.obtener_clientes()
        for cliente in clientes:
            self.clientes_tree.insert("", tk.END, values=cliente)

    def actualizar_tabla_membresias(self):
        # Limpiar la tabla antes de actualizar
        for item in self.membresias_tree.get_children():
            self.membresias_tree.delete(item)
        membresias = self.db.obtener_membresias()
        for membresia in membresias:
            self.membresias_tree.insert("", tk.END, values=membresia)

    def _hover_button(self, button):
        button.bind("<Enter>", lambda e: button.config(bg=COLORS['hover']))
        button.bind("<Leave>", lambda e: button.config(bg=COLORS['button']))

if __name__ == "__main__":
    root = tk.Tk()
    app = GymOwnerApp(root)
    root.mainloop()
