import numpy as np
import galois

# 1. Configurar el campo de Galois para RS(15,11)
# RS(15,11) usa símbolos de 4 bits (2^4 = 16 elementos)
# El polinomio irreducible para n=4 es X^4 + X + 1 (10011 en binario)
GF = galois.GF(2**4, irreducible_poly="x^4 + x + 1")
print("Campo de Galois GF(2^4) con polinomio irreducible x^4 + x + 1")
print(f"Orden del campo: {GF.order}")
print(f"Polinomio irreducible: {GF.irreducible_poly}")
print()

# 2. Verificar el polinomio generador
# Para RS(15,11) con b=1, el polinomio generador tiene raíces en a^1, a^2, ..., a^4
# donde a es el elemento primitivo (2 en nuestro campo)
# El polinomio generador es: g(x) = (x - a^1)(x - a^2)(x - a^3)(x - a^4)

# Elemento primitivo (a = 2 en nuestro campo)
alpha = GF(2)
print(f"Elemento primitivo a = {alpha}")

# Raíces del polinomio generador
roots = [alpha**i for i in range(1, 5)]  # a^1, a^2, a^3, a^4
print(f"Raices del polinomio generador: {roots}")

# Construir el polinomio generador a partir de las raíces
g = galois.Poly.Roots(roots, field=GF)
print(f"Polinomio generador calculado: {g}")

# Mostrar los coeficientes en diferentes formatos
print(f"Coeficientes del polinomio generador: {g.coeffs}")
print(f"Polinomio generador en formato expandido: {g}")
print()

# 3. Verificar las propiedades del polinomio generador
print("Verificacion del polinomio generador:")
print(f"Grado del polinomio generador: {g.degree}")
print(f"Numero de raices esperadas: 4")
print(f"Numero de raices encontradas: {len(roots)}")

# Verificar que efectivamente las raíces anulan el polinomio
print("\nVerificacion de raices:")
for i, root in enumerate(roots, 1):
    evaluation = g(root)
    print(f"g(a^{i}) = {evaluation} {'(CORRECTO)' if evaluation == 0 else '(ERROR)'}")
print()

# 4. Información adicional sobre el código RS
n = 15
k = 11
t = (n - k) // 2
print(f"Parametros del codigo RS(15,11):")
print(f"n = {n}, k = {k}, t = {t}")
print(f"Simbolos de mensaje: {k}")
print(f"Simbolos de redundancia: {n - k}")
print(f"Simbolos corregibles: {t}")
print(f"Capacidad de correccion: {t * 4} bits")
print()
