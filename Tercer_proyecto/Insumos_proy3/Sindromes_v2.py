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
    print("G(x):",g)
    # Multiplicación por x^(n-k) = x^4
    m_shifted = m_poly * galois.Poly([1] + [0]*4, field=GF)

    # División para obtener el residuo
    _, remainder = divmod(m_shifted, g)

    # Palabra codificada: mensaje desplazado + residuo
    code_poly = m_shifted + remainder
    return [int(c) for c in code_poly.coeffs]

alpha = GF.primitive_element
n, k, t = 15, 11, 2
g = galois.Poly.Roots([alpha**i for i in range(1, 2*t + 1)], field=GF)  # x^4 + 13x^3 + 12x^2 + 8x + 7

#   Utilidades compactas
def desc_to_asc(vec_desc):
    return list(reversed(vec_desc))

def asc_to_desc(vec_asc):
    return list(reversed(vec_asc))

def pos_to_power(idx_from_left: int) -> int:
    # índice (0..14) desde la IZQUIERDA -> potencia real (14..0)
    return (n - 1) - idx_from_left

def poly_text_from_desc(vec_desc, var="x"):
    a = desc_to_asc(vec_desc)  # c0..c14
    parts = []
    for p in range(len(a) - 1, -1, -1):
        c = a[p]
        if c == 0: continue
        parts.append(f"{c}" if p == 0 else (f"{c}{var}" if p == 1 else f"{c}{var}^{p}"))
    return " + ".join(parts) if parts else "0"

def remainder_key_str(rem_poly, var="x"):
    # clave: 'a3x^3 + a2x^2 + a1x + a0'  (con a0=S1,...,a3=S4)
    if rem_poly.degree == -1:
        return "0"
    coeffs_desc = list(rem_poly.coeffs)           # [a_d, ..., a_0]
    coeffs_asc4 = [0, 0, 0, 0]
    for i, c in enumerate(reversed(coeffs_desc)):
        if i < 4: coeffs_asc4[i] = int(c)
    a0, a1, a2, a3 = coeffs_asc4
    parts = []
    if a3: parts.append(f"{a3}{var}^3")
    if a2: parts.append(f"{a2}{var}^2")
    if a1: parts.append(f"{a1}{var}")
    if a0 or not parts: parts.append(f"{a0}")
    return " + ".join(parts)

def error_str_to_asc(err_str, n=15):
    # '5x^11 + 3x^2' -> vector ascendente (c0..c14)
    e = GF.Zeros(n)
    s = err_str.replace(" ", "")
    if s != "0":
        for term in s.split("+"):
            if "x^" in term:
                c, p = term.split("x^"); c = int(c); p = int(p)
            elif "x" in term:
                c = int(term[:-1]); p = 1
            else:
                c = int(term); p = 0
            e[p] += GF(c)
    return [int(x) for x in e]

def parse_error_terms(err_str):
    # '5x^11 + 3x^2' -> [(coef, potencia), ...]
    s = err_str.replace(" ", "")
    if s in ("0", ""): return []
    terms = []
    for term in s.split("+"):
        if "x^" in term:
            c, p = term.split("x^"); terms.append((int(c), int(p)))
        elif "x" in term:
            terms.append((int(term[:-1]), 1))
        else:
            terms.append((int(term), 0))
    return terms

def remainder_key_from_desc(received_desc):
    # r(x) en 'asc', dividir por g(x), tomar residuo y formatear clave
    R_poly = galois.Poly(GF(desc_to_asc(received_desc)), field=GF, order="asc")
    _, rem = divmod(R_poly, g)
    return remainder_key_str(rem)


