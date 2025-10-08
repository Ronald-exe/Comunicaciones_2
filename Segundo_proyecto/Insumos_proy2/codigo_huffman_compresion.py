import os
import sys
import getopt
import csv
from math import log2

# =========================================================
# CONFIGURACIÓN DE CODIFICACIÓN (UTF-8 PARA WINDOWS)
# =========================================================
# Evita errores con caracteres griegos o acentuados
sys.stdout.reconfigure(encoding='utf-8')

# =========================================================
# 1. PARÁMETROS DE ENTRADA Y CONFIGURACIÓN
# =========================================================
file_full_path = "C:/Users/esteb/Documents/Decimo_semestre/Comu_2/Comunicaciones_2/Segundo_proyecto/Insumos_proy2/solo_abc_cien.txt" 
file_split_path = file_full_path.split("/")

def myfunc(argv):
    """Procesa argumentos de línea de comando"""
    global file_full_path, file_split_path
    arg_help = f"{argv[0]} -i <input>"
    
    try:
        opts, args = getopt.getopt(argv[1:], "hi:", ["help", "input="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  
            sys.exit(2)
        elif opt in ("-i", "--input"):
            file_full_path = arg
            file_split_path = os.path.split(os.path.normpath(file_full_path))

if __name__ == "__main__":
    myfunc(sys.argv)

# Archivos de salida
file_huffman_comprimido = file_full_path + ".huffman"
ruta_diccionario = file_full_path + ".diccionario.csv"
recovered_path = os.path.join(file_split_path[0], "recovered_" + file_split_path[1])

# =========================================================
# 2. LECTURA DEL ARCHIVO ORIGINAL
# =========================================================
string = []
with open(file_full_path, "rb") as f:
    while (byte := f.read(1)):
        int_val = int.from_bytes(byte, "big")
        string.append(int_val)

if len(string) == 0:
    print("El archivo está vacío. No se puede comprimir.")
    sys.exit(0)

# =========================================================
# 3. DEFINICIÓN DE NODOS PARA EL ÁRBOL DE HUFFMAN
# =========================================================
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def __str__(self):
        return f'{self.left}_{self.right}'

# =========================================================
# 4. CÁLCULO DE FRECUENCIAS
# =========================================================
prob_unit = 1 / len(string)
freq = {}

for c in string:
    freq[c] = freq.get(c, 0) + prob_unit

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
nodes = freq.copy()

# =========================================================
# 5. CONSTRUCCIÓN DEL ÁRBOL DE HUFFMAN
# =========================================================
while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

# =========================================================
# 6. GENERACIÓN DE CÓDIGOS DE HUFFMAN
# =========================================================
def huffman_code_tree(node, binString=''):
    if isinstance(node, int):
        return {node: binString}
    (l, r) = node.children()
    d = {}
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d

huffmanCode = huffman_code_tree(nodes[0][0])

print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(f' {char!r:4} | {huffmanCode[char]:>12}')

# =========================================================
# 7. ESTADÍSTICAS DE COMPRESIÓN
# =========================================================
print("\n" + "="*60)
print("ESTADÍSTICAS DE COMPRESIÓN HUFFMAN")
print("="*60)

# 1. Entropía
entropia = -sum(prob * log2(prob) for _, prob in freq if prob > 0)

# 2. Longitud media
longitud_media = sum(prob * len(huffmanCode[char]) for char, prob in freq)

# 3. Varianza
varianza = sum(prob * (len(huffmanCode[char]) - longitud_media) ** 2 for char, prob in freq)

# 4. Eficiencia
longitud_original = 8  # ASCII
eficiencia_original = (entropia / longitud_original) * 100
eficiencia_huffman = (entropia / longitud_media) * 100

# 5. Tasa de compresión
tasa_compresion = (1 - (longitud_media / longitud_original)) * 100

# Mostrar resultados
print(f"\nENTROPÍA DE LA FUENTE: H(X) = {entropia:.4f} bits/símbolo")
print(f"LONGITUD MEDIA DEL CÓDIGO HUFFMAN: L = {longitud_media:.4f} bits/símbolo")
print(f"VARIANZA DEL CÓDIGO HUFFMAN: σ² = {varianza:.4f}")
print(f"EFICIENCIAS: Original = {eficiencia_original:.2f}%, Huffman = {eficiencia_huffman:.2f}%")
print(f"TASA DE COMPRESIÓN: Reducción = {tasa_compresion:.2f}%")

print(f"\nDETALLE POR SÍMBOLO:")
print(" Símbolo | Probabilidad | Longitud | Código Huffman")
print("---------|--------------|-----------|----------------")
for char, prob in freq:
    simbolo = chr(char) if 32 <= char <= 126 else ' '
    print(f"   {simbolo:<2}    |   {prob:.4f}    |     {len(huffmanCode[char]):<2}    | {huffmanCode[char]}")

# =========================================================
# 8. COMPRESIÓN: VECTOR BINARIO Y BYTES
# =========================================================
binary_string = ''.join(huffmanCode[c] for c in string)
compressed_length_bit = len(binary_string)

# Padding
if compressed_length_bit % 8 != 0:
    binary_string += '0' * (8 - compressed_length_bit % 8)

# Conversión a bytes
byte_string = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
byte_data = [int(b, 2) for b in byte_string]

# =========================================================
# 9. GUARDAR ARCHIVO BINARIO
# =========================================================
with open(file_huffman_comprimido, "wb") as f:
    f.write(bytearray(byte_data))

# =========================================================
# 10. GUARDAR DICCIONARIO CSV
# =========================================================
with open(ruta_diccionario, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([str(compressed_length_bit), "bits"])
    for entrada in huffmanCode:
        writer.writerow([str(entrada), huffmanCode[entrada]])

# =========================================================
# 11. TAMAÑOS Y TASA DE COMPRESIÓN
# =========================================================
original_size = len(string)
compressed_size = len(byte_data)
compression_ratio = (original_size / compressed_size) if compressed_size > 0 else 0

print("\n--------------------------")
print("Tamaño original:", original_size, "bytes")
print("Tamaño comprimido:", compressed_size, "bytes")
print("Tasa de compresión:", compression_ratio)
print("Archivo comprimido guardado en:", file_huffman_comprimido)
print("Diccionario guardado en:", ruta_diccionario)
