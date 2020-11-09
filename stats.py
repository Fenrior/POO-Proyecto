# Ver historial de un paciente

import sqlite3
import crear_datos
import matplotlib.pyplot as plt

# Conjunto de enfermedades que pueden ser diagnosticadas
VALS = {
    "No se Diagnostico nada":0,
    "Depresion":1,
    "Ansiedad":2,
    "Trastorno de Panico":3,
    "Depresion|Ansiedad":4
}

# Historial, manejo de estadisticas de enfermedades mentales
class Historial:
    def __init__(self, file):
        self.info = crear_datos.BaseDatos(file)
    
    def ver_historial(self, nombre):
        """Ver historial de un usuario"""
        datos = self.info.ver_usuario(nombre)
        if datos:
            fig, ax = plt.subplots()
            fig.canvas.draw()
            fig.autofmt_xdate()
            plt.ylim(0, 5 * 1)
            labels = [item.get_text() for item in ax.get_yticklabels()]
            ax.set_title("Historial de Diagnosticos")
            for key, val in VALS.items():
                labels[val] = key
            labels[-1]=""
            ax.set_yticks([0, 1, 2, 3, 4, 5])
            ax.set_yticklabels(labels)
            fechas = [i[0][:] for i in datos]
            diagnosticos = [VALS[i[1]] for i in datos]
            plt.stem(fechas, diagnosticos, label="FEDDDDD")
            plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    hist = Historial("resources/datos.db")
    hist.ver_historial("Amildo")
