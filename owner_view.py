import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors as mcolors
from fpdf import FPDF
from datetime import datetime, timedelta
from tkcalendar import Calendar
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
import matplotlib.pyplot as plt
import io
import numpy as np
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def showtip(self, text, x, y):
        if self.tipwindow or not text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()



class OwnerView:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("Panel del Propietario - Gimnasio")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.tooltip = None
        self.setup_ui()
        
    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#4CAF50", height=80)
        header_frame.pack(fill="x")
        header_label = tk.Label(header_frame, text="Panel del Propietario", bg="#4CAF50", fg="white",
                                font=("Arial", 24, "bold"))
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        sidebar_frame = tk.Frame(self.root, bg="#333333", width=200)
        sidebar_frame.pack(side="left", fill="y")

        buttons = [
            ("Clientes", self.show_clients),
            ("Membresías", self.show_memberships),
            ("Ingresos", self.show_incomes),
            ("Reportes", self.show_reports),
            ("Salir", self.root.quit)
        ]

        for text, command in buttons:
            button = tk.Button(sidebar_frame, text=text, bg="#444", fg="white", font=("Arial", 12, "bold"),
                            relief="flat", command=command)
            button.pack(fill="x", pady=5, padx=10)

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.show_clients()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def hide_client_info(self, event):
        if self.tooltip:
            self.tooltip.hidetip()
            self.tooltip = None
    def show_client_info(self, event):
        item_id = self.client_table.identify_row(event.y)
        if item_id:
            client_data = self.client_table.item(item_id, "values")
            dni = client_data[0]
            client_info = self.db.obtener_cliente(dni)
            membership_info = self.db.obtener_membresias_cliente(dni)

            if client_info and membership_info:
                fecha_fin = datetime.strptime(membership_info[4], '%Y-%m-%d')
                duracion_dias = (fecha_fin - datetime.now()).days
                tooltip_text = (f"DNI: {client_info[0]}\n"
                                f"Nombre: {client_info[1]}\n"
                                f"Fecha de Nacimiento: {client_info[2]}\n"
                                f"Tipo de Membresía: {membership_info[2]}\n"
                                f"Días restantes: {duracion_dias}")

                x, y, _, _ = self.client_table.bbox(item_id)  # Obtener la posición del elemento
                x += self.client_table.winfo_rootx()
                y += self.client_table.winfo_rooty()

                if self.tooltip:
                    self.tooltip.hidetip()
                self.tooltip = ToolTip(self.client_table)
                self.tooltip.showtip(tooltip_text, x, y)
            else:
                if self.tooltip:
                    self.tooltip.hidetip()
                    self.tooltip = None
        else:
            if self.tooltip:
                self.tooltip.hidetip()
                self.tooltip = None
    
    def show_clients(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Gestión de Clientes", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("DNI", "Nombre")
        self.client_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.client_table.heading("DNI", text="DNI")
        self.client_table.heading("Nombre", text="Nombre")
        self.client_table.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.client_table.yview)
        self.client_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.client_table.bind("<Motion>", self.show_client_info)
        self.client_table.bind("<Leave>", self.hide_client_info)

        self.load_clients()

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(button_frame, text="Agregar Cliente", command=self.add_client, bg="#4CAF50", fg="white",
                font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Eliminar Cliente", command=self.delete_client, bg="#F44336", fg="white",
                font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Asignar Membresía", command=self.assign_membership, bg="#2196F3", fg="white",
                font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Editar Membresía", command=self.edit_membership, bg="#FF9800", fg="white",
                font=("Arial", 12)).pack(side="left", padx=5)

    def load_clients(self):
        for row in self.client_table.get_children():
            self.client_table.delete(row)
        clients = self.db.obtener_clientes()
        for client in clients:
            self.client_table.insert("", "end", values=client)

    
    def add_client(self):
        def save_client():
            dni = dni_entry.get()
            name = name_entry.get()
            birthdate = cal.get_date()
            if dni and name and birthdate:
                success = self.db.insertar_cliente(dni, name, birthdate)
                if success:
                    messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                    add_window.destroy()
                    self.load_clients()
                else:
                    messagebox.showerror("Error", "El cliente con este DNI ya existe.")
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Cliente")
        add_window.geometry("400x500")

        frame = tk.Frame(add_window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="DNI:", font=("Arial", 12)).pack(pady=5)
        dni_entry = tk.Entry(frame, font=("Arial", 12))
        dni_entry.pack(pady=5)

        tk.Label(frame, text="Nombre:", font=("Arial", 12)).pack(pady=5)
        name_entry = tk.Entry(frame, font=("Arial", 12))
        name_entry.pack(pady=5)

        tk.Label(frame, text="Fecha de Nacimiento:", font=("Arial", 12)).pack(pady=5)
        cal = Calendar(frame, selectmode='day', year=2000, month=1, day=1, date_pattern='yyyy-mm-dd', font=("Arial", 12))
        cal.pack(pady=10)

        # Añadir una separación para asegurarnos de que el botón "Guardar" sea visible
        spacer = tk.Label(frame, text=" ", font=("Arial", 12))
        spacer.pack(pady=10)

        tk.Button(frame, text="Guardar", command=save_client, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

        add_window.update_idletasks()
        add_window.geometry(add_window.geometry())  # Refrescar la geometría de la ventana



    def delete_client(self):
        selected_item = self.client_table.selection()
        if selected_item:
            dni = self.client_table.item(selected_item, "values")[0]
            self.db.eliminar_cliente(dni)
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            self.load_clients()
        else:
            messagebox.showerror("Error", "Por favor, seleccione un cliente para eliminar.")
    
    def add_membership(self):
        def save_membership():
            tipo = tipo_entry.get()
            duracion_meses = duracion_meses_entry.get()
            duracion_dias = duracion_dias_entry.get()
            precio = precio_entry.get()
            if tipo and (duracion_meses or duracion_dias) and precio:
                self.db.insertar_membresia(tipo, duracion_meses, duracion_dias, precio)
                messagebox.showinfo("Éxito", "Membresía agregada correctamente.")
                add_window.destroy()
                self.load_memberships()
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")

        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Membresía")
        add_window.geometry("300x400")

        frame = tk.Frame(add_window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Tipo:", font=("Arial", 12)).pack(pady=5)
        tipo_entry = tk.Entry(frame, font=("Arial", 12))
        tipo_entry.pack(pady=5)

        tk.Label(frame, text="Duración (Meses):", font=("Arial", 12)).pack(pady=5)
        duracion_meses_entry = tk.Entry(frame, font=("Arial", 12))
        duracion_meses_entry.pack(pady=5)

        tk.Label(frame, text="Duración (Días):", font=("Arial", 12)).pack(pady=5)
        duracion_dias_entry = tk.Entry(frame, font=("Arial", 12))
        duracion_dias_entry.pack(pady=5)

        tk.Label(frame, text="Precio:", font=("Arial", 12)).pack(pady=5)
        precio_entry = tk.Entry(frame, font=("Arial", 12))
        precio_entry.pack(pady=5)

        tk.Button(frame, text="Guardar", command=save_membership, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)

    def edit_membership(self):
        
        selected_client = self.client_table.selection()
        if selected_client:
            client_dni = self.client_table.item(selected_client, "values")[0]
            membership_info = self.db.obtener_membresias_cliente(client_dni)

            if not membership_info:
                messagebox.showerror("Error", "Este cliente no tiene una membresía asignada.")
                return

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Editar Membresía")
            edit_window.geometry("300x400")

            tk.Label(edit_window, text="Tipo de Membresía Actual:").pack(pady=5)
            tk.Label(edit_window, text=membership_info[2]).pack(pady=5)

            tk.Label(edit_window, text="Cambiar a Membresía:").pack(pady=5)
            memberships = self.db.obtener_tipos_membresia()
            membership_options = [membership[0] for membership in memberships]
            membership_combobox = ttk.Combobox(edit_window, values=membership_options)
            membership_combobox.pack(pady=5)
            def save_edit():
                new_membership = membership_combobox.get()
                if new_membership:
                    new_membership_data = self.db.obtener_tipo_membresia(new_membership)
                    
                    # Asegurarnos de que los datos de la membresía sean válidos y convertibles a enteros
                    try:
                        duracion_meses_str = new_membership_data[1]
                        duracion_dias_str = new_membership_data[2]
                        
                        # Verificar si duracion_meses_str y duracion_dias_str son enteros
                        duracion_meses = int(duracion_meses_str) if isinstance(duracion_meses_str, (int, str)) and str(duracion_meses_str).isdigit() else 0
                        duracion_dias = int(duracion_dias_str) if isinstance(duracion_dias_str, (int, str)) and str(duracion_dias_str).isdigit() else 0
                    except (ValueError, IndexError) as e:
                        messagebox.showerror("Error", "Datos de membresía inválidos.")
                        return

                    clases_iniciales = duracion_dias if duracion_dias > 0 else duracion_meses * 30

                    fecha_inicio = datetime.now()
                    try:
                        if duracion_meses > 0:
                            fecha_fin = fecha_inicio + timedelta(days=duracion_meses * 30)
                        else:
                            fecha_fin = fecha_inicio + timedelta(days=duracion_dias)

                        self.db.asignar_membresia_cliente(client_dni, new_membership, fecha_inicio.strftime('%Y-%m-%d'), fecha_fin.strftime('%Y-%m-%d'), clases_iniciales)
                        messagebox.showinfo("Éxito", "Membresía editada correctamente.")
                        edit_window.destroy()
                        self.load_clients()
                    except OverflowError:
                        messagebox.showerror("Error", "La duración de la membresía es demasiado grande.")
                else:
                    messagebox.showerror("Error", "Por favor, seleccione una membresía.")

            tk.Button(edit_window, text="Guardar", command=save_edit, bg="#4CAF50", fg="white").pack(pady=10)





    def show_memberships(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Gestión de Membresías", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Nombre", "Duración", "Precio")
        self.membership_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.membership_table.heading("ID", text="ID")
        self.membership_table.heading("Nombre", text="Nombre")
        self.membership_table.heading("Duración", text="Duración")
        self.membership_table.heading("Precio", text="Precio")
        self.membership_table.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.membership_table.yview)
        self.membership_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_memberships()

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(button_frame, text="Agregar Membresía", command=self.add_membership, bg="#4CAF50", fg="white",
                font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Eliminar Membresía", command=self.delete_membership, bg="#F44336", fg="white",
                font=("Arial", 12)).pack(side="left", padx=5)



    def load_memberships(self):
        for row in self.membership_table.get_children():
            self.membership_table.delete(row)
        memberships = self.db.obtener_tipos_membresia()
        for membership in memberships:
            self.membership_table.insert("", "end", values=membership)
    def assign_membership(self):
        selected_client = self.client_table.selection()
        if selected_client:
            client_dni = self.client_table.item(selected_client, "values")[0]

            assign_window = tk.Toplevel(self.root)
            assign_window.title("Asignar Membresía")
            assign_window.geometry("300x300")

            tk.Label(assign_window, text="Seleccionar Membresía:").pack(pady=5)
            memberships = self.db.obtener_tipos_membresia()
            membership_options = [membership[0] for membership in memberships]
            membership_combobox = ttk.Combobox(assign_window, values=membership_options)
            membership_combobox.pack(pady=5)

            def save_assignment():
                selected_membership = membership_combobox.get()
                if selected_membership:
                    selected_membership_data = self.db.obtener_tipo_membresia(selected_membership)
                    duracion_meses = int(selected_membership_data[1]) if selected_membership_data[1] else 0
                    duracion_dias = int(selected_membership_data[2]) if selected_membership_data[2] else 0
                    clases_iniciales = duracion_dias if duracion_dias > 0 else duracion_meses * 30

                    fecha_inicio = datetime.now()
                    try:
                        if duracion_meses > 0:
                            fecha_fin = fecha_inicio + timedelta(days=duracion_meses * 30)
                        else:
                            fecha_fin = fecha_inicio + timedelta(days=duracion_dias)

                        self.db.asignar_membresia_cliente(client_dni, selected_membership, fecha_inicio.strftime('%Y-%m-%d'), fecha_fin.strftime('%Y-%m-%d'), clases_iniciales)
                        messagebox.showinfo("Éxito", "Membresía asignada correctamente.")
                        assign_window.destroy()
                        self.load_clients()
                    except OverflowError:
                        messagebox.showerror("Error", "La duración de la membresía es demasiado grande.")
                else:
                    messagebox.showerror("Error", "Por favor, seleccione una membresía.")

            tk.Button(assign_window, text="Guardar", command=save_assignment, bg="#4CAF50", fg="white").pack(pady=10)
        else:
            messagebox.showerror("Error", "Por favor, seleccione un cliente.")


    def update_duration_entry_assign(self):
        self.duration_entry_assign.delete(0, tk.END)



    def delete_membership(self):
        selected_item = self.membership_table.selection()
        if selected_item:
            id = self.membership_table.item(selected_item, "values")[0]
            self.db.eliminar_tipo_membresia(id)
            messagebox.showinfo("Éxito", "Membresía eliminada correctamente.")
            self.load_memberships()
        else:
            messagebox.showerror("Error", "Por favor, seleccione una membresía para eliminar.")

    def show_incomes(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Registros de Ingresos", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        # Crear un canvas con barra de desplazamiento
        canvas = tk.Canvas(self.main_frame)
        scrollbar = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Colores para los gráficos de torta
        colors = list(mcolors.TABLEAU_COLORS.values())

        def create_pie_chart():
            # Gráfico de torta para distribución de edades
            fig1, ax1 = plt.subplots(figsize=(5, 3))
            ages = self.db.obtener_edades_clientes()
            age_bins = [10, 20, 30, 40, 50, 60, 70]
            age_labels = [f'{age_bins[i]}-{age_bins[i+1]-1}' for i in range(len(age_bins)-1)]
            age_counts = [sum(1 for age in ages if age_bins[i] <= age < age_bins[i+1]) for i in range(len(age_bins)-1)]
            age_counts.append(sum(1 for age in ages if age >= age_bins[-1]))
            age_labels.append(f'{age_bins[-1]}+')

            # Verificar y manejar valores NaN
            age_counts = np.nan_to_num(age_counts)  # Convertir NaN a 0

            wedges, texts, autotexts = ax1.pie(
                age_counts, labels=age_labels, autopct='%1.1f%%', startangle=140, colors=colors,
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.5, 'linestyle': 'solid', 'antialiased': True}
            )
            ax1.set_title('Distribución de Edades de Clientes')
            for text in texts + autotexts:
                text.set_fontsize(10)
                text.set_fontweight('bold')
                text.set_color('white')  # Hacer los números más legibles
            ax1.legend(wedges, age_labels, title="Edades", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            canvas1 = FigureCanvasTkAgg(fig1, master=scrollable_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        
            

        def create_bar_chart():
            # Gráfico de barras para horarios más visitados
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            
            # Obtener horas de ingreso de la base de datos
            hours = self.db.obtener_horas_ingreso()
            
            # Inicializar el conteo de horas a 0 para cada hora del día
            hour_bins = list(range(24))
            hour_counts = [0] * 24  # Inicializar el conteo de horas a 0
            
            for hour in hours:
                try:
                    # Asegurarse de que `hour` es un entero
                    hour_int = int(hour)
                    if 0 <= hour_int < 24:
                        hour_counts[hour_int] += 1  # Incrementar el conteo para cada hora registrada
                except ValueError:
                    continue  # Ignorar valores no enteros

            # Crear el gráfico de barras
            bars = ax2.bar(hour_bins, hour_counts, color='skyblue', edgecolor='black', width=0.6)

            # Resaltar las barras con el mayor número de ingresos
            max_count = max(hour_counts)
            for bar in bars:
                if bar.get_height() == max_count:
                    bar.set_color('darkblue')

            ax2.set_xticks(hour_bins)
            ax2.set_xticklabels([f'{hour}:00' for hour in hour_bins], rotation=45, ha="right", fontsize=10)
            ax2.set_xlabel('Horas del Día', fontsize=12)
            ax2.set_ylabel('Número de Ingresos', fontsize=12)
            ax2.set_title('Horarios Más Visitados en el Gimnasio', fontsize=14)
            ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

            # Añadir etiquetas a cada barra
            for index, value in enumerate(hour_counts):
                ax2.text(index, value + 0.3, str(value), ha='center', va='bottom', fontsize=8, color='black')  # Etiquetas más grandes y legibles

            # Ajustar el diseño para que las etiquetas no se corten
            fig2.tight_layout()

            canvas2 = FigureCanvasTkAgg(fig2, master=scrollable_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)


        # Llamar a las funciones dentro del hilo principal usando after_idle
        self.main_frame.after_idle(create_pie_chart)
        self.main_frame.after_idle(create_bar_chart)



    def load_incomes(self):
        for row in self.income_table.get_children():
            self.income_table.delete(row)
        incomes = self.db.obtener_ingresos()
        for income in incomes:
            self.income_table.insert("", "end", values=income)

    def add_income(self):
        def save_income():
            date = date_entry.get()
            amount = amount_entry.get()
            if date and amount:
                self.db.insertar_ingreso(date, amount)
                messagebox.showinfo("Éxito", "Ingreso agregado correctamente.")
                add_window.destroy()
                self.load_incomes()
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")

        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Ingreso")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Fecha (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(add_window)
        date_entry.pack(pady=5)

        tk.Label(add_window, text="Monto:").pack(pady=5)
        amount_entry = tk.Entry(add_window)
        amount_entry.pack(pady=5)

        tk.Button(add_window, text="Guardar", command=save_income, bg="#4CAF50", fg="white").pack(pady=10)

    def plot_incomes(self):
        incomes = self.db.obtener_ingresos()
        dates = [income[0] for income in incomes]
        amounts = [float(income[1]) for income in incomes]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, amounts, marker='o')
        plt.title("Ingresos a lo largo del tiempo")
        plt.xlabel("Fecha")
        plt.ylabel("Monto")
        plt.grid()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_reports(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Reportes", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        tk.Button(self.main_frame, text="Generar Reporte en PDF", command=self.generate_report, bg="#4CAF50", fg="white",
                  font=("Arial", 12)).pack(pady=10)






    def generate_report(self):
        try:
            doc = SimpleDocTemplate("reporte_clientes.pdf", pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            # Encabezado
            title_style = styles["Title"]
            title = Paragraph("Reporte de Clientes y Membresías", title_style)
            elements.append(title)
            elements.append(Spacer(1, 12))

            # Definir colores para los gráficos de torta
            pie_colors = list(mcolors.TABLEAU_COLORS.values())

            # Gráfico de Distribución de Edades
            ages = self.db.obtener_edades_clientes()
            age_bins = [10, 20, 30, 40, 50, 60, 70]
            age_labels = [f'{age_bins[i]}-{age_bins[i+1]-1}' for i in range(len(age_bins)-1)]
            age_counts = [sum(1 for age in ages if age_bins[i] <= age < age_bins[i+1]) for i in range(len(age_bins)-1)]
            age_counts.append(sum(1 for age in ages if age >= age_bins[-1]))
            age_labels.append(f'{age_bins[-1]}+')

            fig1, ax1 = plt.subplots(figsize=(5, 4))
            wedges, texts, autotexts = ax1.pie(age_counts, labels=age_labels, autopct='%1.1f%%', startangle=140, colors=pie_colors,
                                            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5, 'linestyle': 'solid', 'antialiased': True})
            ax1.set_title('Distribución de Edades de Clientes', fontsize=14)
            for text in texts + autotexts:
                text.set_fontsize(14)
                text.set_fontweight('bold')
                text.set_color('white')  # Usar blanco para mejor contraste

            buf1 = io.BytesIO()
            plt.savefig(buf1, format='png')
            buf1.seek(0)
            image1 = Image(buf1)
            image1.drawHeight = 200
            image1.drawWidth = 200
            elements.append(image1)
            elements.append(Spacer(1, 12))

            # Gráfico de Horarios Más Visitados
            hours = self.db.obtener_horas_ingreso()
            hour_bins = list(range(24))
            hour_labels = [f'{hour}:00 - {hour+1}:00' for hour in hour_bins]
            hour_counts = [hours.count(hour) for hour in hour_bins]

            fig2, ax2 = plt.subplots(figsize=(5, 4))
            wedges, texts, autotexts = ax2.pie(hour_counts, labels=hour_labels, autopct='%1.1f%%', startangle=140, colors=pie_colors,
                                            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5, 'linestyle': 'solid', 'antialiased': True})
            ax2.set_title('Horarios Más Visitados', fontsize=14)
            for text in texts + autotexts:
                text.set_fontsize(14)
                text.set_fontweight('bold')
                text.set_color('white')  # Usar blanco para mejor contraste

            buf2 = io.BytesIO()
            plt.savefig(buf2, format='png')
            buf2.seek(0)
            image2 = Image(buf2)
            image2.drawHeight = 200
            image2.drawWidth = 200
            elements.append(image2)
            elements.append(Spacer(1, 12))

            # Información Adicional
            p_style = ParagraphStyle(name='Normal', fontSize=12)
            total_clients = len(self.db.obtener_clientes())
            active_memberships = len(self.db.obtener_membresias())
            total_revenue = self.db.obtener_ingresos_totales() if hasattr(self.db, 'obtener_ingresos_totales') else 0

            elements.append(Paragraph(f"Total de Clientes: {total_clients}", p_style))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"Membresías Activas: {active_memberships}", p_style))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"Ingresos Totales: ${total_revenue:.2f}", p_style))
            elements.append(Spacer(1, 12))

            # Tabla con todos los clientes y sus tipos de membresía
            clients = self.db.obtener_clientes_con_membresias()
            client_data = [["DNI", "Nombre", "Fecha de Nacimiento", "Tipo de Membresía"]]
            for client in clients:
                client_data.append([client[0], client[1], client[2], client[3]])

            table = Table(client_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

            # Pie de Página
            footer = Paragraph("Reporte generado automáticamente", styles["Normal"])
            elements.append(Spacer(1, 24))
            elements.append(footer)

            # Crear el PDF
            doc.build(elements)

            # Mostrar mensaje de éxito en el hilo principal de Tkinter
            self.root.after_idle(lambda: messagebox.showinfo("Éxito", "Reporte generado con éxito."))
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al generar el reporte: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = OwnerView(root)
    root.mainloop()
