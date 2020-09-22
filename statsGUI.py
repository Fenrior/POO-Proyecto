# Modulo para interactuar de manera grafica con la informacion de los usuarios
# Agregado por Fernando Lavarreda 
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tf
import tkinter.filedialog as fd


class VerInfo(tk.Tk):
    def __init__(self, ManejoEstadisticas):
        super().__init__()
        self.manejo = ManejoEstadisticas
        self.geometry("370x120")
        self.title("Estadisticas MindfulnessGT")
        self.iconbitmap("resources/bar-chart.ico")
        self.config(bg="#74bce3")

        font = tf.Font(size=18, family="Verdana", weight="bold")
        self.titulo = tk.Label(self, bg="#74bce3", font=font, text="Estadísticas MindfulnessGT", foreground="#009c53")
        descarga = ttk.Button(self, text="Descargar informacion", command=self.download)
        self.excel = ttk.Button(self, text="Enviar a Excel", command=self.create, state=tk.DISABLED)
        self.graphs = ttk.Button(self, text="Grafico de Barras", command=self.graphicate, state=tk.DISABLED)

        self.archivo = tk.StringVar()
        ingresar_archivo = tk.Entry(self, textvariable=self.archivo)
        self.lb = tk.Label(self, bg="#74bce3", foreground="#f7b80a", text="")

