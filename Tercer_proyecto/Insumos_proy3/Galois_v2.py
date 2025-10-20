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



import numpy as np
import galois

# Definimos el campo GF(2^4) con polinomio irreducible x^4 + x + 1 (0b10011)
GF = galois.GF(2**4, irreducible_poly=galois.Poly.Int(0b10011))

def codi_rs(mensaje):
    # Validación de entrada
    if len(mensaje) != 11:
        raise ValueError("El mensaje debe tener longitud 11.")
    if any((x < 0 or x >= 16) for x in mensaje):
        raise ValueError("Todos los símbolos deben estar en el rango [0,15] para GF(2^4).")

    # Convertir el mensaje al campo GF(2^4)
    m = GF(mensaje)
    m_poly = galois.Poly(m, field=GF)

    # Construcción del polinomio generador g(x) con raíces α^1 a α^4
    alpha = GF.primitive_element
    roots = [alpha**i for i in range(1, 5)]
    g = galois.Poly.Roots(roots, field=GF)

    # Multiplicación por x^(n-k) = x^4
    m_shifted = m_poly * galois.Poly([1] + [0]*4, field=GF)

    # División para obtener el residuo
    _, remainder = divmod(m_shifted, g)

    # Palabra codificada: mensaje desplazado + residuo
    code_poly = m_shifted + remainder
    return [int(c) for c in code_poly.coeffs]

m = [7,5,2,13,6,3,4,7,11,6,0]
codificado = codi_rs(m)
print("Código RS(15,11):", codificado)