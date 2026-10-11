import re
import math
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

ARCHIVO = "Datos3N_13Feb26.txt"

# Letras (con acentos, ñ y ü), separadas por un espacio, guion o apóstrofo
LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
PATRON_TEXTO = re.compile(rf"^[{LETRAS}]+(?:[ '\-][{LETRAS}]+)*$")

GENEROS = {1: "Masculino", 2: "Femenino", 3: "No Definido"}


# ---------------------------------------------------------------
# VALIDADORES: devuelven None si el valor es correcto,
# o un texto explicando qué está mal. No muestran ventanas.
# ---------------------------------------------------------------
def validar_texto(valor, campo):
    valor = valor.strip()
    if not valor:
        return f"{campo}: no puede estar vacío."
    if len(valor) < 2:
        return f"{campo}: debe tener al menos 2 letras."
    if not PATRON_TEXTO.match(valor):
        return f"{campo}: solo se permiten letras y espacios (sin números ni símbolos)."
    return None


def validar_edad(valor):
    valor = valor.strip()
    if not valor:
        return "Edad: no puede estar vacía."
    if not (valor.isascii() and valor.isdigit()):
        return "Edad: debe ser un número entero positivo."
    if not 1 <= int(valor) <= 120:
        return "Edad: debe estar entre 1 y 120 años."
    return None


def validar_estatura(valor):
    valor = valor.strip().replace(",", ".")  # acepta 1,70 y 1.70
    if not valor:
        return "Estatura: no puede estar vacía."
    try:
        numero = float(valor)
    except ValueError:
        return "Estatura: debe ser un número (ejemplo: 1.70)."
    if not math.isfinite(numero):
        return "Estatura: valor no válido."
    if not 0.50 <= numero <= 2.50:
        return "Estatura: debe estar en metros, entre 0.50 y 2.50 (ejemplo: 1.70)."
    return None


def validar_telefono(valor):
    valor = valor.strip()
    if not valor:
        return "Teléfono: no puede estar vacío."
    if not (valor.isascii() and valor.isdigit()):
        return "Teléfono: solo debe contener dígitos."
    if len(valor) != 10:
        return "Teléfono: debe tener exactamente 10 dígitos."
    return None


# ---------------------------------------------------------------
# INTERFAZ
# ---------------------------------------------------------------
def main():
    ventana = tk.Tk()
    ventana.configure(bg="blue")
    ventana.geometry("350x600")
    ventana.title("Actividad 04 – Formulario de Registro Vr. 002")

    rbSeleccionGenero = tk.IntVar(value=0)

    def crear_campo(texto, ancho):
        tk.Label(ventana, text=texto, font=("Segoe UI", 14, "bold"),
                 bg="blue").pack(padx=10, pady=8)
        entrada = tk.Entry(ventana, width=ancho, justify="center")
        entrada.pack()
        return entrada

    tbNombre = crear_campo("Nombre : ", 35)
    tbApellidos = crear_campo("Apellidos : ", 35)
    tbEdad = crear_campo("Edad : ", 10)
    tbEstatura = crear_campo("Estatura (m) : ", 15)
    tbTelefono = crear_campo("Teléfono : ", 35)

    gb = tk.LabelFrame(ventana, text="Seleccione un Género : ", padx=10, pady=8)
    gb.pack(padx=10, pady=8)
    for col, (valor, texto) in enumerate(GENEROS.items(), start=1):
        tk.Radiobutton(gb, text=texto, value=valor,
                       variable=rbSeleccionGenero).grid(column=col, row=1)

    def borrar():
        for caja in (tbNombre, tbApellidos, tbEdad, tbEstatura, tbTelefono):
            caja.delete(0, tk.END)
        rbSeleccionGenero.set(0)
        tbNombre.focus_set()

    def guardar():
        nombres = tbNombre.get().strip()
        apellidos = tbApellidos.get().strip()
        edad = tbEdad.get().strip()
        estatura = tbEstatura.get().strip().replace(",", ".")
        tel = tbTelefono.get().strip()

        # (caja, mensaje de error) para poder enfocar la primera con error
        revisiones = [
            (tbNombre, validar_texto(nombres, "Nombre")),
            (tbApellidos, validar_texto(apellidos, "Apellidos")),
            (tbEdad, validar_edad(edad)),
            (tbEstatura, validar_estatura(estatura)),
            (tbTelefono, validar_telefono(tel)),
        ]
        errores = [(caja, msg) for caja, msg in revisiones if msg]
        if rbSeleccionGenero.get() not in GENEROS:
            errores.append((None, "Género: debe seleccionar una opción."))

        if errores:
            messagebox.showerror(
                "Error en el formulario",
                "Corrija lo siguiente:\n\n" + "\n".join(f"• {m}" for _, m in errores),
            )
            primera_caja = next((c for c, _ in errores if c is not None), None)
            if primera_caja:
                primera_caja.focus_set()
            return

        genero = GENEROS[rbSeleccionGenero.get()]
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        datos = (
            f"Fecha de registro : {fecha}\n"
            f"Nombre : {nombres.title()}\n"
            f"Apellidos : {apellidos.title()}\n"
            f"Edad : {int(edad)}\n"
            f"Teléfono : {tel}\n"
            f"Estatura : {float(estatura):.2f} m\n"
            f"Género : {genero}"
        )

        try:
            with open(ARCHIVO, "a", encoding="utf-8") as archivo:
                archivo.write(datos + "\n\n")
        except OSError as error:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{error}")
            return

        messagebox.showinfo("Información", "Datos guardados correctamente\n\n" + datos)
        borrar()

    gb2 = tk.LabelFrame(ventana, text="")
    gb2.pack(padx=10, pady=8)
    tk.Button(gb2, text="Borrar", width=10, padx=10, pady=8,
              command=borrar).grid(column=2, row=1)
    tk.Button(gb2, text="Guardar", width=10, padx=10, pady=8,
              command=guardar).grid(column=1, row=1)

    tbNombre.focus_set()
    ventana.mainloop()


if __name__ == "__main__":
    main()