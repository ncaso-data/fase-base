Cliente = "Luis"
Tasa_anual= 0.4
Meses = 6
Préstamo = 1500

Interés= Préstamo*Tasa_anual*Meses/12
Total = Préstamo + Interés
CuotaMensual = Total/Meses
print(f"Cliente: {Cliente}")
print(f"Interés: {Interés}")
print(f"Total: {Total}")
print(f"Cuota Mensual: {CuotaMensual}")