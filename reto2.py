def calcular_cuota(prestamo, tasa_anual, meses):
    interes = prestamo*tasa_anual*meses/12
    total = prestamo+interes
    cuota_mensual = total/meses
    return(cuota_mensual)

cuotamLuis = calcular_cuota(1500,0.40,6)
cuotamRosa = calcular_cuota(2400,0.30,4)

print(f"La cuota mensual de Luis es de: {cuotamLuis}")
print(f"La cuota mensual de Rosa es de: {cuotamRosa}")