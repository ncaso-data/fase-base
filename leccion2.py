def calcular_interes(prestamo, tasa_anual, meses):
    interes = prestamo * tasa_anual * meses / 12
    return interes

interes_ana = calcular_interes(8000, 0.25, 12)
interes_luis = calcular_interes(1500, 0.40, 6)

print(f"Interés Ana: S/ {interes_ana}")
print(f"Interés Luis: S/ {interes_luis}")
print(calcular_interes(1000, 0.12, 3))