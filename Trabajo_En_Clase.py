import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
import math
import numpy as np
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Wedge
from fpdf import FPDF

class CalculadoraSaludApp:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Calculadora Inteligente de Salud")
        self.raiz.geometry("1100x750")
        
        self.cargar_configuracion()
        
        # Variables de datos del usuario
        self.peso = tk.DoubleVar(value=70.0)
        self.altura = tk.DoubleVar(value=1.75)
        self.edad = tk.IntVar(value=30)
        self.genero = tk.StringVar(value="Masculino")
        self.nivel_actividad = tk.StringVar(value="Moderado")
        
        # Historial de mediciones
        self.historial = []
        self.cargar_historial()
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz: pestañas, marcos y barra de menú
        self.crear_marco_principal()
        self.crear_pestanas()
        self.crear_pestana_datos_basicos()
        self.crear_pestana_analisis()
        self.crear_pestana_historial()
        self.crear_pestana_perfil()
        self.crear_pestana_recomendaciones()
        self.crear_pestana_configuracion()
        self.crear_barra_menu()
        
        # Actualizar tema inicial
        self.actualizar_tema()
    
    def cargar_configuracion(self):
        """Cargar configuración guardada o usar valores por defecto."""
        self.configuracion = {
            "tema": "light",
            "tamano_fuente": 12,
            "fuente": "Segoe UI",
            "velocidad_animacion": 0.5,
            "archivos_recientes": []
        }
        try:
            if os.path.exists("health_calc_config.json"):
                with open("health_calc_config.json", "r") as f:
                    self.configuracion.update(json.load(f))
        except Exception as e:
            print(f"Error cargando configuración: {e}")
    
    def guardar_configuracion(self):
        """Guardar configuración del usuario."""
        try:
            with open("health_calc_config.json", "w") as f:
                json.dump(self.configuracion, f, indent=4)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def configurar_estilo(self):
        """Configurar estilos para la aplicación."""
        self.estilo = ttk.Style()
        # Tema claro
        self.estilo.theme_create("light", parent="clam", settings={
            "TFrame": {"configure": {"background": "#f0f0f0"}},
            "TLabel": {"configure": {"background": "#f0f0f0", "foreground": "#333333",
                                      "font": (self.configuracion["fuente"], self.configuracion["tamano_fuente"])}},
            "TButton": {"configure": {"background": "#e1e1e1", "foreground": "#333333",
                                       "font": (self.configuracion["fuente"], self.configuracion["tamano_fuente"])}},
            "TNotebook": {"configure": {"background": "#f0f0f0"}},
            "TNotebook.Tab": {
                "configure": {"padding": [10, 5], "background": "#d0d0d0",
                              "font": (self.configuracion["fuente"], self.configuracion["tamano_fuente"])},
                "map": {"background": [("selected", "#f0f0f0")],
                        "expand": [("selected", [1, 1, 1, 0])]}
            }
        })
        # Tema oscuro
        self.estilo.theme_create("dark", parent="light", settings={
            "TFrame": {"configure": {"background": "#2d2d2d"}},
            "TLabel": {"configure": {"background": "#2d2d2d", "foreground": "#e0e0e0"}},
            "TButton": {"configure": {"background": "#3d3d3d", "foreground": "#e0e0e0"}},
            "TNotebook": {"configure": {"background": "#2d2d2d"}},
            "TNotebook.Tab": {
                "configure": {"background": "#1d1d1d"},
                "map": {"background": [("selected", "#2d2d2d")],
                        "expand": [("selected", [1, 1, 1, 0])]}
            }
        })
        self.estilo.theme_use("light" if self.configuracion["tema"] == "light" else "dark")
    
    def crear_marco_principal(self):
        """Crear el marco principal de la aplicación."""
        self.marco_principal = ttk.Frame(self.raiz)
        self.marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def crear_pestanas(self):
        """Crear el sistema de pestañas."""
        self.notebook = ttk.Notebook(self.marco_principal)
        self.pestana_datos_basicos = ttk.Frame(self.notebook)
        self.pestana_analisis = ttk.Frame(self.notebook)
        self.pestana_historial = ttk.Frame(self.notebook)
        self.pestana_perfil = ttk.Frame(self.notebook)
        self.pestana_recomendaciones = ttk.Frame(self.notebook)
        self.pestana_configuracion = ttk.Frame(self.notebook)
        
        self.notebook.add(self.pestana_datos_basicos, text="Datos Basicos")
        self.notebook.add(self.pestana_analisis, text="Analisis de Salud")
        self.notebook.add(self.pestana_historial, text="Historial")
        self.notebook.add(self.pestana_perfil, text="Análisis Foto")
        self.notebook.add(self.pestana_recomendaciones, text="Recomendaciones")
        self.notebook.add(self.pestana_configuracion, text="Configuracion")
        self.notebook.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestana_datos_basicos(self):
        """Crear la pestaña de datos básicos."""
        marco_entrada = ttk.Frame(self.pestana_datos_basicos)
        marco_entrada.pack(pady=20, padx=20, fill=tk.X)
        
        ttk.Label(marco_entrada, text="Peso (kg):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(marco_entrada, textvariable=self.peso).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(marco_entrada, text="Altura (m):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(marco_entrada, textvariable=self.altura).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(marco_entrada, text="Edad:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(marco_entrada, textvariable=self.edad).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(marco_entrada, text="Genero:").grid(row=3, column=0, sticky=tk.W)
        ttk.Combobox(marco_entrada, textvariable=self.genero,
                     values=["Masculino", "Femenino", "Otro"]).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(marco_entrada, text="Nivel de actividad:").grid(row=4, column=0, sticky=tk.W)
        ttk.Combobox(marco_entrada, textvariable=self.nivel_actividad,
                     values=["Sedentario", "Ligero", "Moderado", "Intenso", "Muy intenso"]).grid(row=4, column=1, sticky=tk.W)
        
        ttk.Button(self.pestana_datos_basicos, text="Calcular IMC y Metabolismo", command=self.calcular_salud).pack(pady=20)
        
        self.marco_resultados = ttk.Frame(self.pestana_datos_basicos)
        self.marco_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        marco_entrada.columnconfigure(1, weight=1)
    
    def crear_pestana_analisis(self):
        """Crear la pestaña de análisis visual con múltiples gráficos."""
        self.tipo_grafico = tk.StringVar(value="barras")
        marco_tipo = ttk.LabelFrame(self.pestana_analisis, text="Tipo de Grafico")
        marco_tipo.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Radiobutton(marco_tipo, text="Barras", variable=self.tipo_grafico,
                        value="barras", command=self.actualizar_grafico).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(marco_tipo, text="Radar", variable=self.tipo_grafico,
                        value="radar", command=self.actualizar_grafico).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(marco_tipo, text="Medidor", variable=self.tipo_grafico,
                        value="medidor", command=self.actualizar_grafico).pack(side=tk.LEFT, padx=5)
        
        self.marco_grafico = ttk.Frame(self.pestana_analisis)
        self.marco_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.figura = plt.Figure(figsize=(7, 5), dpi=100)
        # Renombramos la instancia del canvas de Matplotlib a self.canvas_fig
        self.canvas_fig = FigureCanvasTkAgg(self.figura, master=self.marco_grafico)
        self.canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.actualizar_grafico()
    
    def crear_pestana_historial(self):
        """Crear la pestaña de historial de mediciones."""
        self.arbol_historial = ttk.Treeview(self.pestana_historial,
                                            columns=("Fecha", "Peso", "Altura", "IMC", "Metabolismo", "Calorias"))
        self.arbol_historial.heading("#0", text="ID")
        self.arbol_historial.heading("Fecha", text="Fecha")
        self.arbol_historial.heading("Peso", text="Peso (kg)")
        self.arbol_historial.heading("Altura", text="Altura (m)")
        self.arbol_historial.heading("IMC", text="IMC")
        self.arbol_historial.heading("Metabolismo", text="Metabolismo")
        self.arbol_historial.heading("Calorias", text="Calorias")
        self.arbol_historial.column("#0", width=50)
        self.arbol_historial.column("Fecha", width=150)
        self.arbol_historial.column("Peso", width=80)
        self.arbol_historial.column("Altura", width=80)
        self.arbol_historial.column("IMC", width=80)
        self.arbol_historial.column("Metabolismo", width=100)
        self.arbol_historial.column("Calorias", width=100)
        self.arbol_historial.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        marco_export = ttk.Frame(self.pestana_historial)
        marco_export.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(marco_export, text="Exportar a CSV", command=self.exportar_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_export, text="Exportar a JSON", command=self.exportar_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_export, text="Exportar a PDF", command=self.exportar_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_export, text="Borrar Historial", command=self.borrar_historial).pack(side=tk.LEFT, padx=5)
        self.actualizar_arbol_historial()
    def crear_pestana_configuracion(self):
        """Crear la pestana de configuracion"""
        # Configuracion de tema
        marco_tema = ttk.LabelFrame(self.pestana_configuracion, text="Tema")
        marco_tema.pack(fill=tk.X, padx=20, pady=10)
        self.var_tema = tk.StringVar(value=self.configuracion["tema"])
        ttk.Radiobutton(marco_tema, text="Modo Claro", variable=self.var_tema,
                        value="light", command=self.actualizar_tema).pack(anchor=tk.W)
        ttk.Radiobutton(marco_tema, text="Modo Oscuro", variable=self.var_tema,
                        value="dark", command=self.actualizar_tema).pack(anchor=tk.W)
        # Configuracion de fuente
        marco_fuente = ttk.LabelFrame(self.pestana_configuracion, text="Fuente")
        marco_fuente.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(marco_fuente, text="Tamano de fuente:").pack(anchor=tk.W)
        self.var_tamano = tk.IntVar(value=self.configuracion["tamano_fuente"])
        ttk.Scale(marco_fuente, from_=8, to=20, variable=self.var_tamano,
                  command=lambda v: self.actualizar_tamano(int(float(v)))).pack(fill=tk.X)
        # Animaciones
        marco_anim = ttk.LabelFrame(self.pestana_configuracion, text="Animaciones")
        marco_anim.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(marco_anim, text="Velocidad de transicion:").pack(anchor=tk.W)
        self.var_velocidad = tk.DoubleVar(value=self.configuracion["velocidad_animacion"])
        ttk.Scale(marco_anim, from_=0.1, to=2.0, variable=self.var_velocidad,
                  command=lambda v: self.actualizar_velocidad(float(v))).pack(fill=tk.X)
        # Boton para guardar configuraciones
        ttk.Button(self.pestana_configuracion, text="Guardar Configuraciones", command=self.guardar_configuraciones).pack(pady=20)
    def crear_pestana_perfil(self):
        """Crear la pestaña de perfil y detección de postura."""
        frame_foto = ttk.Frame(self.pestana_perfil)
        frame_foto.pack(pady=10, padx=10, fill=tk.X)
        ttk.Button(frame_foto, text="Cargar Foto de Perfil", command=self.cargar_foto_perfil).pack(side=tk.LEFT)
        self.label_imagen_perfil = ttk.Label(frame_foto, text="No hay imagen cargada")
        self.label_imagen_perfil.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(self.pestana_perfil, text="Detectar Postura y Proporciones", command=self.detectar_postura).pack(pady=10)
        
        frame_calibracion = ttk.LabelFrame(self.pestana_perfil, text="Calibracion Manual")
        frame_calibracion.pack(pady=10, padx=10, fill=tk.X)
        self.var_cabeza = tk.DoubleVar(value=0.15)
        self.var_torso = tk.DoubleVar(value=0.40)
        self.var_piernas = tk.DoubleVar(value=0.45)
        ttk.Label(frame_calibracion, text="Proporcion Cabeza:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Scale(frame_calibracion, variable=self.var_cabeza, from_=0.0, to=1.0, resolution=0.01, 
                 orient=tk.HORIZONTAL, command=lambda v: self.actualizar_visualizacion_perfil()).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(frame_calibracion, text="Proporcion Torso:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Scale(frame_calibracion, variable=self.var_torso, from_=0.0, to=1.0, resolution=0.01, 
                 orient=tk.HORIZONTAL, command=lambda v: self.actualizar_visualizacion_perfil()).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Label(frame_calibracion, text="Proporcion Piernas:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Scale(frame_calibracion, variable=self.var_piernas, from_=0.0, to=1.0, resolution=0.01, 
                 orient=tk.HORIZONTAL, command=lambda v: self.actualizar_visualizacion_perfil()).grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        frame_calibracion.columnconfigure(1, weight=1)
        
        frame_visualizacion = ttk.Frame(self.pestana_perfil)
        frame_visualizacion.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.figura_perfil = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas_perfil = FigureCanvasTkAgg(self.figura_perfil, master=frame_visualizacion)
        self.canvas_perfil.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.actualizar_visualizacion_perfil()
    
    def cargar_foto_perfil(self):
        """Permite al usuario cargar una foto de perfil."""
        ruta_imagen = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg *.jpeg *.png *.bmp")])
        if ruta_imagen:
            try:
                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize((200, 200))
                self.imagen_perfil = ImageTk.PhotoImage(imagen)
                self.label_imagen_perfil.config(image=self.imagen_perfil, text="")
                self.imagen_original = imagen.copy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la imagen: {e}")
    
    def detectar_postura(self):
        """Simular detección de postura y estimación de proporciones."""
        if not hasattr(self, "imagen_original"):
            messagebox.showwarning("Advertencia", "Primero carga una imagen de perfil.")
            return
        # Algoritmo simulado: se asignan proporciones predeterminadas.
        self.var_cabeza.set(0.15)
        self.var_torso.set(0.40)
        self.var_piernas.set(0.45)
        messagebox.showinfo("Deteccion", "Postura detectada. Puedes ajustar manualmente si es necesario.")
        self.actualizar_visualizacion_perfil()
    
    def actualizar_visualizacion_perfil(self):
        """Actualiza la visualización comparativa de las proporciones detectadas versus promedios saludables."""
        cabeza = self.var_cabeza.get()
        torso = self.var_torso.get()
        piernas = self.var_piernas.get()
        promedios_saludables = {"Cabeza": 0.15, "Torso": 0.40, "Piernas": 0.45}
        detectados = {"Cabeza": cabeza, "Torso": torso, "Piernas": piernas}
        self.figura_perfil.clear()
        ax = self.figura_perfil.add_subplot(111)
        categorias = list(promedios_saludables.keys())
        valores_saludables = [promedios_saludables[k] for k in categorias]
        valores_detectados = [detectados[k] for k in categorias]
        x = np.arange(len(categorias))
        ancho = 0.35
        ax.bar(x - ancho/2, valores_saludables, ancho, label="Saludable", color="green", alpha=0.6)
        ax.bar(x + ancho/2, valores_detectados, ancho, label="Detectado", color="blue", alpha=0.6)
        ax.set_xticks(x)
        ax.set_xticklabels(categorias)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Proporción")
        ax.set_title("Comparación de Proporciones Corporales")
        ax.legend()
        self.canvas_perfil.draw()
    
    def crear_pestana_recomendaciones(self):
        """Crear la pestaña de recomendaciones personalizadas."""
        frame = self.pestana_recomendaciones
        lbl = ttk.Label(frame, text="Recomendaciones Personalizadas", font=("Helvetica", 16))
        lbl.pack(pady=10)
        
        self.text_recomendaciones = tk.Text(frame, height=10, width=60)
        self.text_recomendaciones.pack(pady=5)
        
        btn_generar = ttk.Button(frame, text="Generar Recomendación", command=self.generar_recomendacion)
        btn_generar.pack(pady=5)
        
        feedback_frame = ttk.LabelFrame(frame, text="Feedback")
        feedback_frame.pack(pady=10)
        ttk.Label(feedback_frame, text="¿Fue útil esta recomendación?").pack(side="left", padx=5)
        self.feedback_var = tk.StringVar(value="No")
        ttk.Radiobutton(feedback_frame, text="Sí", variable=self.feedback_var, value="Sí").pack(side="left", padx=5)
        ttk.Radiobutton(feedback_frame, text="No", variable=self.feedback_var, value="No").pack(side="left", padx=5)
    
    def generar_recomendacion(self):
        """Generar recomendación basada en el IMC del último registro del historial."""
        if not self.historial:
            self.text_recomendaciones.delete("1.0", tk.END)
            self.text_recomendaciones.insert(tk.END, "Ingrese sus datos personales primero.")
            return
        
        ultimo = self.historial[-1]
        imc = ultimo.get("imc", 0)
        edad = ultimo.get("edad", 0)
        genero = ultimo.get("genero", "")
        actividad = ultimo.get("actividad", "")
        
        recomendacion = ""
        if imc < 18.5:
            recomendacion = (
                f"Su IMC de {imc:.2f} indica bajo peso.\n"
                "Recomendaciones:\n"
                "- Consuma alimentos ricos en nutrientes y calorías.\n"
                "- Realice ejercicios de fuerza para ganar masa muscular.\n"
                "- Consulte a un nutricionista para un plan personalizado.\n"
            )
        elif imc < 25:
            recomendacion = (
                f"Su IMC de {imc:.2f} se encuentra en un rango saludable.\n"
                "Recomendaciones:\n"
                "- Mantenga una dieta balanceada.\n"
                "- Continúe con su nivel de actividad física actual.\n"
                "- Realice chequeos médicos periódicos.\n"
            )
        elif imc < 30:
            recomendacion = (
                f"Su IMC de {imc:.2f} indica sobrepeso.\n"
                "Recomendaciones:\n"
                "- Reduzca el consumo de alimentos procesados y azúcares.\n"
                "- Aumente su actividad física gradualmente.\n"
                "- Consuma más frutas, verduras y proteínas magras.\n"
            )
        else:
            recomendacion = (
                f"Su IMC de {imc:.2f} indica obesidad.\n"
                "Recomendaciones:\n"
                "- Es importante consultar a un médico para evaluación.\n"
                "- Considere un plan de alimentación supervisado.\n"
                "- Incorpore ejercicio regular adaptado a sus capacidades.\n"
            )
        if edad > 50:
            recomendacion += "\nPara su edad:\n- Realice ejercicios de bajo impacto.\n- Asegure suficiente ingesta de calcio y vitamina D.\n"
        if genero == "Femenino" and edad > 40:
            recomendacion += "\nAdicionalmente:\n- Considere exámenes de densidad ósea periódicos.\n"
        if actividad == "Sedentario":
            recomendacion += "\nDebido a su bajo nivel de actividad:\n- Comience con caminatas diarias de 15-30 minutos.\n"
        
        self.text_recomendaciones.delete("1.0", tk.END)
        self.text_recomendaciones.insert(tk.END, recomendacion)
    
    def calcular_salud(self):
        """Calcular IMC y metabolismo basal."""
        try:
            peso_val = self.peso.get()
            altura_val = self.altura.get()
            edad_val = self.edad.get()
            genero_val = self.genero.get()
            actividad_val = self.nivel_actividad.get()
            imc = peso_val / (altura_val ** 2)
            if genero_val == "Masculino":
                bmr = 88.362 + (13.397 * peso_val) + (4.799 * altura_val * 100) - (5.677 * edad_val)
            else:
                bmr = 447.593 + (9.247 * peso_val) + (3.098 * altura_val * 100) - (4.330 * edad_val)
            factores_actividad = {
                "Sedentario": 1.2,
                "Ligero": 1.375,
                "Moderado": 1.55,
                "Intenso": 1.725,
                "Muy intenso": 1.9
            }
            calorias = bmr * factores_actividad.get(actividad_val, 1.2)
            self.mostrar_resultados(imc, bmr, calorias)
            self.actualizar_grafico()
            self.agregar_al_historial(imc, bmr, calorias)
        except Exception as e:
            messagebox.showerror("Error", f"Error en los cálculos: {str(e)}")
    
    def mostrar_resultados(self, imc, bmr, calorias):
        """Mostrar resultados en el marco de resultados."""
        for widget in self.marco_resultados.winfo_children():
            widget.destroy()
        if imc < 18.5:
            clasificacion_imc = "Bajo peso"
            color = "blue"
        elif 18.5 <= imc < 25:
            clasificacion_imc = "Peso normal"
            color = "green"
        elif 25 <= imc < 30:
            clasificacion_imc = "Sobrepeso"
            color = "orange"
        else:
            clasificacion_imc = "Obesidad"
            color = "red"
        ttk.Label(self.marco_resultados, text="Resultados de Salud", 
                  font=(self.configuracion["fuente"], self.configuracion["tamano_fuente"] + 2, "bold")
                  ).pack(anchor=tk.W, pady=5)
        resultados = [
            f"IMC: {imc:.1f} ({clasificacion_imc})",
            f"Metabolismo basal: {bmr:.0f} kcal/dia",
            f"Gasto calórico diario: {calorias:.0f} kcal/dia"
        ]
        for res in resultados:
            etiqueta = ttk.Label(self.marco_resultados, text=res)
            if "IMC" in res:
                etiqueta.config(foreground=color)
            etiqueta.pack(anchor=tk.W, pady=5)
    
    def actualizar_grafico(self):
        """Actualizar el gráfico según el tipo seleccionado."""
        if not self.historial:
            return
        ultima_entrada = self.historial[-1]
        tipo = self.tipo_grafico.get()
        self.figura.clear()
        if tipo == "barras":
            self.crear_grafico_barras(ultima_entrada)
        elif tipo == "radar":
            self.crear_grafico_radar(ultima_entrada)
        elif tipo == "medidor":
            self.crear_grafico_medidor(ultima_entrada)
        self.canvas_fig.draw()
    
    def crear_grafico_barras(self, datos):
        """Crear gráfico de barras comparativo."""
        ax = self.figura.add_subplot(111)
        categorias = ['IMC', 'Metabolismo', 'Calorias']
        imc_val = datos.get('imc', 0)
        bmr_val = datos.get('bmr', 0)
        calorias_val = datos.get('calorias', 0)
        valores_usuario = [imc_val, bmr_val, calorias_val]
        rangos_saludables = {
            'IMC': (18.5, 24.9),
            'Metabolismo': (1500, 2500),
            'Calorias': (1800, 3000)
        }
        x = np.arange(len(categorias))
        ancho = 0.35
        barras = ax.bar(x, valores_usuario, ancho, color='skyblue', label='Tus valores')
        for i, categoria in enumerate(categorias):
            bajo, alto = rangos_saludables[categoria]
            ax.plot([i - ancho/2, i + ancho/2], [bajo, bajo], 'r--', linewidth=1)
            ax.plot([i - ancho/2, i + ancho/2], [alto, alto], 'r--', linewidth=1)
            ax.fill_between([i - ancho/2, i + ancho/2], bajo, alto, color='red', alpha=0.1)
        ax.set_xticks(x)
        ax.set_xticklabels(categorias)
        ax.set_title('Comparación con Rangos Saludables')
        ax.legend([barras, ax.lines[0]], ['Tus valores', 'Rango saludable'])
        ax.grid(True, linestyle='--', alpha=0.6)
    
    def crear_grafico_radar(self, datos):
        """Crear gráfico radar de métricas de salud."""
        ax = self.figura.add_subplot(111, polar=True)
        categorias = ['IMC', 'Metabolismo', 'Calorias', 'Edad', 'Peso']
        imc_val = datos.get('imc', 0)
        bmr_val = datos.get('bmr', 0)
        calorias_val = datos.get('calorias', 0)
        edad_val = datos.get('edad', 0)
        peso_val = datos.get('peso', 0)
        valores = [
            min(imc_val / 40 * 100, 100),
            min(bmr_val / 3000 * 100, 100),
            min(calorias_val / 4000 * 100, 100),
            min(edad_val / 100 * 100, 100),
            min(peso_val / 150 * 100, 100)
        ]
        valores += valores[:1]
        angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
        angulos += angulos[:1]
        ax.plot(angulos, valores, 'o-', linewidth=2, label='Tus valores')
        ax.fill(angulos, valores, alpha=0.25)
        ax.plot(angulos, [50] * len(angulos), 'k--', alpha=0.5, label='Promedio')
        ax.set_thetagrids(np.degrees(angulos[:-1]), categorias)
        ax.set_yticklabels([])
        ax.set_title('Análisis Radial de Salud', pad=20)
        ax.legend(loc='upper right')
        ax.grid(True)
    
    def crear_grafico_medidor(self, datos):
        """Crear medidor semicircular para IMC."""
        ax = self.figura.add_subplot(111)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-0.1, 1.1)
        ax.axis('off')
        imc = datos.get('imc', 0)
        min_val, max_val = 15, 40
        zonas = [
            (15, 18.5, "Bajo peso", "lightblue"),
            (18.5, 25, "Normal", "lightgreen"),
            (25, 30, "Sobrepeso", "orange"),
            (30, 40, "Obesidad", "red")
        ]
        for inicio, fin, etiqueta_texto, color in zonas:
            angulo_inicio = 180 * (inicio - min_val) / (max_val - min_val)
            angulo_fin = 180 * (fin - min_val) / (max_val - min_val)
            sector = Wedge((0, 0), 1, angulo_inicio, angulo_fin, width=0.3, color=color, alpha=0.5)
            ax.add_patch(sector)
            angulo_medio = (angulo_inicio + angulo_fin) / 2
            rad = 0.7
            x = rad * math.cos(math.radians(angulo_medio))
            y = rad * math.sin(math.radians(angulo_medio))
            ax.text(x, y, etiqueta_texto, ha='center', va='center', rotation=angulo_medio-90, fontsize=8)
        for valor in np.linspace(min_val, max_val, 6):
            angulo = 180 * (valor - min_val) / (max_val - min_val)
            x_in = 0.7 * math.cos(math.radians(angulo))
            y_in = 0.7 * math.sin(math.radians(angulo))
            x_out = 0.8 * math.cos(math.radians(angulo))
            y_out = 0.8 * math.sin(math.radians(angulo))
            ax.plot([x_in, x_out], [y_in, y_out], 'k-')
            ax.text(x_out * 1.1, y_out * 1.1, f"{valor:.0f}", ha='center', va='center', fontsize=8)
        angulo_aguja = 180 * (imc - min_val) / (max_val - min_val)
        x_aguja = 0.9 * math.cos(math.radians(angulo_aguja))
        y_aguja = 0.9 * math.sin(math.radians(angulo_aguja))
        ax.plot([0, x_aguja], [0, y_aguja], 'r-', linewidth=2)
        ax.plot(x_aguja, y_aguja, 'ro', markersize=8)
        ax.text(0, -0.1, f"IMC: {imc:.1f}", ha='center', va='center', fontsize=12, weight='bold')
        if imc < 18.5:
            estado = "Bajo peso"
        elif imc < 25:
            estado = "Normal"
        elif imc < 30:
            estado = "Sobrepeso"
        else:
            estado = "Obesidad"
        ax.text(0, -0.2, f"Clasificación: {estado}", ha='center', va='center', fontsize=10)
    
    def agregar_al_historial(self, imc, bmr, calorias):
        """Agregar una nueva entrada al historial."""
        entrada = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "peso": self.peso.get(),
            "altura": self.altura.get(),
            "edad": self.edad.get(),
            "genero": self.genero.get(),
            "actividad": self.nivel_actividad.get(),
            "imc": imc,
            "bmr": bmr,
            "calorias": calorias
        }
        self.historial.append(entrada)
        self.guardar_historial()
        self.actualizar_arbol_historial()
    
    def actualizar_arbol_historial(self):
        """Actualizar el Treeview con los datos del historial."""
        for item in self.arbol_historial.get_children():
            self.arbol_historial.delete(item)
        for i, entrada in enumerate(self.historial):
            fecha = entrada.get("fecha", "Sin Fecha")
            peso = entrada.get("peso", 0)
            altura = entrada.get("altura", 0)
            imc = entrada.get("imc", 0)
            bmr = entrada.get("bmr", 0)
            calorias = entrada.get("calorias", 0)
            self.arbol_historial.insert("", "end", text=str(i + 1), values=(
                fecha,
                peso,
                altura,
                f"{imc:.2f}",
                f"{bmr:.0f}",
                f"{calorias:.0f}"
            ))
    
    def cargar_historial(self):
        """Cargar historial desde archivo."""
        try:
            if os.path.exists("health_history.json"):
                with open("health_history.json", "r") as f:
                    self.historial = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial: {str(e)}")
    
    def guardar_historial(self):
        """Guardar historial en archivo."""
        try:
            with open("health_history.json", "w") as f:
                json.dump(self.historial, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el historial: {str(e)}")
    
    def borrar_historial(self):
        """Borrar todo el historial."""
        if messagebox.askyesno("Confirmar", "¿Estas seguro de borrar todo el historial?"):
            self.historial = []
            self.guardar_historial()
            self.actualizar_arbol_historial()
    
    def exportar_csv(self):
        """Exportar historial a archivo CSV."""
        ruta_archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        if ruta_archivo:
            try:
                with open(ruta_archivo, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Fecha", "Peso (kg)", "Altura (m)", "Edad", "Genero", "Actividad", "IMC", "Metabolismo", "Calorias"])
                    for entrada in self.historial:
                        writer.writerow([
                            entrada.get("fecha", "Sin Fecha"),
                            entrada.get("peso", 0),
                            entrada.get("altura", 0),
                            entrada.get("edad", 0),
                            entrada.get("genero", ""),
                            entrada.get("actividad", ""),
                            entrada.get("imc", 0),
                            entrada.get("bmr", 0),
                            entrada.get("calorias", 0)
                        ])
                messagebox.showinfo("Exito", "Historial exportado a CSV correctamente!")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar a CSV: {str(e)}")
    
    def exportar_json(self):
        """Exportar historial a archivo JSON."""
        ruta_archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if ruta_archivo:
            try:
                with open(ruta_archivo, "w") as f:
                    json.dump(self.historial, f, indent=4)
                messagebox.showinfo("Exito", "Historial exportado a JSON correctamente!")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar a JSON: {str(e)}")
    
    def exportar_pdf(self):
        """Exportar historial a archivo PDF."""
        ruta_archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if ruta_archivo:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Historial de Salud", ln=1, align="C")
                pdf.ln(10)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(40, 10, "Fecha", 1)
                pdf.cell(20, 10, "Peso", 1)
                pdf.cell(20, 10, "Altura", 1)
                pdf.cell(15, 10, "IMC", 1)
                pdf.cell(30, 10, "Metabolismo", 1)
                pdf.cell(25, 10, "Calorias", 1)
                pdf.ln()
                pdf.set_font("Arial", size=10)
                for entrada in self.historial:
                    pdf.cell(40, 10, entrada.get("fecha", "Sin Fecha"), 1)
                    pdf.cell(20, 10, str(entrada.get("peso", 0)), 1)
                    pdf.cell(20, 10, str(entrada.get("altura", 0)), 1)
                    pdf.cell(15, 10, f"{entrada.get('imc', 0):.2f}", 1)
                    pdf.cell(30, 10, f"{entrada.get('bmr', 0):.0f}", 1)
                    pdf.cell(25, 10, f"{entrada.get('calorias', 0):.0f}", 1)
                    pdf.ln()
                pdf.output(ruta_archivo)
                messagebox.showinfo("Exito", "Historial exportado a PDF correctamente!")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar a PDF: {str(e)}")
    
    def actualizar_tema(self):
        """Actualizar el tema de la aplicación."""
        tema = self.var_tema.get()
        self.estilo.theme_use("light" if tema == "light" else "dark")
        if tema == "dark":
            plt.style.use('dark_background')
            if hasattr(self, 'figura'):
                self.figura.patch.set_facecolor('#2d2d2d')
        else:
            plt.style.use('default')
            if hasattr(self, 'figura'):
                self.figura.patch.set_facecolor('#f0f0f0')
        # Actualizamos el canvas de la gráfica (self.canvas_fig es FigureCanvasTkAgg)
        if hasattr(self, 'canvas_fig'):
            self.canvas_fig.draw()
    
    def actualizar_tamano(self, tamano):
        """Actualizar tamaño de fuente."""
        self.configuracion["tamano_fuente"] = tamano
        self.estilo.configure("TLabel", font=(self.configuracion["fuente"], tamano))
        self.estilo.configure("TButton", font=(self.configuracion["fuente"], tamano))
        self.estilo.configure("TNotebook.Tab", font=(self.configuracion["fuente"], tamano))
    
    def actualizar_velocidad(self, velocidad):
        """Actualizar velocidad de animación."""
        self.configuracion["velocidad_animacion"] = velocidad
    
    def guardar_configuraciones(self):
        """Guardar configuraciones del usuario."""
        self.configuracion.update({
            "tema": self.var_tema.get(),
            "tamano_fuente": self.var_tamano.get(),
            "velocidad_animacion": self.var_velocidad.get()
        })
        self.guardar_configuracion()
        messagebox.showinfo("Configuracion", "Preferencias guardadas exitosamente!")
    
    def guardar_datos(self):
        """Guardar datos del usuario."""
        datos = {
            "peso": self.peso.get(),
            "altura": self.altura.get(),
            "edad": self.edad.get(),
            "genero": self.genero.get(),
            "nivel_actividad": self.nivel_actividad.get()
        }
        try:
            with open("health_data.json", "w") as f:
                json.dump(datos, f, indent=4)
            messagebox.showinfo("Guardar", "Datos guardados exitosamente!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    
    def cargar_datos(self):
        """Cargar datos del usuario."""
        try:
            with open("health_data.json", "r") as f:
                datos = json.load(f)
            self.peso.set(datos.get("peso", 70.0))
            self.altura.set(datos.get("altura", 1.75))
            self.edad.set(datos.get("edad", 30))
            self.genero.set(datos.get("genero", "Masculino"))
            self.nivel_actividad.set(datos.get("nivel_actividad", "Moderado"))
            messagebox.showinfo("Cargar", "Datos cargados exitosamente!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró archivo de datos")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {str(e)}")
    
    def mostrar_acerca(self):
        """Mostrar información acerca de la aplicación."""
        texto_acerca = (
            "Calculadora Inteligente de Salud\n"
            "Version 1.0\n\n"
            "Caracteristicas:\n"
            "- Calculo de IMC y metabolismo basal\n"
            "- Multiples visualizaciones de datos\n"
            "- Historial completo de mediciones\n"
            "- Exportacion a PDF, CSV y JSON\n"
            "- Personalizacion de interfaz\n"
            "- Deteccion de postura y estimacion de proporciones (Perfil)\n\n"
            "@ 2025"
        )
        messagebox.showinfo("Acerca de", texto_acerca)
    
    def crear_barra_menu(self):
        """Crear la barra de menú."""
        barra_menu = tk.Menu(self.raiz)
        # Menú Archivo
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Guardar datos", command=self.guardar_datos)
        menu_archivo.add_command(label="Cargar datos", command=self.cargar_datos)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.raiz.quit)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        # Menú Ayuda
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        self.raiz.config(menu=barra_menu)

if __name__ == "__main__":
    raiz = tk.Tk()
    app = CalculadoraSaludApp(raiz)
    raiz.mainloop()
