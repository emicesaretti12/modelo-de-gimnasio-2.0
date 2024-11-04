import tkinter as tk
from views.owner_view import GymOwnerApp
from config import COLORS, APP_TITLE

def main():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("800x600")
    root.config(bg=COLORS['background'])
    
    # Inicializar vista del dueño
    GymOwnerApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()
