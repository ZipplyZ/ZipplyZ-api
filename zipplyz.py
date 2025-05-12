import os
import json
from time import sleep
from os import system
from collections import Counter

CARPETA_ARCHIVOS = os.path.join(os.path.expanduser("~"), "ZipplyZ")

class NodoHuffman:
    def __init__(self, caracter=None, frecuencia=0):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

class CompresorHuffman:
    def __init__(self):
        self.codigos = {}
        self.codigos_invertidos = {}

    def construir_diccionario_frecuencias(self, texto):
        return Counter(texto)

    def construir_arbol_huffman(self, frecuencias):
        nodos = [NodoHuffman(caracter, freq) for caracter, freq in frecuencias.items()]
        while len(nodos) > 1:
            nodos.sort(key=lambda x: x.frecuencia)
            izquierda = nodos.pop(0)
            derecha = nodos.pop(0)
            fusionado = NodoHuffman(frecuencia=izquierda.frecuencia + derecha.frecuencia)
            fusionado.izquierda = izquierda
            fusionado.derecha = derecha
            nodos.append(fusionado)
        return nodos[0] if nodos else None

    def generar_codigos(self, nodo, codigo_actual=""):
        if nodo is None:
            return
        if nodo.caracter is not None:
            self.codigos[nodo.caracter] = codigo_actual
            self.codigos_invertidos[codigo_actual] = nodo.caracter
            return
        self.generar_codigos(nodo.izquierda, codigo_actual + "0")
        self.generar_codigos(nodo.derecha, codigo_actual + "1")

    def codificar(self, texto):
        frecuencias = self.construir_diccionario_frecuencias(texto)
        raiz = self.construir_arbol_huffman(frecuencias)
        self.generar_codigos(raiz)
        texto_codificado = ''.join(self.codigos[caracter] for caracter in texto)
        return texto_codificado, self.codigos

    def decodificar(self, texto_codificado, codigos):
        codigos_invertidos = {v: k for k, v in codigos.items()}
        codigo_actual = ""
        texto_decodificado = ""
        for bit in texto_codificado:
            codigo_actual += bit
            if codigo_actual in codigos_invertidos:
                texto_decodificado += codigos_invertidos[codigo_actual]
                codigo_actual = ""
        return texto_decodificado

def limpiar_pantalla():
    system('cls' if os.name == 'nt' else 'clear')

def animacion_progreso(mensaje="Procesando"):
    print(f"{mensaje}", end="", flush=True)
    for _ in range(3):
        sleep(0.5)
        print(".", end="", flush=True)
    print()

def mostrar_logo():
    from colorama import init, Style
    init()

    def fg(code): return f'\033[38;5;{code}m'

    RESET       = Style.RESET_ALL
    PRIMARY_1   = fg(45)
    PRIMARY_2   = fg(255)
    UNDERSCORE  = fg(2)

    raw_logo = [
        r"_/\\\\\\\\\\\\\\\____________________________________/\\\\\\___________________/\\\\\\\\\\\\\\\_",
        r"_\////////////\\\____________________________________\////\\\__________________\////////////\\\__",
        r" ___________/\\\/____/\\\___/\\\\\\\\\____/\\\\\\\\\_____\/\\\_______/\\\__/\\\___________/\\\/___",
        r"  _________/\\\/_____\///___/\\\/////\\\__/\\\/////\\\____\/\\\______\//\\\/\\\__________/\\\/_____",
        r"   _______/\\\/________/\\\_\/\\\\\\\\\\__\/\\\\\\\\\\_____\/\\\_______\//\\\\\_________/\\\/_______",
        r"    _____/\\\/_________\/\\\_\/\\\//////___\/\\\//////______\/\\\________\//\\\________/\\\/_________",
        r"     ___/\\\/___________\/\\\_\/\\\_________\/\\\____________\/\\\_____/\\_/\\\_______/\\\/___________",
        r"      __/\\\\\\\\\\\\\\\_\/\\\_\/\\\_________\/\\\__________/\\\\\\\\\_\//\\\\/_______/\\\\\\\\\\\\\\\_",
        r"       _\///////////////__\///__\///__________\///__________\/////////___\////________\///////////////__"
    ]

    for i, line in enumerate(raw_logo):
        primary = PRIMARY_1 if i % 2 == 0 else PRIMARY_2
        colored = ''.join(
            UNDERSCORE + ch if ch == '_'
            else primary + ch
            for ch in line
        )
        print(colored + RESET)

def mostrar_instrucciones():
    print("\n INSTRUCCIONES Y RESTRICCIONES")
    print("────────────────────────────────────────────────────────")
    print("• El texto no debe estar vacío.")
    print("• Se permiten letras (mayúsculas y minúsculas), números, espacios y signos de puntuación.")
    print("• También puedes usar el signo de exclamación: !")
    print("• Caracteres especiales como acentos y ñ están permitidos.")
    print("• El nombre del archivo debe ser válido (sin \\ / : * ? \" < > |).")
    print("• Para el nombre de archivo solo: A–Z, a–z, 0–9, espacio y guión bajo (_).\n")
    print("────────────────────────────────────────────────────────\n")

