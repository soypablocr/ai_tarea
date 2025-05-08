import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mediapipe as mp

mp_pose = mp.solutions.pose

class PostureAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Postura Corporal")
        
        # Variables
        self.image_path = None
        self.landmarks = []
        self.draggable_points = []
        self.calibration_mode = False
        self.healthy_avg = {
            'hombros': 0.25,    # Proporción promedio saludable (25% de la altura)
            'cintura': 0.5,     # 50% de la altura
            'cadera': 0.55      # 55% de la altura
        }
        
        # GUI Elements
        self.create_widgets()
        
    def create_widgets(self):
        # Frame superior para botones
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        
        self.btn_upload = tk.Button(top_frame, text="Cargar Foto", command=self.upload_image)
        self.btn_upload.pack(side=tk.LEFT, padx=5)
        
        self.btn_process = tk.Button(top_frame, text="Analizar Postura", command=self.process_image)
        self.btn_process.pack(side=tk.LEFT, padx=5)
        
        self.btn_calibrate = tk.Button(top_frame, text="Calibrar", command=self.toggle_calibration)
        self.btn_calibrate.pack(side=tk.LEFT, padx=5)
        
        self.btn_compare = tk.Button(top_frame, text="Mostrar Comparación", command=self.show_comparison)
        self.btn_compare.pack(side=tk.LEFT, padx=5)
        
        # Canvas para imagen
        self.canvas = tk.Canvas(self.root, width=600, height=500)
        self.canvas.pack(pady=10)
        
        # Frame para gráfico
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.show_image()
            
    def show_image(self):
        self.img = Image.open(self.image_path)
        self.img = self.img.resize((600, 500), Image.Resampling.LANCZOS)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tkimg)
        
    def process_image(self):
        with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
            image = cv2.imread(self.image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            
            if results.pose_landmarks:
                self.landmarks = self.extract_landmarks(results, image.shape)
                self.draw_landmarks(image)
                self.calculate_proportions()
                
    def extract_landmarks(self, results, img_shape):
        landmarks = []
        for lm in results.pose_landmarks.landmark:
            x = int(lm.x * img_shape[1])
            y = int(lm.y * img_shape[0])
            landmarks.append((x, y))
        return landmarks
    
    def draw_landmarks(self, image):
        h, w = image.shape[:2]
        for point in self.landmarks:
            cv2.circle(image, point, 5, (0,255,0), -1)
        
        # Convertir a formato Tkinter
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(img).resize((600, 500))
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tkimg)
        
    def calculate_proportions(self):
        if len(self.landmarks) >= 25:
            # Calcular proporciones relativas
            altura = self.landmarks[25][1] - self.landmarks[0][1]  # De nariz a tobillo
            hombros = abs(self.landmarks[11][0] - self.landmarks[12][0])
            cintura = abs(self.landmarks[23][1] - self.landmarks[0][1])
            cadera = abs(self.landmarks[24][1] - self.landmarks[0][1])
            
            self.proporciones = {
                'hombros': hombros / altura,
                'cintura': cintura / altura,
                'cadera': cadera / altura
            }
    
    def toggle_calibration(self):
        self.calibration_mode = not self.calibration_mode
        if self.calibration_mode:
            self.enable_calibration()
        else:
            self.disable_calibration()
    
    def enable_calibration(self):
        self.draggable_points = []
        for i, (x, y) in enumerate(self.landmarks):
            point = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='red', tags=f"point_{i}")
            self.draggable_points.append(point)
            self.canvas.tag_bind(point, '<B1-Motion>', lambda e, idx=i: self.drag_point(e, idx))
    
    def drag_point(self, event, idx):
        x, y = event.x, event.y
        self.landmarks[idx] = (x, y)
        self.canvas.coords(self.draggable_points[idx], x-5, y-5, x+5, y+5)
        self.calculate_proportions()
    
    def disable_calibration(self):
        for point in self.draggable_points:
            self.canvas.delete(point)
        self.draggable_points = []
        self.draw_landmarks(cv2.imread(self.image_path))
    
    def show_comparison(self):
        if hasattr(self, 'proporciones'):
            # Crear gráfico comparativo
            fig = plt.figure(figsize=(8,4))
            categories = list(self.proporciones.keys())
            user_values = [self.proporciones[c] for c in categories]
            avg_values = [self.healthy_avg[c] for c in categories]
            
            x = np.arange(len(categories))
            bar_width = 0.35
            
            plt.bar(x - bar_width/2, user_values, bar_width, label='Usuario')
            plt.bar(x + bar_width/2, avg_values, bar_width, label='Promedio Saludable')
            
            plt.xticks(x, categories)
            plt.ylabel('Proporciones')
            plt.title('Comparación con Promedios Saludables')
            plt.legend()
            
            # Mostrar en Tkinter
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = PostureAnalyzerApp(root)
    root.mainloop()
