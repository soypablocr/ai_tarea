import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import mediapipe as mp
from PIL import Image, ImageTk
import os

# Inicializar MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# Proporciones corporales saludables promedio
HEALTHY_PROPORTIONS = {
    'head_to_body': 1/7.5,
    'shoulder_to_waist': 1.6,
    'arm_to_body': 0.4,
    'leg_to_body': 0.5,
    'waist_to_hip': 0.75
}

class PostureAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Analizador de Postura")
        self.geometry("800x600")
        
        # Variables de instancia
        self.image_path = None
        self.landmarks = None
        self.proportions = {}
        self.calibration_factors = {
            'head': 1.0,
            'shoulders': 1.0,
            'waist': 1.0,
            'hips': 1.0,
            'knees': 1.0,
            'ankles': 1.0
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="Cargar Imagen", command=self.load_image_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Analizar Postura", command=self.analyze_and_show).pack(side='left', padx=5)
        
        # Frame para la imagen
        self.image_frame = ttk.LabelFrame(main_frame, text="Imagen")
        self.image_frame.pack(expand=True, fill='both', pady=5)
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(expand=True, fill='both')
        
        # Frame para resultados
        self.results_frame = ttk.LabelFrame(main_frame, text="Resultados")
        self.results_frame.pack(fill='x', pady=5)
        
        self.results_text = tk.Text(self.results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(expand=True, fill='both', padx=5, pady=5)
    
    def load_image_dialog(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            try:
                self.image_path = file_path
                self.display_image(file_path)
                messagebox.showinfo("Éxito", "Imagen cargada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")
    
    def display_image(self, image_path):
        image = Image.open(image_path)
        # Redimensionar manteniendo proporción
        display_size = (600, 400)
        image.thumbnail(display_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
    
    def analyze_and_show(self):
        if not self.image_path:
            messagebox.showwarning("Advertencia", "Por favor, cargue una imagen primero")
            return
            
        try:
            self.analyze_posture()
            report = self.generate_report()
            self.show_results(report)
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis: {str(e)}")
    
    def show_results(self, report):
        self.results_text.delete(1.0, tk.END)
        if not report:
            self.results_text.insert(tk.END, "No hay resultados disponibles")
            return
            
        # Mostrar comparaciones
        self.results_text.insert(tk.END, "RESULTADOS DEL ANÁLISIS\n\n")
        for key, data in report['comparison'].items():
            self.results_text.insert(tk.END, f"{key}:\n")
            self.results_text.insert(tk.END, f"  Tu medida: {data['yours']:.3f}\n")
            self.results_text.insert(tk.END, f"  Medida saludable: {data['healthy']:.3f}\n")
            self.results_text.insert(tk.END, f"  Diferencia: {data['percentage']:.1f}%\n\n")

    # [Mantener los métodos anteriores sin cambios]
    def analyze_posture(self):
        """Analiza la postura en la imagen cargada"""
        if not self.image_path:
            raise ValueError("No se ha cargado ninguna imagen")
            
        image = cv2.imread(self.image_path)
        if image is None:
            raise ValueError("No se pudo leer la imagen")
            
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if not results.pose_landmarks:
            raise ValueError("No se detectó postura en la imagen")
            
        self.landmarks = results.pose_landmarks.landmark
        self.calculate_proportions()
        return self.proportions
    
    def calculate_proportions(self):
        """Calcula las proporciones corporales"""
        if not self.landmarks:
            return
            
        # [Resto del método igual que antes]
        head = self.get_landmark_point(mp_pose.PoseLandmark.NOSE)
        neck = self.get_landmark_point(mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER)
        shoulder_left = self.get_landmark_point(mp_pose.PoseLandmark.LEFT_SHOULDER)
        shoulder_right = self.get_landmark_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
        waist = self.get_landmark_point(mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP)
        hip_left = self.get_landmark_point(mp_pose.PoseLandmark.LEFT_HIP)
        hip_right = self.get_landmark_point(mp_pose.PoseLandmark.RIGHT_HIP)
        knee_left = self.get_landmark_point(mp_pose.PoseLandmark.LEFT_KNEE)
        knee_right = self.get_landmark_point(mp_pose.PoseLandmark.RIGHT_KNEE)
        ankle_left = self.get_landmark_point(mp_pose.PoseLandmark.LEFT_ANKLE)
        ankle_right = self.get_landmark_point(mp_pose.PoseLandmark.RIGHT_ANKLE)
        
        # Calcular distancias
        head_height = self.distance(head, neck)
        torso_height = self.distance(neck, waist)
        full_height = self.distance(head, ankle_left)
        
        # Calcular proporciones
        self.proportions = {
            'head_to_body': head_height / full_height,
            'shoulder_to_waist': self.distance(shoulder_left, shoulder_right) / self.distance(waist, neck),
            'arm_to_body': self.distance(shoulder_left, knee_left) / full_height,
            'leg_to_body': self.distance(waist, ankle_left) / full_height,
            'waist_to_hip': self.distance(waist, hip_left) / self.distance(hip_left, knee_left)
        }
        return self.proportions

    def get_landmark_point(self, *landmarks):
        """Obtiene el punto promedio de landmarks con calibración"""
        x, y = 0, 0
        count = 0
        
        for landmark in landmarks:
            lm = self.landmarks[landmark.value]
            factor = self.get_calibration_factor(landmark.value)
            x += lm.x * factor
            y += lm.y * factor
            count += 1
        
        return (x / count, y / count)
    
    def get_calibration_factor(self, landmark_value):
        """Obtiene el factor de calibración para un landmark específico"""
        if landmark_value in [mp_pose.PoseLandmark.NOSE.value]:
            return self.calibration_factors['head']
        elif landmark_value in [mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_SHOULDER.value]:
            return self.calibration_factors['shoulders']
        elif landmark_value in [mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.RIGHT_HIP.value]:
            return self.calibration_factors['hips']
        elif landmark_value in [mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.RIGHT_KNEE.value]:
            return self.calibration_factors['knees']
        elif landmark_value in [mp_pose.PoseLandmark.LEFT_ANKLE.value, mp_pose.PoseLandmark.RIGHT_ANKLE.value]:
            return self.calibration_factors['ankles']
        return 1.0
    
    def distance(self, point1, point2):
        """Calcula la distancia euclidiana entre dos puntos"""
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
    
    def compare_with_healthy(self):
        """Compara las proporciones con los promedios saludables"""
        if not self.proportions:
            return None
            
        comparison = {}
        for key, value in self.proportions.items():
            healthy = HEALTHY_PROPORTIONS[key]
            difference = value - healthy
            percentage = (difference / healthy) * 100
            comparison[key] = {
                'yours': value,
                'healthy': healthy,
                'difference': difference,
                'percentage': percentage
            }
        return comparison
    
    def generate_report(self):
        """Genera un reporte completo del análisis"""
        if not self.proportions:
            return None
            
        comparison = self.compare_with_healthy()
        report = {
            'image_path': self.image_path,
            'proportions': self.proportions,
            'comparison': comparison,
            'calibration': self.calibration_factors
        }
        return report

if __name__ == "__main__":
    app = PostureAnalyzer()
    app.mainloop()
