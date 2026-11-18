#!/usr/bin/env python3
"""
Calculadora Científica en Python (Interfaz Gráfica con Tkinter)
"""

import math
import tkinter as tk
from tkinter import messagebox


class CalculadoraCientifica:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("420x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.expresion = ""
        self.modo_grados = True  # True = Grados (DEG), False = Radianes (RAD)
        self.memoria = 0.0

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Pantalla principal
        frame_pantalla = tk.Frame(self.root, bg="#1e1e2e", padx=12, pady=12)
        frame_pantalla.pack(fill="x")

        self.lbl_modo = tk.Label(
            frame_pantalla,
            text="MODO: DEG (Grados)",
            font=("Consolas", 10, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e",
            anchor="w",
        )
        self.lbl_modo.pack(fill="x")

        self.entrada_var = tk.StringVar(value="0")
        self.pantalla = tk.Entry(
            frame_pantalla,
            textvariable=self.entrada_var,
            font=("Consolas", 24, "bold"),
            bg="#11111b",
            fg="#cdd6f4",
            bd=0,
            justify="right",
            insertbackground="#cdd6f4",
        )
        self.pantalla.pack(fill="x", ipady=15, pady=(6, 0))

        # Contenedor de botones
        frame_botones = tk.Frame(self.root, bg="#1e1e2e", padx=10, pady=5)
        frame_botones.pack(fill="both", expand=True)

        # Definición de botones (texto, fila, columna, tipo)
        botones = [
            ("DEG/RAD", 0, 0, "func"), ("sin", 0, 1, "func"), ("cos", 0, 2, "func"), ("tan", 0, 3, "func"), ("C", 0, 4, "clear"),
            ("asin", 1, 0, "func"), ("acos", 1, 1, "func"), ("atan", 1, 2, "func"), ("log", 1, 3, "func"), ("DEL", 1, 4, "clear"),
            ("ln", 2, 0, "func"), ("√", 2, 1, "func"), ("x²", 2, 2, "func"), ("xʸ", 2, 3, "func"), ("/", 2, 4, "op"),
            ("π", 3, 0, "func"), ("7", 3, 1, "num"), ("8", 3, 2, "num"), ("9", 3, 3, "num"), ("*", 3, 4, "op"),
            ("e", 4, 0, "func"), ("4", 4, 1, "num"), ("5", 4, 2, "num"), ("6", 4, 3, "num"), ("-", 4, 4, "op"),
            ("n!", 5, 0, "func"), ("1", 5, 1, "num"), ("2", 5, 2, "num"), ("3", 5, 3, "num"), ("+", 5, 4, "op"),
            ("(", 6, 0, "func"), (")", 6, 1, "func"), ("0", 6, 2, "num"), (".", 6, 3, "num"), ("=", 6, 4, "eq"),
        ]

        colores = {
            "num": ("#313244", "#cdd6f4"),
            "op": ("#f38ba8", "#11111b"),
            "func": ("#45475a", "#89b4fa"),
            "clear": ("#fab387", "#11111b"),
            "eq": ("#a6e3a1", "#11111b"),
        }

        for i in range(7):
            frame_botones.rowconfigure(i, weight=1)
        for j in range(5):
            frame_botones.columnconfigure(j, weight=1)

        for texto, fila, col, tipo in botones:
            bg_color, fg_color = colores[tipo]
            btn = tk.Button(
                frame_botones,
                text=texto,
                font=("Consolas", 13, "bold"),
                bg=bg_color,
                fg=fg_color,
                activebackground="#585b70",
                activeforeground="#ffffff",
                bd=0,
                cursor="hand2",
                command=lambda t=texto: self._al_presionar(t),
            )
            btn.grid(row=fila, column=col, sticky="nsew", padx=3, pady=3)

        # Atajos de teclado
        self.root.bind("<Return>", lambda _: self._al_presionar("="))
        self.root.bind("<BackSpace>", lambda _: self._al_presionar("DEL"))
        self.root.bind("<Escape>", lambda _: self._al_presionar("C"))

    def _alternar_modo(self):
        self.modo_grados = not self.modo_grados
        texto_modo = "MODO: DEG (Grados)" if self.modo_grados else "MODO: RAD (Radianes)"
        self.lbl_modo.config(text=texto_modo)

    def _sin(self, x):
        return math.sin(math.radians(x)) if self.modo_grados else math.sin(x)

    def _cos(self, x):
        return math.cos(math.radians(x)) if self.modo_grados else math.cos(x)

    def _tan(self, x):
        if self.modo_grados and (x % 180 == 90):
            raise ValueError("Tangente indefinida")
        return math.tan(math.radians(x)) if self.modo_grados else math.tan(x)

    def _asin(self, x):
        res = math.asin(x)
        return math.degrees(res) if self.modo_grados else res

    def _acos(self, x):
        res = math.acos(x)
        return math.degrees(res) if self.modo_grados else res

    def _atan(self, x):
        res = math.atan(x)
        return math.degrees(res) if self.modo_grados else res

    def _al_presionar(self, valor: str):
        if valor == "DEG/RAD":
            self._alternar_modo()
            return

        if valor == "C":
            self.expresion = ""
            self.entrada_var.set("0")
            return

        if valor == "DEL":
            self.expresion = self.expresion[:-1]
            self.entrada_var.set(self.expresion if self.expresion else "0")
            return

        if valor == "=":
            self._calcular()
            return

        mapeo = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "asin": "asin(",
            "acos": "acos(",
            "atan": "atan(",
            "log": "log(",
            "ln": "ln(",
            "√": "sqrt(",
            "x²": "**2",
            "xʸ": "**",
            "π": "pi",
            "e": "e",
            "n!": "factorial(",
        }

        token = mapeo.get(valor, valor)
        if self.expresion == "0" and token.isdigit():
            self.expresion = token
        else:
            self.expresion += token

        self.entrada_var.set(self.expresion)

    def _calcular(self):
        if not self.expresion:
            return

        entorno_seguro = {
            "__builtins__": None,
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "asin": self._asin,
            "acos": self._acos,
            "atan": self._atan,
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "factorial": lambda n: math.factorial(int(n)),
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
        }

        try:
            resultado = eval(self.expresion, entorno_seguro)
            if isinstance(resultado, float):
                resultado = round(resultado, 10)
                if resultado.is_integer():
                    resultado = int(resultado)
            self.expresion = str(resultado)
            self.entrada_var.set(self.expresion)
        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir entre cero.")
            self.expresion = ""
            self.entrada_var.set("0")
        except Exception as exc:
            messagebox.showerror("Error matemático", f"Expresión inválida.\nDetalle: {exc}")
            self.expresion = ""
            self.entrada_var.set("0")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = CalculadoraCientifica(ventana)
    ventana.mainloop()