import tkinter as tk
from tkinter import filedialog, messagebox, font
from lark import Lark, exceptions
from reader import AST
from semantic import SemanticAnalyzer
from ensamblador import ensamblador

class CompiladorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compilador")
        self.geometry("1100x650")
        self.configure(bg="#fefae0")
        self.fuente_actual = tk.StringVar(value="Consolas")
        self.crear_menu()
        self.crear_encabezado()
        self.crear_botones()
        self.crear_editor()
        self.crear_consola()
        self.init_parser()

    def init_parser(self):
        try:
            with open("grammar.lark", "r", encoding="utf-8") as f:
                grammar = f.read()
            self.parser = Lark(grammar, parser="lalr", transformer=AST(), start='start')
            self.raw_parser = Lark(grammar, parser="lalr", start='start')  # sin transformer para ensamblador
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo 'grammar.lark' no encontrado.")
            self.quit()

    def crear_menu(self):
        menubar = tk.Menu(self)
        fuente_menu = tk.Menu(menubar, tearoff=0)
        for f in sorted(set(font.families())):
            fuente_menu.add_radiobutton(label=f, variable=self.fuente_actual, command=self.cambiar_fuente)
        menubar.add_cascade(label="Fuente", menu=fuente_menu)
        self.config(menu=menubar)

    def cambiar_fuente(self):
        nueva = self.fuente_actual.get()
        self.editor_texto.configure(font=(nueva, 13))

    def crear_encabezado(self):
        tk.Label(self, text="COMPILADOR", font=("Helvetica", 16, "bold"), bg="#fefae0", fg="#606c38").pack()
        tk.Label(self, text="Equipo 04", font=("Helvetica", 12), bg="#fefae0", fg="#bc6c25").pack()

    def crear_botones(self):
        frame = tk.Frame(self, bg="#fefae0")
        frame.pack(pady=5)

        # Botones principales
        botones = [
            ("Nuevo", self.abrir_nuevo),
            ("Abrir", self.abrir_archivo),
            ("Guardar", self.guardar_archivo),
            ("Compilar", self.compilar_completo),
            ("Parsing Tree", self.ver_parse_tree),
            ("Generar Ensamblador", self.generar_ensamblador)
        ]

        for texto, accion in botones:
            tk.Button(frame, text=texto, width=16, bg="#ccd5ae", command=accion).pack(side=tk.LEFT, padx=5)


    def crear_editor(self):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))
        self.editor_texto = tk.Text(frame, wrap=tk.NONE, font=(self.fuente_actual.get(), 13), height=20)
        self.editor_texto.pack(fill=tk.BOTH, expand=True)

    def crear_consola(self):
        self.consola = tk.Text(self, height=10, bg="#e9edc9", font=("Consolas", 11))
        self.consola.pack(fill=tk.X, padx=10, pady=5)

    def accion_boton(self, nombre):
        if nombre == "Abrir":
            self.abrir_archivo()
        elif nombre == "Guardar":
            self.guardar_archivo()
        elif nombre == "Nuevo":
            self.editor_texto.delete("1.0", tk.END)
        elif nombre == "Compilar":
            self.compilar()

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos", "*.comp *.txt"), ("Todos", "*.*")])
        if ruta:
            with open(ruta, "r", encoding="utf-8") as f:
                self.editor_texto.delete("1.0", tk.END)
                self.editor_texto.insert(tk.END, f.read())

    def guardar_archivo(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".comp")
        if ruta:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(self.editor_texto.get("1.0", tk.END))

    def abrir_nuevo(self):
        self.editor_texto.delete("1.0", tk.END)
        self.consola.delete("1.0", tk.END)


    def compilar_completo(self):
        codigo = self.editor_texto.get("1.0", tk.END).strip()
        self.consola.delete("1.0", tk.END)

        try:
            ast = self.parser.parse(codigo)
            sem = SemanticAnalyzer()
            errores = sem.analyze(ast[1])

            if errores:
                self.consola.insert(tk.END, "Errores semánticos:\n")
                for err in errores:
                    self.consola.insert(tk.END, f"{err}\n")
                return

            arbol = self.raw_parser.parse(codigo)
            generador = ensamblador()
            generador.transform(arbol)
            salida = generador.get_output()

            self.consola.insert(tk.END, "AST:\n")
            self.consola.insert(tk.END, f"{ast}\n\n")
            self.consola.insert(tk.END, "Código Ensamblador:\n")
            self.consola.insert(tk.END, salida)

        except exceptions.UnexpectedCharacters as e:
            self.consola.insert(tk.END, f"Error léxico:\n{e}")
        except exceptions.UnexpectedInput as e:
            self.consola.insert(tk.END, f"Error sintáctico:\n{e}")
        except Exception as e:
            self.consola.insert(tk.END, f"Error general:\n{e}")

    def ver_parse_tree(self):
        codigo = self.editor_texto.get("1.0", tk.END).strip()
        self.consola.delete("1.0", tk.END)

        try:
            arbol = self.raw_parser.parse(codigo)
            self.consola.insert(tk.END, "Árbol de Parseo (Pretty):\n")
            self.consola.insert(tk.END, arbol.pretty())
        except Exception as e:
            self.consola.insert(tk.END, f"Error al generar el árbol:\n{e}")

    def generar_ensamblador(self):
        codigo = self.editor_texto.get("1.0", tk.END).strip()
        self.consola.delete("1.0", tk.END)

        try:
            arbol = self.raw_parser.parse(codigo)
            generador = ensamblador()
            generador.transform(arbol)
            salida = generador.get_output()
            self.consola.insert(tk.END, "Código Ensamblador:\n")
            self.consola.insert(tk.END, salida)
        except Exception as e:
            self.consola.insert(tk.END, f"Error al generar ensamblador:\n{e}")

if __name__ == "__main__":
    app = CompiladorGUI()
    app.mainloop()
