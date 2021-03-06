# Andrés Cortez, Fernando Lavarreda, Valeria Paiz, Alejandro Ortega
# Universidad del Valle, Programacion Orientada a Objetos

import webbrowser
import tkinter as tk
import tkinter.font as tf
import tkinter.ttk as ttk
from PIL import ImageTk, Image


class Second(tk.Toplevel):
    def __init__(self, nombre_enfermedad, info, informacionrestante):
        """Constructor de clase toma como argumentos el nombre de enfermedad, informacion y un diccionario de otras
        con el resto de enfermedades y su informacion"""
        super().__init__()
        del informacionrestante[nombre_enfermedad]
        self.mas_ventanas = informacionrestante
        self.protocol("WM_DELETE_WINDOW", self.cierre)
        self.grab_set()
        self.fraa = tk.Frame(self, bg="#666699")
        self.title("Diagnóstico de la enfermedad")
        fonta = tf.Font(family="Algerian", size=12)
        fonta1 = tf.Font(family="Arial", size=8)
        fets = tf.Font(family="Verdana", size=10)
        self.geometry("800x580")
        self.iconbitmap("resources/meditation.ico")
        tk.Label(self, text="        ", bg="#666699").grid(row=1, column=1)
        self.config(bg="#666699")
        tk.Label(self, text="Información", font=fonta, bg="#666699").grid(row=0, column=0)
        tk.Label(self, text=f"Diagnóstico: {nombre_enfermedad}", bg="#666699").grid(row=1, column=0)
        self.fraa2 = tk.Frame(self)

        for i in range(2, 7):
            lj = tk.Label(self.fraa2, text=f"{info[i-2]}", bg="#666699", fg="#ffffff", justify=tk.RIGHT, anchor="w")
            lj.grid(row=i + 1, column=0, sticky=tk.W+tk.E)
        tk.Label(self.fraa, text="Tratamiento Propuesto: ", font=fets, bg="#666699").grid(row=0, column=0)
        for i in range(1, 16):
            lj = tk.Label(self.fraa, text=f"{info[i+5]}", bg="#666699", fg="#ffffff", justify=tk.RIGHT, anchor="w")
            lj.grid(row=i+1, column=0, columnspan=5, sticky=tk.W+tk.E)
        self.of = tk.Label(self.fraa, font=fonta1, text="www.oms.org/gethelp", foreground="lightblue",
                             bg="#666699", justify=tk.LEFT, cursor="hand1")
        # self.link2 = tk.Label(self.fraa, font=fonta1, text="https://meditacionguatemala.org/", foreground="lightblue",
        # bg="#666699").grid(row=1, column=0)
        # self.link3 = tk.Label(self.fraa, font=fonta1, text="https://bcc.com.gt/contacto", foreground="lightblue",
        # bg="#666699").grid(row=1, column=2, columnspan=1)
        # Configure Image for presentation
        ng = ImageTk.PhotoImage(Image.open("resources/health.png").resize((180, 180)))
        self.ll = tk.Canvas(self, width=180, height=180, bg="#666699")
        self.ll.create_image(90, 90, image=ng, anchor=tk.CENTER)
        self.ll.image = ng
        self.of.bind("<Button-1>", self.search)
        self.of.grid(row=1, column=0)
        self.fraa2.grid(row=2, column=0, rowspan=1)
        self.ll.grid(row=2, column=2, rowspan=1)
        self.fraa.grid(row=3, column=0, columnspan=3)

    def cierre(self):
        """Al cerrar ventana ver si no han quedado pendiente la apertura de otra de ellas"""
        self.destroy()
        if list(self.mas_ventanas.keys()):
            llaves = list(self.mas_ventanas.keys()).copy()
            nv = Second(llaves[0], self.mas_ventanas[llaves[0]], self.mas_ventanas)
            nv.mainloop()
    
    def search(self, e):
        try:
            webbrowser.open(e.widget["text"])
        except Exception:
            pass
    
        

class RespuestasCuestionario(tk.Toplevel):
    def __init__(self, diagnosticos, lectura, color="#3178eb"):
        super().__init__()
        self.grab_set()
        self.title("Diagnosticos")
        self.config(bg=color)
        self.iconbitmap("resources/meditation.ico")
        font3 = tf.Font(size=12, family="Courier", weight="bold")
        tk.Label(self, text="Diagnosticos: ", font=font3, foreground="white", bg=color).grid(row=0, column=0)
        self.kk = ttk.Combobox(self, values=diagnosticos)
        self.kk.bind("<<ComboboxSelected>>", self.ver)
        self.kk.grid(row=0, column=1)
        self.lectura = lectura
        self.resizable(False, False)

    def ver(self,*args):
        seleccion = self.kk.get()
        options = ["Ansiedad", "Depresion", "Trastorno de Panico"]
        if seleccion in options:
            info = self.lectura.ver_diagnostico(True, seleccion)
            ventana_diagnostico = Second(seleccion, info[seleccion], info)
            ventana_diagnostico.mainloop()


# No ejecutar como archivo principal, en si no proveer nombre enfermedad, informacion enfermedad y informacion restante

if __name__ == "__main__":
    pass
# sc = Second()
# sc.mainloop()
