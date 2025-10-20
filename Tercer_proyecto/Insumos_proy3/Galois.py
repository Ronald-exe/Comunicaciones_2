import numpy as np
import galois

GF = galois.GF(2**4, irreducible_poly=galois.Poly.Int(0b10011))

# Tabla de suma
add_table = np.zeros((16,16), dtype=int)
mul_table = np.zeros((16,16), dtype=int)

for i in range(16):
    for j in range(16):
        add_table[i,j] = int(GF(i) + GF(j))
        mul_table[i,j] = int(GF(i) * GF(j))

print("Tabla de Suma GF(16):")
print(add_table)
print("\nTabla de Multiplicación GF(16):")
print(mul_table)


