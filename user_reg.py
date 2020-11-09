

import tkinter as tk
import time
import tkinter.ttk as ttk
import crear_datos as c_datos

# Login de usuarios

class Login(tk.Toplevel):
    def __init__(self, parent, color="#60db67", db="resources/datos.db"):
        super().__init__(parent)
        self.config(bg=color)
        self.iconbitmap("resources/meditation.ico")
        self.db = db
        self.usuario = tk.StringVar()
        self.clave = tk.StringVar()
        self.mostrar = tk.StringVar()
        tk.Label(self, text="Usuario: ", bg=color).grid(row=0, column=0, sticky=tk.W)
        tk.Label(self, text="Clave: ", bg=color).grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self, textvariable=self.usuario, width=15).grid(column=1, row=0, sticky=tk.W)
        tk.Entry(self, textvariable=self.clave, width=15, show="*").grid(column=1, row=1, sticky=tk.W)
        tk.Label(self, textvariable=self.mostrar, bg=color).grid(column=0, row=2, columnspan=2, sticky=tk.W+tk.E)
        
        
        ttk.Button(self, text="Ingresar", command=self.ingresar).grid(column=1, row=3, sticky=tk.W+tk.E)
        ttk.Button(self, text="Registrarse", command=self.sign).grid(column=0, row=3, sticky=tk.W+tk.E)
        
    def inicio(self):
        self.grab_set()
        self.wait_window()
        base_datos = c_datos.BaseDatos(self.db)
        return base_datos.user_login(self.usuario.get(), self.clave.get())
    
    def ingresar(self):
        base_datos = c_datos.BaseDatos(self.db)
        info = base_datos.user_login(self.usuario.get(), self.clave.get())[1]
        self.mostrar.set(info)
        self.update_idletasks()
        if info == "Acceso concedido":
            time.sleep(0.8)
            self.destroy()
            

    def sign(self):
        sig = Signin(self, self.db)
        sg = sig.inicio()
        self.usuario.set(sg[0])
        self.clave.set(sg[1])
        self.ingresar()



# Registro, crear un nuevo usuario

class Signin(tk.Toplevel):
    def __init__(self, parent, db, color="#36a893"):
        super().__init__(parent)
        self.config(bg=color)
        self.iconbitmap("resources/meditation.ico")
        self.db = db
        self.usuario = tk.StringVar()
        self.clave = tk.StringVar()
        self.sexo = tk.StringVar()
        self.edad = tk.StringVar()
        self.ingresos = tk.StringVar()
        self.mostrar = tk.StringVar()
        tk.Label(self, text="Usuario: ", bg=color).grid(row=0, column=0, sticky=tk.W)
        tk.Label(self, text="Clave: ", bg=color).grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self, textvariable=self.usuario, width=15).grid(column=1, row=0, sticky=tk.W)
        tk.Entry(self, textvariable=self.clave, width=15, show="*").grid(column=1, row=1, sticky=tk.W)
        
        tk.Label(self, text="Sexo: ", bg=color).grid(row=2, column=0)
        tk.Radiobutton(self, text="Masculino", value="m", variable=self.sexo, bg=color).grid(row=3, column=0, sticky=tk.W)
        tk.Radiobutton(self, text="Femenino", value="f", variable=self.sexo, bg=color).grid(row=3, column=1, sticky=tk.W)
        
        tk.Label(self, text="Edad: ", bg=color).grid(row=4, column=0)
        tk.Radiobutton(self, text="<17", value="<17", variable=self.edad, bg=color).grid(row=5, column=0, sticky=tk.W)
        tk.Radiobutton(self, text="17-25", value="17-25", variable=self.edad, bg=color).grid(row=5, column=1, sticky=tk.W)
        tk.Radiobutton(self, text="26-39", value="26-39", variable=self.edad, bg=color).grid(row=5, column=2, sticky=tk.W)
        tk.Radiobutton(self, text="40-60", value="40-60", variable=self.edad, bg=color).grid(row=5, column=3, sticky=tk.W)
        tk.Radiobutton(self, text="60<", value="60<", variable=self.edad, bg=color).grid(row=5, column=4, sticky=tk.W)
        
        
        tk.Label(self, text="Ingresos: ", bg=color).grid(row=6, column=0)
        tk.Radiobutton(self, text="Muy Bajos", value="MB", variable=self.ingresos, bg=color).grid(row=7, column=0, sticky=tk.W)
        tk.Radiobutton(self, text="Bajos", value="B", variable=self.ingresos, bg=color).grid(row=7, column=1, sticky=tk.W)
        tk.Radiobutton(self, text="Medios", value="M", variable=self.ingresos, bg=color).grid(row=7, column=2, sticky=tk.W)
        tk.Radiobutton(self, text="Altos", value="A", variable=self.ingresos, bg=color).grid(row=7, column=3, sticky=tk.W)
        tk.Radiobutton(self, text="Muy Altos", value="MA", variable=self.ingresos, bg=color).grid(row=7, column=4, sticky=tk.W)
        
        tk.Label(self, textvariable=self.mostrar, bg=color).grid(row=8, column=0, columnspan=4,sticky=tk.W+tk.E)
        ttk.Button(self, text="Crear", command=self.crear).grid(row=8, column=4)
        
        self.sexo.set("f")
        self.edad.set("<17")
        self.ingresos.set("MB")
    
    def inicio(self):
        self.grab_set()
        self.wait_window()
        return self.usuario.get(), self.clave.get()
    
    def crear(self):
        base_datos = c_datos.BaseDatos(self.db)
        info = base_datos.user_signin(self.usuario.get(), self.clave.get(), self.sexo.get(), self.edad.get(), self.ingresos.get())[0]
        self.mostrar.set(info)
        self.update_idletasks()
        if info == "Usuario creado correctamente":
            time.sleep(1)
            self.destroy()
        
        

if __name__ == "__main__":
    root = tk.Tk()
    lg = Login(root)
    root.mainloop()
    lg.mainloop()
        
        
        
        
        
        
        
        