cliente = "Ana"
monto = 8000
tasa_anual = 0.25
plazo_meses = 6

interes = monto * tasa_anual * plazo_meses / 12
total = monto + interes

print(f"Cliente: {cliente}")
print(f"Interés: S/ {interes}")
print(f"Total a pagar: S/ {total}")
print(type(cliente), type(monto), type(tasa_anual))