#   Tabla OFFLINE: residuo → error  (peso ≤ 2)
def build_offline_remainder_table():
    table = {}
    nonzero = [int(x) for x in GF.Range(1, 16)]  # 1..15

    # Peso 1
    for idx in range(n):
        p = pos_to_power(idx)
        for a in nonzero:
            e_asc = GF.Zeros(n); e_asc[p] = GF(a)
            E_poly = galois.Poly(e_asc, field=GF, order="asc")
            _, rem = divmod(E_poly, g)
            key = remainder_key_str(rem)
            val = f"{a}x^{p}" if p > 1 else (f"{a}x" if p == 1 else f"{a}")
            table.setdefault(key, val)

    # Peso 2
    for i in range(n):
        p1 = pos_to_power(i)
        for j in range(i+1, n):
            p2 = pos_to_power(j)
            for a in nonzero:
                for b in nonzero:
                    e_asc = GF.Zeros(n)
                    e_asc[p1] = GF(a); e_asc[p2] += GF(b)
                    E_poly = galois.Poly(e_asc, field=GF, order="asc")
                    _, rem = divmod(E_poly, g)
                    key = remainder_key_str(rem)
                    part1 = f"{a}x^{p1}" if p1 > 1 else (f"{a}x" if p1 == 1 else f"{a}")
                    part2 = f"{b}x^{p2}" if p2 > 1 else (f"{b}x" if p2 == 1 else f"{b}")
                    table.setdefault(key, f"{part1} + {part2}")
    table["0"] = "0"
    return table


#   Corrección vía tabla OFFLINE (residuo → error)
def correct_with_remainder_lookup_desc(received_desc, tabla_residuos):
    key = remainder_key_from_desc(received_desc)
    err_str = tabla_residuos.get(key)
    if err_str is None:
        raise ValueError(f"Residuo {key} no mapeado (posible >2 errores o convención distinta).")
    # c = r - E  (en GF(2^4), resta = suma)
    r_asc = GF(desc_to_asc(received_desc))
    e_asc = GF(error_str_to_asc(err_str))
    c_asc = r_asc + e_asc
    return asc_to_desc([int(x) for x in c_asc]), err_str, key

# Corrección “visibilizada” con XOR
def xor_correct_desc(received_desc, err_str):
    corrected = received_desc.copy()
    for coef, power in parse_error_terms(err_str):
        pos_izq = 14 - power
        corrected[pos_izq] = corrected[pos_izq] ^ coef 
    return corrected


#   Demostracion
if __name__ == "__main__":
    # 1) Codificar mensaje de ejemplo 
    m = [7,5,2,13,6,3,4,7,11,6,0]
    codificado_desc = codi_rs(m)
    print("\nCodigo enviado:")
    print("Código RS(15,11) (DESC):", codificado_desc)

    # 2) Construir tabla OFFLINE (residuo -> error)
    print("\nConstruyendo tabla OFFLINE (residuo -> error)…")
    tabla_res = build_offline_remainder_table()
    print("Entradas (incluye 0):", len(tabla_res))

    # 3) Dos recibidos inventados (1 y 2 símbolos)
    #    A: E(x) = 3x^13
    rA = codificado_desc.copy()
    rA[14 - 13] ^= 3

    #    B: E(x) = 5x^4 + 12x^9
    rB = codificado_desc.copy()
    rB[14 - 4]  ^= 5
    rB[14 - 9]  ^= 12

    # 4) Mostrar y corregir
    for tag, r in (("A (1 símbolo: 3x^13)", rA), ("B (2 símbolos: 5x^4 + 12x^9)", rB)):
        print(f"\n—— Caso {tag} ——")
        print("Recibido (DESC):", r)
        print("Recibido (texto):", poly_text_from_desc(r))

        # Detección: residuo como llave y error estimado
        key = remainder_key_from_desc(r)
        err = tabla_res.get(key, "No encontrado")
        print("Residuo mod g(x):", key)
        print("Error estimado:", err)

        # Corrección (dos formas equivalentes)
        c_hat_desc, _, _ = correct_with_remainder_lookup_desc(r, tabla_res)   # suma en GF(2^4)
        c_hat_desc_xor = xor_correct_desc(r, err)                             # XOR bit a bit (visible)

        print("Corregido (GF): ", c_hat_desc)
        print("Corregido (XOR):", c_hat_desc_xor)
        print("¿Corrección exacta?:", c_hat_desc == codificado_desc == c_hat_desc_xor)
