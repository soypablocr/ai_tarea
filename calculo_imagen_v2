import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self, master):
        self.master = master
        master.title("Análisis de Proporciones Corporales")

        self.imagen_original = None
        self.imagen_tk = None
        self.proporciones = None
        self.puntos_calibracion = []

        # Frame para la imagen
        self.frame_imagen = tk.LabelFrame(master, text="Imagen de Perfil")
        self.frame_imagen.pack(padx=10, pady=10)

        self.label_imagen = tk.Label(self.frame_imagen)
        self.label_imagen.pack()
        self.label_imagen.bind("<Button-1>", self.seleccionar_punto_calibracion)

        # Frame para los botones
        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack(pady=5)

        self.btn_cargar = tk.Button(self.frame_botones, text="Cargar Imagen", command=self.cargar_imagen)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        self.btn_analizar = tk.Button(self.frame_botones, text="Analizar", command=self.analizar_imagen, state=tk.DISABLED)
        self.btn_analizar.pack(side=tk.LEFT, padx=5)

        self.btn_comparar = tk.Button(self.frame_botones, text="Comparar Promedios", command=self.mostrar_comparacion, state=tk.DISABLED)
        self.btn_comparar.pack(side=tk.LEFT, padx=5)

        self.btn_calibrar = tk.Button(self.frame_botones, text="Calibrar Manualmente", command=self.iniciar_calibracion, state=tk.DISABLED)
        self.btn_calibrar.pack(side=tk.LEFT, padx=5)

        # Frame para información/resultados
        self.frame_resultados = tk.LabelFrame(master, text="Resultados")
        self.frame_resultados.pack(padx=10, pady=10)

        self.label_resultados = tk.Label(self.frame_resultados, text="Carga una imagen para comenzar.")
        self.label_resultados.pack()

    def cargar_imagen(self):
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen de perfil",
                                                filetypes=(("Archivos de imagen", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*")))
        if ruta_imagen:
            try:
                self.imagen_original = cv2.imread(ruta_imagen)
                self.mostrar_imagen(self.imagen_original)
                self.btn_analizar.config(state=tk.NORMAL)
                self.label_resultados.config(text="Imagen cargada.")
                self.proporciones = None
                self.btn_comparar.config(state=tk.DISABLED)
                self.btn_calibrar.config(state=tk.NORMAL)
                self.puntos_calibracion = []
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
                self.imagen_original = None
                self.imagen_tk = None
                self.label_imagen.config(image=None)
                self.btn_analizar.config(state=tk.DISABLED)
                self.btn_comparar.config(state=tk.DISABLED)
                self.btn_calibrar.config(state=tk.DISABLED)
                self.label_resultados.config(text="Error al cargar la imagen.")

    def mostrar_imagen(self, imagen_cv2):
        imagen_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(imagen_rgb)
        self.imagen_tk = ImageTk.PhotoImage(imagen_pil)
        self.label_imagen.config(image=self.imagen_tk)

    def detectar_postura_proporciones(self, imagen):
        """Implementación básica de detección de postura y proporciones (similar a la versión no-GUI)."""
        if imagen is None:
            return None

        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        imagen_con_deteccion = imagen.copy()
        proporciones = None

        if contornos:
            mayor_contorno = max(contornos, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(mayor_contorno)
            cv2.rectangle(imagen_con_deteccion, (x, y), (x + w, y + h), (0, 255, 0), 2)
            proporcion_altura_ancho = h / w if w > 0 else 0
            proporciones = {"altura": h, "ancho": w, "proporcion_altura_ancho": proporcion_altura_ancho}
            self.label_resultados.config(text=f"Proporción estimada altura/ancho: {proporcion_altura_ancho:.2f}")
        else:
            self.label_resultados.config(text="No se detectaron contornos significativos.")

        return imagen_con_deteccion, proporciones

    def analizar_imagen(self):
        if self.imagen_original is not None:
            imagen_con_deteccion, self.proporciones = self.detectar_postura_proporciones(self.imagen_original)
            self.mostrar_imagen(imagen_con_deteccion)
            if self.proporciones:
                self.btn_comparar.config(state=tk.NORMAL)

    def comparar_con_promedios_saludables(self, proporciones):
        """Compara las proporciones con promedios saludables y devuelve la figura de Matplotlib."""
        if proporciones is None:
            return None

        promedio_saludable_altura_ancho = 1.6  # Ejemplo hipotético

        proporcion_detectada = proporciones.get("proporcion_altura_ancho")

        if proporcion_detectada is not None:
            fig, ax = plt.subplots(figsize=(6, 4))
            bar_labels = ['Detectada', 'Saludable']
            bar_values = [proporcion_detectada, promedio_saludable_altura_ancho]
            ax.bar(bar_labels, bar_values, color=['blue', 'green'])
            ax.set_ylabel('Proporción Altura/Ancho')
            ax.set_title('Comparación de Proporciones')
            return fig
        return None

    def mostrar_comparacion(self):
        if self.proporciones:
            fig = self.comparar_con_promedios_saludables(self.proporciones)
            if fig:
                top_level = tk.Toplevel(self.master)
                top_level.title("Comparación con Promedios")
                canvas = FigureCanvasTkAgg(fig, master=top_level)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack()
                canvas.draw()
            else:
                messagebox.showinfo("Información", "No se pudieron comparar las proporciones.")
        else:
            messagebox.showinfo("Información", "Primero debes analizar una imagen.")

    def iniciar_calibracion(self):
        if self.imagen_original is not None:
            self.puntos_calibracion = []
            messagebox.showinfo("Calibración", "Haz clic en puntos clave de la imagen (ej., cabeza, hombros, caderas, pies).")
            self.label_imagen.config(cursor="crosshair")
            self.master.bind("<KeyRelease>", self.finalizar_calibracion)
        else:
            messagebox.showinfo("Advertencia", "Por favor, carga una imagen primero.")

    def seleccionar_punto_calibracion(self, event):
        if self.imagen_original is not None and self.label_imagen.cget("cursor") == "crosshair":
            x, y = event.x, event.y
            self.puntos_calibracion.append((x, y))
            imagen_con_puntos = self.imagen_original.copy()
            for px, py in self.puntos_calibracion:
                cv2.circle(imagen_con_puntos, (px, py), 5, (0, 255, 0), -1)
            self.mostrar_imagen(imagen_con_puntos)

    def finalizar_calibracion(self, event):
        if event.keysym == 'Return' and self.label_imagen.cget("cursor") == "crosshair":
            self.label_imagen.config(cursor="")
            self.master.unbind("<KeyRelease>")
            if self.puntos_calibracion:
                messagebox.showinfo("Calibración", f"Puntos de calibración seleccionados: {self.puntos_calibracion}. La lógica para usar estos puntos aún no está implementada.")
                # Aquí iría la lógica para usar los puntos de calibración
            else:
                messagebox.showinfo("Calibración", "No se seleccionaron puntos de calibración.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    
