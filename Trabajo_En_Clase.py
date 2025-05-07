import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import math
import cv2
from PIL import Image, ImageTk
import os
import csv

class HealthCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Inteligente de Salud")
        self.geometry("900x600")
        self.preferences_file = "preferences.json"
        self.data_history_file = "data_history.json"
        self.history = []
        self.load_preferences()

        self.create_main_tabs()

    def load_preferences(self):
        # Cargar preferencias de usuario si existen
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, "r") as f:
                    self.preferences = json.load(f)
            except:
                self.preferences = {"theme": "light"}
        else:
            self.preferences = {"theme": "light"}

    def save_preferences(self):
        # Guardar las preferencias en un archivo JSON
        with open(self.preferences_file, "w") as f:
            json.dump(self.preferences, f)

    def create_main_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Datos personales y preferencias
        self.tab_datos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_datos, text="Datos Personales")
        self.create_tab_datos()

        # Tab 2: Medidor Visual Interactivo
        self.tab_medidor = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_medidor, text="Medidor Visual")
        self.create_tab_medidor()

        # Tab 3: Análisis de Imagen
        self.tab_imagen = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_imagen, text="Análisis de Imagen")
        self.create_tab_imagen()

        # Tab 4: Recomendaciones
        self.tab_recomendaciones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_recomendaciones, text="Recomendaciones")
        self.create_tab_recomendaciones()

        # Tab 5: Historial y Exportación
        self.tab_historial = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_historial, text="Historial de Medidas")
        self.create_tab_historial()

    # ---------------------------
    # Tab 1: Datos Personales
    # ---------------------------
    def create_tab_datos(self):
        frame = self.tab_datos
        lbl_title = ttk.Label(frame, text="Ingrese sus datos:", font=("Helvetica", 16))
        lbl_title.pack(pady=10)

        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10)

        # Peso
        ttk.Label(form_frame, text="Peso (kg):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_peso = ttk.Entry(form_frame)
        self.entry_peso.grid(row=0, column=1, padx=5, pady=5)

        # Altura
        ttk.Label(form_frame, text="Altura (m):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_altura = ttk.Entry(form_frame)
        self.entry_altura.grid(row=1, column=1, padx=5, pady=5)

        # Edad
        ttk.Label(form_frame, text="Edad:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_edad = ttk.Entry(form_frame)
        self.entry_edad.grid(row=2, column=1, padx=5, pady=5)

        # Género
        ttk.Label(form_frame, text="Género:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_genero = ttk.Combobox(form_frame, values=["Masculino", "Femenino", "Otro"])
        self.combo_genero.grid(row=3, column=1, padx=5, pady=5)

        # Nivel de actividad física
        ttk.Label(form_frame, text="Nivel de actividad física:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.combo_actividad = ttk.Combobox(form_frame, values=["Bajo", "Moderado", "Alto"])
        self.combo_actividad.grid(row=4, column=1, padx=5, pady=5)

        # Botón para guardar datos y calcular IMC
        btn_guardar = ttk.Button(frame, text="Guardar y Calcular IMC", command=self.guardar_datos)
        btn_guardar.pack(pady=10)

        # Opción para cambiar de tema: claro u oscuro
        self.theme_var = tk.StringVar(value=self.preferences.get("theme", "light"))
        theme_frame = ttk.LabelFrame(frame, text="Tema")
        theme_frame.pack(pady=10, padx=5, fill="x")
        radio_light = ttk.Radiobutton(theme_frame, text="Claro", value="light", variable=self.theme_var, command=self.toggle_theme)
        radio_dark = ttk.Radiobutton(theme_frame, text="Oscuro", value="dark", variable=self.theme_var, command=self.toggle_theme)
        radio_light.pack(side="left", padx=10, pady=5)
        radio_dark.pack(side="left", padx=10, pady=5)

    def toggle_theme(self):
        # Cambia el color de fondo de la aplicación según el tema seleccionado
        theme = self.theme_var.get()
        if theme == "dark":
            self.configure(bg="gray20")
            style = ttk.Style()
            style.theme_use("clam")
            style.configure(".", background="gray20", foreground="white")
        else:
            self.configure(bg="SystemButtonFace")
            style = ttk.Style()
            style.theme_use("default")
        self.preferences["theme"] = theme
        self.save_preferences()

    def guardar_datos(self):
        try:
            peso = float(self.entry_peso.get())
            altura = float(self.entry_altura.get())
            edad = int(self.entry_edad.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para peso, altura y edad.")
            return

        genero = self.combo_genero.get()
        actividad = self.combo_actividad.get()

        # Calcular IMC
        imc = peso / (altura ** 2)
        messagebox.showinfo("IMC Calculado", f"Su IMC es: {imc:.2f}")

        # Agregar registro al historial
        nuevo_registro = {
            "peso": peso,
            "altura": altura,
            "edad": edad,
            "genero": genero,
            "actividad": actividad,
            "imc": imc
        }
        self.history.append(nuevo_registro)
        self.update_historial_tree()

    # ---------------------------
    # Tab 2: Medidor Visual Interactivo
    # ---------------------------
    def create_tab_medidor(self):
        frame = self.tab_medidor
        lbl = ttk.Label(frame, text="Medidor Visual Interactivo", font=("Helvetica", 16))
        lbl.pack(pady=10)

        # Selector de tipo de visualización (ejemplo: medidor, gráfico de barras o radar)
        self.visualizacion_var = tk.StringVar(value="Medidor")
        opciones = ["Medidor", "Gráfico de Barras", "Radar"]
        combo = ttk.Combobox(frame, textvariable=self.visualizacion_var, values=opciones)
        combo.pack(pady=5)

        # Canvas para la visualización
        self.canvas_medidor = tk.Canvas(frame, width=400, height=300, bg="white")
        self.canvas_medidor.pack(pady=10)

        btn_actualizar = ttk.Button(frame, text="Actualizar Medidor", command=self.actualizar_medidor)
        btn_actualizar.pack(pady=5)

    def actualizar_medidor(self):
        # Se basa en el último IMC ingresado y actualiza el Canvas
        if not self.history:
            messagebox.showwarning("Sin datos", "Aún no ha ingresado datos para calcular el IMC.")
            return
        imc = self.history[-1]["imc"]
        self.canvas_medidor.delete("all")
        ancho = 400
        alto = 300
        margin = 20
        # Dibuja un arco semicircular; este es un ejemplo simplificado
        self.canvas_medidor.create_arc(margin, margin, ancho-margin, alto*1.5-margin, start=180, extent=180, style="arc", width=2)
        # Calcular el ángulo según el IMC (suponiendo que IMC máximo se aproxima a 40)
        angulo = 180 - ((imc / 40.0) * 180)
        # Dibujar la aguja del medidor
        x_centro = ancho / 2
        y_centro = alto * 0.75
        longitud = 120
        x_fin = x_centro + longitud * math.cos(math.radians(angulo))
        y_fin = y_centro - longitud * math.sin(math.radians(angulo))
        self.canvas_medidor.create_line(x_centro, y_centro, x_fin, y_fin, width=3, fill="red")
        self.canvas_medidor.create_text(x_centro, alto - 20, text=f"IMC: {imc:.2f}", font=("Helvetica", 14))

    # ---------------------------
    # Tab 3: Análisis de Imagen
    # ---------------------------
    def create_tab_imagen(self):
        frame = self.tab_imagen
        lbl = ttk.Label(frame, text="Análisis de Imagen", font=("Helvetica", 16))
        lbl.pack(pady=10)

        btn_cargar = ttk.Button(frame, text="Cargar Imagen", command=self.cargar_imagen)
        btn_cargar.pack(pady=5)

        self.lbl_imagen = ttk.Label(frame)
        self.lbl_imagen.pack(pady=10)

        self.detected_info = ttk.Label(frame, text="La información del análisis se mostrará aquí.")
        self.detected_info.pack(pady=5)

    def cargar_imagen(self):
        ruta_imagen = filedialog.askopenfilename(title="Seleccione una imagen", 
                                                   filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if ruta_imagen:
            # Cargar la imagen con OpenCV
            imagen_cv = cv2.imread(ruta_imagen)
            if imagen_cv is None:
                messagebox.showerror("Error", "No se pudo abrir la imagen seleccionada.")
                return
            # Convertir la imagen a RGB para usarla con PIL
            imagen_cv = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)
            imagen_pil = Image.fromarray(imagen_cv)
            imagen_pil = imagen_pil.resize((250, 250))
            self.imagen_tk = ImageTk.PhotoImage(imagen_pil)
            self.lbl_imagen.configure(image=self.imagen_tk)

            # Ejemplo de análisis: detección de bordes usando Canny
            imagen_gris = cv2.cvtColor(imagen_cv, cv2.COLOR_RGB2GRAY)
            bordes = cv2.Canny(imagen_gris, 100, 200)
            # Esta parte se puede ampliar para comparar proporciones o detectar la postura
            self.detected_info.configure(text="Se detectaron bordes en la imagen. Ajuste la calibración manualmente si es requerido.")

    # ---------------------------
    # Tab 4: Recomendaciones
    # ---------------------------
    def create_tab_recomendaciones(self):
        frame = self.tab_recomendaciones
        lbl = ttk.Label(frame, text="Recomendaciones Personalizadas", font=("Helvetica", 16))
        lbl.pack(pady=10)

        # Área para mostrar la recomendación
        self.text_recomendaciones = tk.Text(frame, height=10, width=60)
        self.text_recomendaciones.pack(pady=5)
        btn_generar = ttk.Button(frame, text="Generar Recomendación", command=self.generar_recomendacion)
        btn_generar.pack(pady=5)

        # Sección de feedback
        feedback_frame = ttk.LabelFrame(frame, text="Feedback")
        feedback_frame.pack(pady=10)
        ttk.Label(feedback_frame, text="¿Fue útil esta recomendación?").pack(side="left", padx=5)
        self.feedback_var = tk.StringVar(value="No")
        ttk.Radiobutton(feedback_frame, text="Sí", variable=self.feedback_var, value="Sí").pack(side="left", padx=5)
        ttk.Radiobutton(feedback_frame, text="No", variable=self.feedback_var, value="No").pack(side="left", padx=5)

    def generar_recomendacion(self):
        # Genera una recomendación simple basándose en el IMC del último registro
        if not self.history:
            self.text_recomendaciones.delete("1.0", tk.END)
            self.text_recomendaciones.insert(tk.END, "Ingrese sus datos personales en la pestaña 'Datos Personales'.")
            return
        
        ultimo = self.history[-1]
        imc = ultimo["imc"]
        recomendacion = ""
        if imc < 18.5:
            recomendacion = ("Su IMC indica bajo peso. Se recomienda aumentar la ingesta calórica y consultar a un profesional.")
        elif imc < 25:
            recomendacion = ("Su IMC se encuentra en un rango saludable. Mantenga su estilo de vida activo y equilibrado.")
        elif imc < 30:
            recomendacion = ("Su IMC indica sobrepeso. Considere mejorar su dieta y aumentar la actividad física.")
        else:
            recomendacion = ("Su IMC indica obesidad. Es importante consultar a un especialista para una evaluación personalizada.")
        
        self.text_recomendaciones.delete("1.0", tk.END)
        self.text_recomendaciones.insert(tk.END, recomendacion)

    # ---------------------------
    # Tab 5: Historial y Exportación de Datos
    # ---------------------------
    def create_tab_historial(self):
        frame = self.tab_historial
        lbl = ttk.Label(frame, text="Historial de Mediciones", font=("Helvetica", 16))
        lbl.pack(pady=10)

        # Treeview para mostrar el historial
        self.tree = ttk.Treeview(frame, columns=("Peso", "Altura", "Edad", "Género", "Actividad", "IMC"), show="headings")
        for col in ("Peso", "Altura", "Edad", "Género", "Actividad", "IMC"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Botones para exportar los datos
        export_frame = ttk.Frame(frame)
        export_frame.pack(pady=5)
        btn_csv = ttk.Button(export_frame, text="Exportar a CSV", command=self.exportar_csv)
        btn_csv.pack(side="left", padx=5)
        btn_json = ttk.Button(export_frame, text="Exportar a JSON", command=self.exportar_json)
        btn_json.pack(side="left", padx=5)
        btn_pdf = ttk.Button(export_frame, text="Exportar a PDF", command=self.exportar_pdf)
        btn_pdf.pack(side="left", padx=5)

    def update_historial_tree(self):
        # Actualiza el Treeview con los registros del historial
        for row in self.tree.get_children():
            self.tree.delete(row)
        for registro in self.history:
            self.tree.insert("", tk.END, values=(
                registro["peso"],
                registro["altura"],
                registro["edad"],
                registro["genero"],
                registro["actividad"],
                f"{registro['imc']:.2f}"
            ))

    def exportar_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Peso", "Altura", "Edad", "Género", "Actividad", "IMC"])
                    for registro in self.history:
                        writer.writerow([registro["peso"], registro["altura"], registro["edad"],
                                         registro["genero"], registro["actividad"], registro["imc"]])
                messagebox.showinfo("Éxito", "Datos exportados a CSV exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar CSV: {str(e)}")

    def exportar_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    json.dump(self.history, file, indent=4)
                messagebox.showinfo("Éxito", "Datos exportados a JSON exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar JSON: {str(e)}")

    def exportar_pdf(self):
        # La exportación a PDF puede implementarse con librerías adicionales como reportlab
        messagebox.showinfo("Exportar a PDF", "La función de exportación a PDF está en desarrollo.")

if __name__ == "__main__":
    app = HealthCalculator()
    app.mainloop()