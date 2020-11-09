# Andrés Cortez, Fernando Lavarreda, Valeria Paiz, Alejandro Ortega
# Universidad del Valle, Programacion Orientada a Objetos

import tkinter as tk
import tkinter.font as tf
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import resultados as rt
import stats
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import crear_datos
import sqlite3 as db

# Clases para la parte grafica de las preguntas de la aplicacion
# Toma como argumento un objeto LecturaArchivos para mostrar e interactuar


class MyApp(tk.Toplevel):
    def __init__(self, lectura, usuario):
        super().__init__()
        self.grab_set()
        self.lectura = lectura
        self.user = usuario
        # -----------------General Look for the App------------------------------ #
        fonta = tf.Font(size=15, family="Helvetica", weight="bold")
        font3 = tf.Font(size=12, family="Courier", weight="bold")
        fonta2 = tf.Font(size=3)
        self.config(bg="#3cb371")
        self.title("Mindfulness")
        self.options = ["Ansiedad", "Depresion", "Trastorno de Panico"]
        self.geometry("600x480")
        self.iconbitmap("resources/meditation.ico")

        # ------------------Question Configurations------------------------------ #
        tk.Label(self, text="Cuestionario", bg="#3cb371", font=font3, foreground="#800020").grid(row=2, column=1, columnspan=2)
        self.fran = Questions(self, lectura)
        self.scroll_canvas = tk.Canvas(self, height=340, width=10, bg="#5181a9")
        self.scroll_canvas.pack_propagate(0)
        self.scroll = tk.Scrollbar(self.scroll_canvas, orient=tk.VERTICAL)
        self.fran.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.fran.yview)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)

        # ----------------------------------------------------------------------- #

        tk.Label(self, text="Bienvenido a Mindfulness Application", bg="#3cb371", foreground="#a83285", font=fonta).grid(row=0, columnspan=7)

        tk.Label(self, text="Sabe que es lo que tiene: ", bg="#3cb371").grid(column=6, row=1)
        tk.Label(self, text="    ", bg="#3cb371").grid(column=5, row=1)
        tk.Label(self, text="   ", bg="#3cb371").grid(column=0, row=1)
        tk.Label(self, text="   ", bg="#3cb371", font=fonta2).grid(column=0, row=4)
        self.kk = ttk.Combobox(self, values=self.options)
        self.kk.bind("<<ComboboxSelected>>", self.ver2)

        img = ImageTk.PhotoImage(Image.open("resources/brain.png").resize((190, 190)))
        self.canv = tk.Canvas(self, width=200, height=200, bg="teal")
        self.canv.create_image(102, 100, anchor=tk.CENTER, image=img)
        self.canv.image = img
        self.canv.grid(row=3, column=6)

        self.fran.grid(row=3, column=1, columnspan=4)
        self.submit = ttk.Button(self, text="Obtener Diagnóstico", command=self.ver).grid(row=5, column=3, columnspan=2, sticky=tk.NW+tk.SE)
        ttk.Button(self, text="Ver Historial", command=self.hist).grid(row=5, column=1, columnspan=2, sticky=tk.NW+tk.SE)
        tk.Button(self, text="Compartir informacion", command=self.share, bg="#34c3eb").grid(row=5, column=6, sticky=tk.NW+tk.SE)
        self.kk.grid(row=2, column=6)
        self.scroll_canvas.grid(row=3, column=5, padx=(0, 50))

    def ver(self):
        """Visualizar diagnostico a traves del cuestionario para desplegar las posibles enfermedades"""
        respondido = [valor.get() for valor in self.fran.respuestas]
        self.lectura.clamp_respuestas(respondido)
        

        info = self.lectura.ver_diagnostico()
        self.lectura.grabar_info(self.user,'|'.join(list(info.keys())))
        self.lectura.set_to_zero()
        #llaves = list(info.keys()).copy()
        rt.RespuestasCuestionario(list(info.keys()).copy(), self.lectura).ver()
        #ventana_diagnostico = rt.Second(llaves[0], info[llaves[0]], info)
        #ventana_diagnostico.mainloop()

    def ver2(self, *args):
        """Visualizar enfermedad cuando el paciente sabe que es lo que tiene"""
        seleccion = self.kk.get()
        self.lectura.grabar_info(self.user, seleccion)
        if seleccion in self.options:
            info = self.lectura.ver_diagnostico(True, seleccion)
            ventana_diagnostico = rt.Second(seleccion, info[seleccion], info)
            ventana_diagnostico.mainloop()
    
    def hist(self):
        lh = stats.Historial("resources/datos.db")
        lh.ver_historial(self.user[0])
    
    def share(self):
        directory = fd.askdirectory(title="Nuevo Direcotrio", initialdir="/", mustexist=True, parent=self)
        if directory:
            try:
                conn = db.connect("resources/datos.db")
                backup = crear_datos.BaseDatos(directory+"/share.db")
                backup.create_registry_table()
                backup.create_user_table()
                bck = db.connect(directory+"/share.db")
                with bck:
                    conn.backup(bck)
                bck.close()
                conn.close()
            except Exception:
                pass
            else:
                mb.askquestion("Compartir", message=f"Para compartir la informacion envia el archivo:\n\n{directory}/share.db\n\nA:\nlav19205@uvg.edu.gt, pai19155@uvgedu.gt, \nort18248@uvg.edu.gt o cor20238@uvg.edu.gt\n\nGracias!", parent=self)


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




if __name__ == "__main__":
    pass
# yy = MyApp()
# yy.mainloop()