def menu():
    compresor = CompresorHuffman()
    os.makedirs(CARPETA_ARCHIVOS, exist_ok=True)

    while True:
        limpiar_pantalla()
        mostrar_logo()
        print()

        print(" MENÚ PRINCIPAL")
        print("────────────────────────────────────────")
        print(" [  1  ] Comprimir texto y guardar")
        print(" [  2  ] Descomprimir archivo")
        print(" [  3  ] Ver archivos guardados")
        print(" [  4  ] Eliminar archivos guardados")
        print(" [  5  ] Salir")
        print("────────────────────────────────────────")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            print("\n[ COMPRESIÓN DE TEXTO ]")
            print("────────────────────────────────────────")
            print("• El texto no debe estar vacío.")
            print("• Se permiten letras, números, espacios y signos de puntuación.")
            print("• Caracteres especiales como acentos y ñ están permitidos.")
            print("• El nombre del archivo debe ser válido (sin \\ / : * ? \" < > |).\n")

            texto = input("Ingresar texto a comprimir:\n\n> ").strip()
            if not texto:
                print("¡Error! El texto no puede estar vacío.")
                input("Presiona Enter para continuar...")
                continue

            codificado, codigos = compresor.codificar(texto)
            animacion_progreso("Comprimiendo")
            nombre = input("Nombre del archivo a guardar (sin extensión): ").strip()
            if not all(c.isalnum() or c in (' ', '_') for c in nombre):
                print("¡Error! El nombre contiene caracteres no válidos.")
                input("Presiona Enter para continuar...")
                continue

            ruta = os.path.join(CARPETA_ARCHIVOS, f"{nombre}.txt")
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump({"codificado": codificado, "codigos": codigos}, f, ensure_ascii=False)

            print(f"\n✔ Texto comprimido y guardado como '{ruta}'")

            tamanio_original = len(texto.encode('utf-8'))
            tamanio_comprimido = len(codificado) // 8
            print(f"✔ Tamaño original: {tamanio_original} bytes")
            print(f"✔ Tamaño comprimido: {tamanio_comprimido} bytes")
            input("Presiona Enter para continuar...")

        elif opcion == "2":
            limpiar_pantalla()
            print("\n[ DESCOMPRESIÓN DE ARCHIVO ]")
            print("────────────────────────────────────────")
            print("• Solo se muestran archivos válidos previamente guardados.")
            print("• El archivo debe contener un texto comprimido con este sistema.\n")

            archivos = [f for f in os.listdir(CARPETA_ARCHIVOS) if f.endswith(".txt")]
            if not archivos:
                print("⚠ No hay archivos para descomprimir.")
                input("Presiona Enter para continuar...")
                continue

            print("Archivos disponibles:")
            for i, nombre in enumerate(archivos):
                print(f"[ {i + 1} ] {nombre}")

            try:
                idx = int(input("Selecciona el número del archivo: ")) - 1
                ruta = os.path.join(CARPETA_ARCHIVOS, archivos[idx])

                with open(ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)

                texto_decodificado = compresor.decodificar(datos["codificado"], datos["codigos"])
                animacion_progreso("Descomprimiendo")
                print("\nTexto descomprimido:")
                print(texto_decodificado)
                input("Presiona Enter para continuar...")
            except (IndexError, ValueError):
                print("¡Error! Opción inválida.")
                input("Presiona Enter para continuar...")

        elif opcion == "3":
            limpiar_pantalla()
            print("\n[ VER ARCHIVOS GUARDADOS ]")
            print("────────────────────────────────────────")
            archivos = [f for f in os.listdir(CARPETA_ARCHIVOS) if f.endswith(".txt")]
            if not archivos:
                print("⚠ No hay archivos guardados.")
            else:
                for nombre in archivos:
                    print(f"- {nombre}")
            input("Presiona Enter para continuar...")

        elif opcion == "4":
            limpiar_pantalla()
            print("\n[ ELIMINAR ARCHIVOS ]")
            print("────────────────────────────────────────")
            print("• Elimina de forma permanente un archivo comprimido.\n")

            archivos = [f for f in os.listdir(CARPETA_ARCHIVOS) if f.endswith(".txt")]
            if not archivos:
                print("⚠ No hay archivos para eliminar.")
                input("Presiona Enter para continuar...")
                continue
            print("Archivos disponibles:")
            for i, nombre in enumerate(archivos):
                print(f"[ {i + 1} ] {nombre}")

            try:
                idx = int(input("Selecciona el número del archivo a eliminar: ")) - 1
                ruta = os.path.join(CARPETA_ARCHIVOS, archivos[idx])
                os.remove(ruta)
                animacion_progreso("Eliminando")
                print(f"\n✔ Archivo '{archivos[idx]}' eliminado.")
                input("Presiona Enter para continuar...")
            except (IndexError, ValueError):
                print("¡Error! Opción inválida.")
                input("Presiona Enter para continuar...")

        elif opcion == "5":
            limpiar_pantalla()
            print("Gracias por usar a ZipplyZ!")
            print("────────────────────────────────────────")
            animacion_progreso("Saliendo del programa")
            sleep(1)
            break

        else:
            print("¡Opción inválida!")
            input("Presiona Enter para continuar...")


if __name__ == "__main__":
    menu()
