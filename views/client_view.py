import tkinter as tk
from tkinter import messagebox
from database import Database
from config import COLORS

class ClientApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.config(bg=COLORS['background'])

        # Título de la ventana
        title_label = tk.Label(self.root, text="Registro de Ingreso", font=("Arial", 18, "bold"), bg=COLORS['background'], fg=COLORS['text'])
        title_label.pack(pady=10)

        # Entradas para DNI
        tk.Label(self.root, text="Ingrese su DNI:", bg=COLORS['background'], fg=COLORS['text']).pack(pady=10)
        self.dni_entry = tk.Entry(self.root)
        self.dni_entry.pack(pady=10)

        # Botón para registrar ingreso
        self.registrar_btn = tk.Button(self.root, text="Registrar Ingreso", command=self.registrar_ingreso, bg=COLORS['button'], fg=COLORS['button_text'], font=("Arial", 12, "bold"))
        self.registrar_btn.pack(pady=20)
        self._hover_button(self.registrar_btn)

        # Mensaje de estado
        self.estado_label = tk.Label(self.root, text="", bg=COLORS['background'], fg=COLORS['text'])
        self.estado_label.pack(pady=10)

    def registrar_ingreso(self):
        dni = self.dni_entry.get()
        if dni:
            cliente = self.db.obtener_cliente(dni)
            if cliente:
                # Comprobar si el cliente tiene clases disponibles
                clases_disponibles = self.db.obtener_clases_disponibles(dni)
                if clases_disponibles > 0:
                    self.db.registrar_ingreso(dni)
                    self.db.actualizar_clases(dni, clases_disponibles - 1)  # Reducir clases disponibles
                    self.estado_label.config(text="Ingreso registrado exitosamente.", fg=COLORS['success'])
                else:
                    self.estado_label.config(text="No tienes clases disponibles.", fg=COLORS['error'])
            else:
                self.estado_label.config(text="DNI no encontrado.", fg=COLORS['error'])
        else:
            messagebox.showerror("Error", "Por favor ingrese su DNI.")

    def _hover_button(self, button):
        button.bind("<Enter>", lambda e: button.config(bg=COLORS['hover']))
        button.bind("<Leave>", lambda e: button.config(bg=COLORS['button']))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
