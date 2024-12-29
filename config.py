# config.py

# Paleta de colores para la interfaz
COLORS = { 'background': '#f7f7f7',
          'menu_bg': '#333',
          'menu_fg': '#fff',
          'button_bg': '#4CAF50',
          'button_fg': '#fff',
          'title_fg': '#333',
          'tab_bg': '#e0e0e0' }
# Título de la aplicación

APP_TITLE = "Gestión de Gimnasio"

# Configuraciones de tamaño de ventanas
WINDOW_SIZES = {
    "main": (800, 600),
    "login": (400, 300),
    "client_registration": (600, 500)
}

# Rutas de archivos importantes
PATHS = {
    "database": "gimnasio.db",
    "logs": "logs/",
    "backups": "backups/"
}

# Configuraciones generales de la aplicación
APP_CONFIG = {
    "version": "1.0.0",
    "debug_mode": False,
    "max_login_attempts": 3,
    "password_min_length": 8
}