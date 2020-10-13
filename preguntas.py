# Andrés Cortez, Fernando Lavarreda, Valeria Paiz, Alejandro Ortega
# Universidad del Valle, Programacion Orientada a Objetos

import tkinter as tk
import tkinter.font as tf
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import resultados as rt

# Clases para la parte grafica de las preguntas de la aplicacion
# Toma como argumento un objeto LecturaArchivos para mostrar e interactuar


class MyApp(tk.Toplevel):
    def __init__(self, lectura):
        super().__init__()
        self.grab_set()
        self.lectura = lectura
        # -----------------General Look for the App------------------------------ #
        fonta = tf.Font(size=15, family="Helvetica", weight="bold")
        font3 = tf.Font(size=12, family="Courier", weight="bold")
        fonta2 = tf.Font(size=3)
        self.config(bg="#3cb371")
        self.title("Mindfulness")
        self.options = ["Ansiedad", "Depresion"]
        self.geometry("600x480")
        self.iconbitmap("resources/meditation.ico")

        # ------------------Question Configurations------------------------------ #
        self.tituloCuestionario = tk.Label(self, text="Cuestionario", bg="#3cb371", font=font3, foreground="#800020").grid(row=2, column=1, columnspan=2)
        self.fran = Questions(self, lectura)
        self.scroll_canvas = tk.Canvas(self, height=340, width=10, bg="#5181a9")
        self.scroll_canvas.pack_propagate(0)
        self.scroll = tk.Scrollbar(self.scroll_canvas, orient=tk.VERTICAL)
        self.fran.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.fran.yview)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)

        # ----------------------------------------------------------------------- #

        self.gg = tk.Label(self, text="Bienvenido a Mindfulness Application", bg="#3cb371", foreground="#a83285", font=fonta).grid(row=0, columnspan=7)

        self.ok = tk.Label(self, text="Sabe que es lo que tiene: ", bg="#3cb371").grid(column=6, row=1)
        self.ok2 = tk.Label(self, text="    ", bg="#3cb371").grid(column=5, row=1)
        self.ok3 = tk.Label(self, text="   ", bg="#3cb371").grid(column=0, row=1)
        self.ok4 = tk.Label(self, text="   ", bg="#3cb371", font=fonta2).grid(column=0, row=4)
        self.kk = ttk.Combobox(self, values=self.options)
        self.kk.bind("<<ComboboxSelected>>", self.ver2)

        img = ImageTk.PhotoImage(Image.open("resources/brain.png").resize((190, 190)))
        self.canv = tk.Canvas(self, width=200, height=200, bg="teal")
        self.canv.create_image(102, 100, anchor=tk.CENTER, image=img)
        self.canv.image = img
        self.canv.grid(row=3, column=6)

        self.fran.grid(row=3, column=1, columnspan=4)
        self.confirm = tk.IntVar()
        tk.Checkbutton(self, text="Compartir informacion", variable=self.confirm, bg="#3cb371").grid(row=5, column=1, columnspan=2)
        self.submit = ttk.Button(self, text="Obtener Diagnóstico", command=self.ver).grid(row=5, column=3, columnspan=2)
        self.kk.grid(row=2, column=6)
        self.scroll_canvas.grid(row=3, column=5, padx=(0, 50))

    def ver(self):
        """Visualizar diagnostico a traves del cuestionario para desplegar las posibles enfermedades"""
        respondido = [valor.get() for valor in self.fran.respuestas]
        self.lectura.clamp_respuestas(respondido)
        
        inf = ["n", "n", "n"]
        if self.confirm.get():
            user = Informacion(self)
            inf = user.cierre()

        info = self.lectura.ver_diagnostico()
        self.lectura.grabar_info(['|'.join(list(info.keys()))]+inf, "resources/creds.json", "Mindfulness")
        self.lectura.set_to_zero()
        llaves = list(info.keys()).copy()
        ventana_diagnostico = rt.Second(llaves[0], info[llaves[0]], info)
        ventana_diagnostico.mainloop()

    def ver2(self, *args):
        """Visualizar enfermedad cuando el paciente sabe que es lo que tiene"""
        seleccion = self.kk.get()

        inf = ["n", "n", "n"]
        if self.confirm.get():
            user = Informacion(self)
            inf = user.cierre()

        self.lectura.grabar_info([seleccion]+inf, "resources/creds.json", "Mindfulness")
        if seleccion in self.options:
            info = self.lectura.ver_diagnostico(True, seleccion)
            ventana_diagnostico = rt.Second(seleccion, info[seleccion], info)
            ventana_diagnostico.mainloop()


