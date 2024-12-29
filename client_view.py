import tkinter as tk
from tkinter import messagebox, Label
from PIL import Image, ImageTk
from database import Database
from datetime import datetime

class ClientView:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("Registro de Ingreso - Gimnasio")
        self.root.attributes("-fullscreen", True)  # Pantalla completa
        self.root.bind("<Escape>", self.exit_fullscreen)  # Permitir salir de pantalla completa con Escape

        self.setup_ui()

    def setup_ui(self):
        # Cargar la imagen de fondo
        self.background_image = Image.open("C:/Users/emiliano/OneDrive/modelo de gimnasio 2/imagen.jpg")
        self.background_label = Label(self.root)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.update_background()

        # Crear un frame con estilo
        frame = tk.Frame(self.root, bg="#ffffff", relief="groove", bd=2, padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)

        title = tk.Label(frame, text="Bienvenido al Gimnasio", font=("Helvetica", 28, "bold"), fg="#333333", bg="#ffffff")
        title.pack(pady=10)

        dni_label = tk.Label(frame, text="Ingrese su DNI:", font=("Helvetica", 20), fg="#333333", bg="#ffffff")
        dni_label.pack(pady=10)
        
        self.dni_entry = tk.Entry(frame, font=("Helvetica", 18), width=25, bd=2, relief="groove")
        self.dni_entry.pack(pady=5)
        
        # Vincular la tecla Enter al campo de entrada
        self.dni_entry.bind("<Return>", self.on_enter)

        register_button = tk.Button(frame, text="Registrar Ingreso", command=self.registrar_ingreso, bg="#4CAF50", fg="white", font=("Helvetica", 18, "bold"), height=2, width=25, bd=0)
        register_button.pack(pady=20)

    def update_background(self):
        # Redimensionar la imagen para que ocupe todo el fondo
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.background_resized = self.background_image.resize((width, height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_resized)
        self.background_label.config(image=self.background_photo)
        self.background_label.image = self.background_photo  # Mantener una referencia a la imagen

    def registrar_ingreso(self):
        dni = self.dni_entry.get()
        cliente = self.db.obtener_cliente(dni)

        if cliente:
            clases_restantes = self.db.obtener_clases_disponibles(dni)
            if clases_restantes > 0:
                self.db.registrar_ingreso(dni)
                nombre = cliente[1]
                clases_restantes -= 1
                self.show_temp_message(f"Bienvenido {nombre}!\nSu ingreso ha sido registrado.\nClases restantes: {clases_restantes}", "success")
            else:
                self.show_temp_message("Sin clases disponibles, comuníquese con el monitor", "error")
            self.dni_entry.delete(0, tk.END)  # Limpiar el campo de entrada después de registrar
        else:
            self.show_temp_message("Cliente no encontrado. Por favor, verifique su DNI.", "error")

    def show_temp_message(self, message, message_type):
        # Definir colores para el mensaje
        colors = {
            "success": "#4CAF50",
            "error": "#FF0000"
        }
        color = colors.get(message_type, "#4CAF50")

        # Crear un label temporal para mostrar el mensaje
        temp_label = tk.Label(self.root, text=message, font=("Helvetica", 16), fg="white", bg=color, padx=10, pady=10, relief="solid")
        temp_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Deslizar el label hacia arriba y luego eliminarlo
        def slide_up():
            y = temp_label.winfo_y()
            if y > -50:
                temp_label.place(y=y-2)
                self.root.after(10, slide_up)
            else:
                temp_label.destroy()

        self.root.after(2000, slide_up)

    def on_enter(self, event):
        self.registrar_ingreso()

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientView(root)
    root.mainloop()
