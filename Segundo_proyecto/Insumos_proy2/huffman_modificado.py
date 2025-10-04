import os
import sys
import getopt
import csv
from math import log2

# Parametros de entrada y ayuda:
file_full_path = "C:/Users/Asus/Downloads/Insumos_proy2/Insumos_proy2/solo_abc_cien.txt" 
file_split_path = file_full_path.split("/")
def myfunc(argv):
    global file_full_path, file_split_path
    arg_output = ""
    arg_user = ""
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
            file_split_path = os.path.normpath(file_full_path)
            file_split_path = os.path.split(file_split_path)


if __name__ == "__main__":
    myfunc(sys.argv)


file_huffman_comprimido = file_full_path+".huffman"
ruta_diccionario = file_full_path+".diccionario.csv"
recovered_path = os.path.join(file_split_path[0], "recovered_"+file_split_path[1]);
#-----------------------------------------------------
# Algorithmo de compresión de huffman
#-----------------------------------------------------
#Apertura y lectura del archivo
string=[];
with open(file_full_path, "rb") as f:
    while (byte := f.read(1)):
        # Do stuff with byte.
        int_val = int.from_bytes(byte, "big")
        string.append(int_val)

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


# Función principal del algoritmo de Huffman
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is int:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d
    

# calculo de frecuencias y probabilidades
prob_unit = 1/len(string)
freq = {}
for c in string:
    if c in freq:
        freq[c] += prob_unit
    else:
        freq[c] = prob_unit

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    #print(nodes)
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffman_code_tree(nodes[0][0])

print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))

############################################################## Modificación ################################################################################


print("\n" + "="*60)
print("ESTADÍSTICAS DE COMPRESIÓN HUFFMAN")
print("="*60)

# 1. Cálculo de la Entropía de la fuente
entropia = 0
for char, prob in freq:
    if prob > 0:
        entropia -= prob * log2(prob)

# 2. Cálculo de la Longitud media del código Huffman
longitud_media = 0
for char, prob in freq:
    longitud_media += prob * len(huffmanCode[char])

# 3. Cálculo de la Varianza del código Huffman
varianza = 0
for char, prob in freq:
    varianza += prob * (len(huffmanCode[char]) - longitud_media) ** 2

# 4. Eficiencia de la codificación original (8 bits por carácter)
longitud_original = 8  # ASCII usa 8 bits por carácter
eficiencia_original = (entropia / longitud_original) * 100

# 5. Eficiencia del nuevo código Huffman
eficiencia_huffman = (entropia / longitud_media) * 100

# 6. Cálculo de la tasa de compresión
tasa_compresion = (1 - (longitud_media / longitud_original)) * 100

# Mostrar resultados
print(f"\nENTROPÍA DE LA FUENTE:")
print(f"  H(X) = {entropia:.4f} bits/símbolo")

print(f"\nLONGITUD MEDIA DEL CÓDIGO HUFFMAN:")
print(f"  L = {longitud_media:.4f} bits/símbolo")

print(f"\nVARIANZA DEL CÓDIGO HUFFMAN:")
print(f"  σ² = {varianza:.4f}")

print(f"\nEFICIENCIAS:")
print(f"  Codificación original (8-bit ASCII): {eficiencia_original:.2f}%")
print(f"  Codificación Huffman: {eficiencia_huffman:.2f}%")

print(f"\nTASA DE COMPRESIÓN:")
print(f"  Reducción: {tasa_compresion:.2f}%")

# Mostrar detalles por símbolo
print(f"\nDETALLE POR SÍMBOLO:")
print(" Símbolo | Probabilidad | Longitud | Código Huffman")
print("---------|--------------|-----------|----------------")
for char, prob in freq:
    print(f"   {chr(char) if 32 <= char <= 126 else ' ':<2}    |"
          f"   {prob:.4f}    |"
          f"     {len(huffmanCode[char]):<2}    |"
          f" {huffmanCode[char]}")