# Clase que muestra las preguntas en pantalla al usuario
# Toma como argumentos su pantalla madre, el objeto LecturaArchivos y color de las preguntas

class Questions(tk.Canvas):
    def __init__(self, master, lectura, color="#5181a9"):
        super().__init__(master, width=300, height=340, scrollregion=(0, 0, 0, 1925), bd=0, bg=color)
        self.pack_propagate(0)
        font_1 = tf.Font(size=10, family="Verdana")
        self.frame = tk.Frame(self, width=300, height=100, bg=color)
        self.create_window((-3, -3), window=self.frame, anchor=tk.NW)
        self.display = lectura.ver_preguntas()
        self.respuestas = [tk.IntVar() for _ in self.display]

        j = 1
        for i in range(0, len(self.display)-1):
            lb = tk.Label(self.frame, text=self.display[i+1], font=font_1, bg="#caf1de", justify=tk.LEFT)
            lb.grid(row=j, column=0, columnspan=5, sticky=tk.W+tk.E)
            for ix in range(4):
                rd = tk.Radiobutton(self.frame, text=f"{ix}", variable=self.respuestas[i], value=ix, bg=color)
                rd.grid(row=j+1, column=ix)
            j += 2
        master.update_idletasks()


# Clase para agregar informacion adicional acerca del usuario

class Informacion(tk.Toplevel):
    def __init__(self, parent, color="#5cdbc4"):
        super().__init__(parent)
        self.title("Informacion")
        self.iconbitmap("resources/meditation.ico")
        self.config(bg=color)
        self.sexo = tk.StringVar()
        self.edad = tk.StringVar()
        self.ingresos = tk.StringVar()
        tk.Label(self, text="Sexo: ", bg="#84d44e", justify=tk.LEFT).grid(row=1, column=0, sticky=tk.W+tk.E)
        tk.Radiobutton(self, text="Masculino", variable=self.sexo, value="m", bg=color).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        tk.Radiobutton(self, text="Femenino ", variable=self.sexo, value="f", bg=color).grid(row=2, column=2, columnspan=2, sticky=tk.W)
        tk.Radiobutton(self, text="N/A", variable=self.sexo, value="n", bg=color).grid(row=2, column=4)

        tk.Label(self, text="Edad: ", bg="#84d44e", justify=tk.LEFT).grid(row=3, column=0, sticky=tk.W+tk.E)
        tk.Radiobutton(self, text="<17", variable=self.edad, value="<17", bg=color).grid(row=4, column=0, sticky=tk.W)
        tk.Radiobutton(self, text="17-25", variable=self.edad, value="17-25", bg=color).grid(row=4, column=1)
        tk.Radiobutton(self, text="26-39", variable=self.edad, value="26-39", bg=color).grid(row=4, column=2)
        tk.Radiobutton(self, text="40-60", variable=self.edad, value="40-60", bg=color).grid(row=4, column=3)
        tk.Radiobutton(self, text="60<", variable=self.edad, value="60<", bg=color).grid(row=4, column=4)
        tk.Radiobutton(self, text="N/A", variable=self.edad, value="n", bg=color).grid(row=4, column=5)

        tk.Label(self, text="Ingresos: ", bg="#84d44e", justify=tk.LEFT).grid(row=5, column=0, sticky=tk.W+tk.E)
        tk.Radiobutton(self, text="Bajos", variable=self.ingresos, value="Ba", bg=color).grid(row=6, column=0)
        tk.Radiobutton(self, text="Medios", variable=self.ingresos, value="Me", bg=color).grid(row=6, column=1)
        tk.Radiobutton(self, text="Altos", variable=self.ingresos, value="Al", bg=color).grid(row=6, column=2)
        tk.Radiobutton(self, text="N/A", variable=self.ingresos, value="n", bg=color).grid(row=6, column=3)


        ttk.Button(self, text="Enviar", command=self.cierre)
        self.edad.set("n")
        self.sexo.set("n")
        self.ingresos.set("n")
    
    def cierre(self):
        self.grab_set()
        self.wait_window()
        return [self.sexo.get(), self.edad.get(), self.ingresos.get()]


if __name__ == "__main__":
    pass
# yy = MyApp()
# yy.mainloop()
