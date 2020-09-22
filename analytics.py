# Andrés Cortez, Fernando Lavarreda, Valeria Paiz, Alejandro Ortega
# Universidad del Valle, Programacion Orientada a Objetos
import socket
import gspread as gs
from datetime import datetime

# Clase que almacena multiples Enfermedades y provee de un diagnostico
# Determina si las enfermedades se padecen o no al introducirle datos


class Diagnostico:
    def __init__(self):
        """Inicializar objeto Diagnostico, que contiene multiples Enfermedades"""
        self.enfermedades = []

    def add_enfermedad(self, nombre, umbral):
        """Agregar objeto Enfermedad al Diagnostico"""
        self.enfermedades.append(Enfermedad(nombre, umbral))

    def aumento_enfermedad(self, cantidad, nombre):
        """Incrementar el valor actual de una enfermedad en base a su nombre"""
        for enfermedad in self.enfermedades:
            if enfermedad.nombre == nombre:
                enfermedad.incrementar(cantidad)

    def ver_diagnostico(self):
        """Obtener listado de las enfermedades que dieron positivo"""
        positivos = []
        for enfermedad in self.enfermedades:
            if enfermedad.diagnostico():
                positivos.append(enfermedad.nombre)
        return positivos

    def eliminar_enfermedad(self, nombre):
        """Eliminar une enfermedad de la lista de enfermedades actuales"""
        indexes = []
        counter = 0
        for enfermedad in self.enfermedades:
            if enfermedad.get_nombre() == nombre:
                indexes.append(counter)
            counter += 1
        for index in indexes:
            self.enfermedades.pop(index)

    def clear(self):
        """Cambiar los valores actuales de las enfermedades a cero"""
        for enfermedad in self.enfermedades:
            enfermedad.valorActual = 0

# Clase que modela una enfermedad mental
# Toma como parametros su nombre y el umbral que indica se se padece o no


class Enfermedad:
    def __init__(self, nombre, umbral):
        """Creacion de un objeto que representa una enfermedad mental"""
        self.nombre = ""
        self.umbral = 0
        self.valorActual = 0
        self.set_nombre(nombre)
        self.set_umbral(umbral)

    def diagnostico(self):
        """Metodo para determinar si una enfermedad ha dado positivo o no"""
        if self.umbral <= self.valorActual:
            return True
        else:
            return False

    def incrementar(self, cantidad):
        """Aumental el valor actual de una enfermedad"""
        self.valorActual += cantidad

    def set_nombre(self, nombre):
        """Cambiar el nombre de la enfermedad"""
        self.nombre = nombre

    def set_umbral(self, umbral):
        """Cambiar umbral para la enfermedad"""
        self.umbral = umbral

    def set_valorActual(self, cantidad):
        self.valorActual = cantidad

    def get_nombre(self):
        """Visualizar el nombre de la enfermedad"""
        return self.nombre

    def get_umbral(self):
        """Visualizar umbral de la enfermedad"""
        return self.umbral

    def get_valor_actual(self):
        """Visualizar el valor actual de la enfermedad"""
        return self.valorActual


 ## Falta trabajar en LeturaArchivos
