# Description: this file handles reading from a file or terminal


#Leer las cadenas desde un archivo
def read_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        reader = file.read()
    file.close()
    return reader


#Leer las cadenas desde la terminal
def read_from_terminal():
    print("Ingresa el código línea por línea. Escribe 'EOF' para terminar:")
    lines = []
    while True:
        line = input("> ")
        if line.strip().upper() == "EOF":
            break
        lines.append(line)
    return "\n".join(lines)