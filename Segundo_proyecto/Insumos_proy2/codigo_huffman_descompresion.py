import os
import sys
import getopt
import csv
from math import log2

# =========================================================
# 1. PARÁMETROS DE ENTRADA Y CONFIGURACIÓN
# =========================================================
file_full_path = "~/Documents/TEC/IIS_25/comu/Comunicaciones_2/Segundo_proyecto/Insumos_proy2" 
file_split_path = file_full_path.split("/")

def myfunc(argv):
    global file_full_path, file_split_path
    arg_help = "{0} -i <input>".format(argv[0])
    
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

# Árbol binario
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def insert_in_tree(raiz, ruta, valor):
    if(len(ruta)==1):
        if(ruta=='0'):
            raiz.left = valor;
        else:
            raiz.right = valor;
    else:
        if(ruta[0]=='0'):
            #if type(raiz.left) is int:
            if(raiz.left==None):
                raiz.left = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.left,ruta,valor);
        else:
            #if type(raiz.right) is int:
            if(raiz.right==None):
                raiz.right = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.right,ruta,valor);

# =========================================================
# 3. DEFINICIÓN DE NODOS PARA EL ÁRBOL DE HUFFMAN
# =========================================================
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)
    
def insert_in_tree(raiz, ruta, valor):
    if(len(ruta)==1):
        if(ruta=='0'):
            raiz.left = valor;
        else:
            raiz.right = valor;
    else:
        if(ruta[0]=='0'):
            #if type(raiz.left) is int:
            if(raiz.left==None):
                raiz.left = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.left,ruta,valor);
        else:
            #if type(raiz.right) is int:
            if(raiz.right==None):
                raiz.right = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.right,ruta,valor);

# =========================================================
# 4. CALCULO DE FRECUENCIAS
# =========================================================
prob_unit = 1 / len(string)
freq = {}

for c in string:
    if c in freq:
        freq[c] += prob_unit
    else:
        freq[c] = prob_unit

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
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is int:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

huffmanCode = huffman_code_tree(nodes[0][0])

print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))

# =========================================================
# 7. ESTADÍSTICAS DE COMPRESIÓN
# =========================================================
print("\n" + "="*60)
print("ESTADÍSTICAS DE COMPRESIÓN HUFFMAN")
print("="*60)

# 1. Entropía
entropia = 0
for char, prob in freq:
    if prob > 0:
        entropia -= prob * log2(prob)

# 2. Longitud media
longitud_media = 0
for char, prob in freq:
    longitud_media += prob * len(huffmanCode[char])

# 3. Varianza
varianza = 0
for char, prob in freq:
    varianza += prob * (len(huffmanCode[char]) - longitud_media) ** 2

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
    print(f"   {chr(char) if 32 <= char <= 126 else ' ':<2}    |"
          f"   {prob:.4f}    |"
          f"     {len(huffmanCode[char]):<2}    |"
          f" {huffmanCode[char]}")

# =========================================================
# 8. COMPRESIÓN: VECTOR BINARIO Y BYTES
# =========================================================
binary_string = []
for c in string:
    binary_string += huffmanCode[c]

compressed_length_bit = len(binary_string)

# Padding
if compressed_length_bit % 8 > 0:
    for i in range(8 - len(binary_string) % 8):
        binary_string += '0'

# Bytes
byte_string = "".join([str(i) for i in binary_string])
byte_string = [byte_string[i:i+8] for i in range(0, len(byte_string), 8)]
byte_data = [int(b, 2) for b in byte_string]

# =========================================================
# 9. GUARDAR ARCHIVO BINARIO
# =========================================================
with open(file_huffman_comprimido, "wb") as f:
    f.write(bytearray(byte_data))

# =========================================================
# 10. GUARDAR DICCIONARIO CSV
# =========================================================
with open(ruta_diccionario, 'w', newline='') as csvfile:
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


# =========================================================
# 12. Descompresión
# =========================================================
csvfile = open(ruta_diccionario, 'r')
reader = csv.reader(csvfile)
bits_a_leer = None;
diccionario = dict();
for row in reader:
    if(bits_a_leer==None) :
        bits_a_leer = int(row[0]);
    else:
        diccionario.update({int(row[0]): row[1]})
Decoding = NodeTree(None,None);
for entrada in diccionario:
    insert_in_tree( Decoding,diccionario[entrada], entrada)

nodo = Decoding;
data_estimated = [];
for i in range(compressed_length_bit):
    (l,r) = nodo.children();
    #print([i,binary_string[i]])
    if(binary_string[i]=='1'):
        nodo = r;
    else:
        nodo = l;

    if type(nodo) is int:
        data_estimated.append(nodo)
        #print([i,nodo])
        nodo = Decoding;

# =========================================================
# 13. Verificación de los datos estimados
# =========================================================
if data_estimated == string:
    print("Verificación exitosa: los datos descomprimidos coinciden con los originales.")
else:
    print("Verificación fallida: los datos descomprimidos NO coinciden con los originales.")
    print(f"Original:     {string[:50]}...")
    print(f"Descomprimido:{data_estimated[:50]}...")

# =========================================================
# 14. Escritura de datos estimados
# =========================================================
with open(recovered_path, "wb") as f:
    f.write(bytearray(data_estimated))

print("Archivo recuperado guardado en:", recovered_path)