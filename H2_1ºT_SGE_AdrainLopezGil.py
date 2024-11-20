import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Clase principal que inicializa la aplicación y gestiona la conexión a la base de datos.
class EncuestaApp:
    # Inicializa la aplicación, configura la ventana principal y conecta con la base de datos.
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Encuestas")
        
        # Configuración de la conexión a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="campusfp",
            database="ENCUESTAS"
        )
        self.cursor = self.conn.cursor()
        
        self.create_widgets()
    
    # Crea y organiza los widgets principales de la interfaz gráfica.
    def create_widgets(self):
        # Configurar una estructura de columnas más equilibrada
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Secciones de la interfaz
        self.create_input_section()
        self.create_button_section()
        self.create_treeview_section()
        self.create_filter_section()

    # Configura la sección de entrada de datos de las encuestas
    def create_input_section(self):
        input_frame = tk.LabelFrame(self.root, text="Datos de Encuesta", padx=10, pady=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Entradas para los campos de la encuesta
        self.edad_entry = self.create_label_entry(input_frame, "Edad:", 0)
        self.sexo_entry = self.create_label_entry(input_frame, "Sexo:", 1)
        self.bebidas_semana_entry = self.create_label_entry(input_frame, "Bebidas Semana:", 2)
        self.cervezas_semana_entry = self.create_label_entry(input_frame, "Cervezas Semana:", 3)
        self.bebidas_fin_semana_entry = self.create_label_entry(input_frame, "Bebidas Fin de Semana:", 4)
        self.bebidas_destiladas_semana_entry = self.create_label_entry(input_frame, "Bebidas Destiladas Semana:", 5)
        self.vinos_semana_entry = self.create_label_entry(input_frame, "Vinos Semana:", 6)
        self.perdidas_control_entry = self.create_label_entry(input_frame, "Pérdidas de Control:", 7)
        self.diversion_dependencia_alcohol_entry = self.create_label_entry(input_frame, "Diversión Dependencia Alcohol:", 8)
        self.problemas_digestivos_entry = self.create_label_entry(input_frame, "Problemas Digestivos:", 9)
        self.tension_alta_entry = self.create_label_entry(input_frame, "Tensión Alta:", 10)
        self.dolor_cabeza_entry = self.create_label_entry(input_frame, "Dolor de Cabeza:", 11)

    # Configura los botones para realizar acciones como agregar, eliminar, ver encuestas, etc.
    def create_button_section(self):
        button_frame = tk.LabelFrame(self.root, text="Acciones", padx=10, pady=10)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Botones para operaciones CRUD y gráficos
        self.create_button(button_frame, "Agregar Encuesta", self.add_encuesta, 0, 0)
        self.create_button(button_frame, "Ver Encuestas", self.view_encuestas, 1, 0)
        self.create_button(button_frame, "Eliminar Encuesta", self.eliminar_encuesta, 2, 0)
        self.create_button(button_frame, "Gráfico Edad", self.show_age_distribution, 3, 0)
        self.create_button(button_frame, "Gráfico Consumo", self.show_alcohol_consumption_by_age, 4, 0)
        self.create_button(button_frame, "Cargar Datos", self.load_data, 5, 0)
        self.create_button(button_frame, "Modificar Datos", self.update_data, 6, 0)
        self.create_button(button_frame, "Aplicar Filtros", self.apply_filters, 7, 0)
        self.create_button(button_frame, "Exportar a Excel", self.export_to_excel, 8, 0)

    # Crea el Treeview donde se muestran las encuestas almacenadas.
    def create_treeview_section(self):
        treeview_frame = tk.LabelFrame(self.root, text="Lista de Encuestas", padx=10, pady=10)
        treeview_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(treeview_frame, columns=("idEncuesta", "Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                                          "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana",
                                                          "PerdidasControl", "DiversionDependenciaAlcohol",
                                                          "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), 
                                 show="headings", height=15)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

    # Configura la sección de filtros para buscar encuestas según ciertos criterios.
    def create_filter_section(self):
        filter_frame = tk.LabelFrame(self.root, text="Filtros", padx=10, pady=10)
        filter_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        tk.Label(filter_frame, text="Filtrar Encuestas").grid(row=0, column=0, columnspan=2, pady=5)

        self.filter_edad_entry = self.create_label_entry(filter_frame, "Edad (min):", 1)
        self.filter_sexo_entry = self.create_label_entry(filter_frame, "Sexo:", 2)
        self.filter_bebidas_semana_entry = self.create_label_entry(filter_frame, "Bebidas Semana:", 3)

    # Crea un par etiqueta-campo de entrada para un campo específico.
    def create_label_entry(self, frame, label, row):
        tk.Label(frame, text=label).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    # Crea un botón y lo posiciona en el frame especificado.
    def create_button(self, frame, text, command, row, column):
        tk.Button(frame, text=text, command=command, width=20).grid(row=row, column=column, pady=5, padx=5)

    # Agrega una nueva encuesta a la base de datos con los datos ingresados en los campos.
    def add_encuesta(self):
        try:
            edad = int(self.edad_entry.get())
            sexo = self.sexo_entry.get()
            bebidas_semana = int(self.bebidas_semana_entry.get())
            cervezas_semana = int(self.cervezas_semana_entry.get())
            bebidas_fin_semana = int(self.bebidas_fin_semana_entry.get())
            bebidas_destiladas_semana = int(self.bebidas_destiladas_semana_entry.get())
            vinos_semana = int(self.vinos_semana_entry.get())
            perdidas_control = int(self.perdidas_control_entry.get())
            diversion_dependencia_alcohol = self.diversion_dependencia_alcohol_entry.get()
            problemas_digestivos = self.problemas_digestivos_entry.get()
            tension_alta = self.tension_alta_entry.get()
            dolor_cabeza = self.dolor_cabeza_entry.get()

            self.cursor.execute(
                "INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia_alcohol, problemas_digestivos, tension_alta, dolor_cabeza)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Encuesta agregada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar la encuesta: {e}")

    # Muestra todas las encuestas almacenadas en la base de datos en el Treeview.
    def view_encuestas(self):
        self.cursor.execute("SELECT * FROM ENCUESTA")
        encuestas = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for encuesta in encuestas:
            self.tree.insert("", tk.END, values=encuesta)

    # Elimina una encuesta seleccionada del Treeview y de la base de datos.
    def eliminar_encuesta(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, selecciona una encuesta para eliminar.")
            return
        valores = self.tree.item(seleccion, 'values')
        id_encuesta = valores[0]
        self.cursor.execute("DELETE FROM ENCUESTA WHERE idEncuesta = %s", (id_encuesta,))
        self.conn.commit()
        self.tree.delete(seleccion)
        messagebox.showinfo("Éxito", "Encuesta eliminada correctamente.")

    # Aplica los filtros ingresados en la sección correspondiente y actualiza el Treeview.
    def apply_filters(self):
        edad = self.filter_edad_entry.get()
        sexo = self.filter_sexo_entry.get()
        bebidas_semana = self.filter_bebidas_semana_entry.get()

        query = "SELECT * FROM ENCUESTA WHERE 1"
        params = []
        if edad:
            query += " AND Edad >= %s"
            params.append(edad)
        if sexo:
            query += " AND Sexo = %s"
            params.append(sexo)
        if bebidas_semana:
            query += " AND BebidasSemana >= %s"
            params.append(bebidas_semana)

        self.cursor.execute(query, tuple(params))
        filtered_data = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in filtered_data:
            self.tree.insert("", tk.END, values=row)

    # Exporta los datos filtrados del Treeview a un archivo Excel.
    def export_to_excel(self):
        # Obtener los datos filtrados
        self.apply_filters()

        # Obtener los datos del Treeview
        rows = []
        for row in self.tree.get_children():
            rows.append(self.tree.item(row)['values'])

        # Crear un DataFrame de pandas y exportar a Excel
        df = pd.DataFrame(rows, columns=["idEncuesta", "Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                         "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana",
                                         "PerdidasControl", "DiversionDependenciaAlcohol",
                                         "ProblemasDigestivos", "TensionAlta", "DolorCabeza"])
        file_name = "encuestas_filtradas.xlsx"
        df.to_excel(file_name, index=False)
        messagebox.showinfo("Éxito", f"Datos exportados correctamente a {file_name}.")

    # Genera un gráfico de distribución de edades basándose en los datos de la base de datos.
    def show_age_distribution(self):
        self.cursor.execute("SELECT Edad FROM ENCUESTA")
        edades = [row[0] for row in self.cursor.fetchall()]
        plt.hist(edades, bins=10, color='blue', edgecolor='black')
        plt.title("Distribución de Edades")
        plt.xlabel("Edades")
        plt.ylabel("Frecuencia")
        plt.show()

    # Genera un gráfico que muestra el consumo de alcohol por edades.
    def show_alcohol_consumption_by_age(self):
        self.cursor.execute("SELECT Edad, BebidasSemana FROM ENCUESTA")
        data = self.cursor.fetchall()
        edades = [row[0] for row in data]
        bebidas = [row[1] for row in data]
        plt.bar(edades, bebidas, color='green')
        plt.title("Consumo de Alcohol por Edad")
        plt.xlabel("Edad")
        plt.ylabel("Bebidas por Semana")
        plt.show()

    # Carga todos los datos de la base de datos en el Treeview.
    def load_data(self):
        self.view_encuestas()

    # Actualiza una encuesta seleccionada en el Treeview con los datos ingresados en los campos.
    def update_data(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un registro para actualizar.")
            return
        valores = self.tree.item(seleccion, 'values')
        id_encuesta = valores[0]

        try:
            edad = int(self.edad_entry.get())
            sexo = self.sexo_entry.get()
            bebidas_semana = int(self.bebidas_semana_entry.get())
            cervezas_semana = int(self.cervezas_semana_entry.get())
            bebidas_fin_semana = int(self.bebidas_fin_semana_entry.get())
            bebidas_destiladas_semana = int(self.bebidas_destiladas_semana_entry.get())
            vinos_semana = int(self.vinos_semana_entry.get())
            perdidas_control = int(self.perdidas_control_entry.get())
            diversion_dependencia_alcohol = self.diversion_dependencia_alcohol_entry.get()
            problemas_digestivos = self.problemas_digestivos_entry.get()
            tension_alta = self.tension_alta_entry.get()
            dolor_cabeza = self.dolor_cabeza_entry.get()

            self.cursor.execute(
                "UPDATE ENCUESTA SET Edad = %s, Sexo = %s, BebidasSemana = %s, CervezasSemana = %s, BebidasFinSemana = %s, BebidasDestiladasSemana = %s, VinosSemana = %s, PerdidasControl = %s, DiversionDependenciaAlcohol = %s, ProblemasDigestivos = %s, TensionAlta = %s, DolorCabeza = %s WHERE idEncuesta = %s",
                (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia_alcohol, problemas_digestivos, tension_alta, dolor_cabeza, id_encuesta)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Encuesta actualizada correctamente.")
            self.view_encuestas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la encuesta: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncuestaApp(root)
    root.mainloop()
