import tkinter as tk
from tkinter import ttk
from owner_view import OwnerView
from client_view import ClientView

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cargando...")
        self.geometry("600x400")  # Tamaño de la pantalla de carga
        self.configure(bg="white")

        # Etiqueta de carga
        label = tk.Label(self, text="Cargando...", font=("Arial", 18, "bold"), bg="white")
        label.pack(expand=True)

        # Barra de progreso
        progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=400, mode='indeterminate')
        progress.pack(pady=20)
        progress.start()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Software Gimnasio")
        self.show_splash_screen()
    
    def show_splash_screen(self):
        splash = SplashScreen(self.root)
        self.root.after(3000, self.destroy_splash_screen, splash)  # Mostrar pantalla de carga durante 3 segundos

    def destroy_splash_screen(self, splash):
        splash.destroy()
        self.create_owner_view()
        self.create_client_view()

    def create_owner_view(self):
        owner_root = tk.Toplevel(self.root)
        OwnerView(owner_root)
        self.setup_fullscreen_bindings(owner_root)

    def create_client_view(self):
        client_root = tk.Toplevel(self.root)
        ClientView(client_root)
        self.setup_fullscreen_bindings(client_root)

    def setup_fullscreen_bindings(self, window):
        window.attributes('-fullscreen', True)
        window.fullscreen = True
        window.bind("<F11>", lambda event: self.toggle_fullscreen(window))
        window.bind("<Escape>", lambda event: self.exit_fullscreen(window))

    def toggle_fullscreen(self, window):
        window.fullscreen = not window.fullscreen
        window.attributes('-fullscreen', window.fullscreen)

    def exit_fullscreen(self, window):
        window.fullscreen = False
        window.attributes('-fullscreen', window.fullscreen)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
