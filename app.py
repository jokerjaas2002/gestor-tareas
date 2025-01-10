import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class Tarea:
    def __init__(self, nombre, descripcion, fecha, hora, prioridad):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha
        self.hora = hora
        self.prioridad = prioridad
        self.completada = False

    def marcar_completada(self):
        self.completada = True

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
            "hora": self.hora,
            "prioridad": self.prioridad,
            "completada": self.completada
        }

    @staticmethod
    def from_dict(data):
        tarea = Tarea(data["nombre"], data["descripcion"], data["fecha"], data["hora"], data["prioridad"])
        tarea.completada = data["completada"]
        return tarea


class ListaTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, tarea):
        self.tareas.remove(tarea)

    def guardar_tareas(self, archivo):
        with open(archivo, 'w') as f:
            json.dump([tarea.to_dict() for tarea in self.tareas], f)

    def cargar_tareas(self, archivo):
        try:
            with open(archivo, 'r') as f:
                tareas_data = json.load(f)
                self.tareas = [Tarea.from_dict(data) for data in tareas_data]
        except FileNotFoundError:
            self.tareas = []


# Funciones de la interfaz gráfica
def agregar_tarea():
    nombre = nombre_entry.get()
    descripcion = descripcion_entry.get()
    fecha = fecha_entry.get()
    hora = hora_entry.get()
    prioridad = prioridad_entry.get()

    if not nombre or not descripcion or not fecha or not hora or not prioridad:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    nueva_tarea = Tarea(nombre, descripcion, fecha, hora, prioridad)
    lista.agregar_tarea(nueva_tarea)
    lista.guardar_tareas('tareas.json')  # Guardar tareas al agregar
    actualizar_lista_tareas()
    limpiar_campos()
    mensaje_label.config(text=f"Tarea '{nombre}' agregada.")

def limpiar_campos():
    nombre_entry.delete(0, tk.END)
    descripcion_entry.delete(0, tk.END)
    fecha_entry.delete(0, tk.END)
    hora_entry.delete(0, tk.END)
    prioridad_entry.delete(0, tk.END)

def actualizar_lista_tareas():
    lista_tareas.delete(0, tk.END)
    for tarea in lista.tareas:
        lista_tareas.insert(tk.END, f"{tarea.nombre} - {tarea.fecha} {tarea.hora} - {tarea.prioridad}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Tareas")
ventana.geometry("400x400")
ventana.configure(bg='lightblue')

# Crear un marco para organizar los elementos
frame = tk.Frame(ventana, bg='lightblue')
frame.pack(pady=10)

# Crear elementos de la interfaz
nombre_label = tk.Label(frame, text="Nombre de la tarea:", bg='lightblue')
nombre_label.pack()
nombre_entry = tk.Entry(frame)
nombre_entry.pack(pady=5)

descripcion_label = tk.Label(frame, text="Descripción:", bg='lightblue')
descripcion_label.pack()
descripcion_entry = tk.Entry(frame)
descripcion_entry.pack(pady=5)

fecha_label = tk.Label(frame, text="Fecha (YYYY-MM-DD):", bg='lightblue')
fecha_label.pack()
fecha_entry = tk.Entry(frame)
fecha_entry.pack(pady=5)

hora_label = tk.Label(frame, text="Hora (HH:MM):", bg='lightblue')
hora_label.pack()
hora_entry = tk.Entry(frame)
hora_entry.pack(pady=5)

prioridad_label = tk.Label(frame, text="Prioridad (Alta/Media/Baja):", bg='lightblue')
prioridad_label.pack()
prioridad_entry = tk.Entry(frame)
prioridad_entry.pack(pady=5)

agregar_boton = tk.Button(frame, text="Agregar Tarea", command=agregar_tarea, bg='green', fg='white')
agregar_boton.pack(pady=10)

# Crear lista de tareas con scrollbar
lista_frame = tk.Frame(ventana)
lista_frame.pack(pady=10)

scrollbar = tk.Scrollbar(lista_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_tareas = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, width=50, height=10)
lista_tareas.pack(side=tk.LEFT)

scrollbar.config(command=lista_tareas.yview)

# Label para mostrar mensajes de estado
mensaje_label = tk.Label(ventana, text="", bg='lightblue')
mensaje_label.pack(pady=10)

# Cargar tareas desde el archivo al iniciar
lista = ListaTareas()
lista.cargar_tareas('tareas.json')
actualizar_lista_tareas()  # Actualizar la lista de tareas en la interfaz

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
