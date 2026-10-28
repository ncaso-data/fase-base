import csv
import sqlite3

# Base de datos temporal en memoria (se crea al ejecutar y desaparece al terminar)
conexion = sqlite3.connect(":memory:")


def convertir(valor):
    """Convierte texto del CSV a número si se puede; celda vacía -> NULL."""
    if valor == "":
        return None
    try:
        return int(valor)
    except ValueError:
        try:
            return float(valor)
        except ValueError:
            return valor


def cargar_tabla(nombre):
    """Lee data/<nombre>.csv y lo carga como tabla SQL."""
    # utf-8-sig elimina un carácter oculto (BOM) que a veces trae el inicio de un CSV
    with open(f"data/{nombre}.csv", encoding="utf-8-sig") as archivo:
        lector = csv.reader(archivo)
        columnas = next(lector)
        filas = [[convertir(v) for v in fila] for fila in lector]
    conexion.execute(f"CREATE TABLE {nombre} ({', '.join(columnas)})")
    marcadores = ", ".join("?" * len(columnas))
    conexion.executemany(f"INSERT INTO {nombre} VALUES ({marcadores})", filas)
    print(f"Tabla {nombre}: {len(filas)} filas cargadas")


def consultar(sql):
    """Ejecuta una consulta SQL e imprime el resultado como tabla."""
    cursor = conexion.execute(sql)
    columnas = [d[0] for d in cursor.description]
    print("\n" + " | ".join(columnas))
    print("-" * 40)
    for fila in cursor.fetchall():
        print(" | ".join(str(v) for v in fila))


for tabla in ["clientes", "prestamos", "pagos"]:
    cargar_tabla(tabla)

# ================== TUS CONSULTAS DEBAJO ==================

consultar("""
SELECT segmento, COUNT(cliente_id) AS n_clientes
FROM clientes
GROUP BY segmento;
""")

# Explorar: ver columnas y 3 filas de ejemplo de cada tabla
consultar("SELECT * FROM clientes LIMIT 3;")
consultar("SELECT * FROM prestamos LIMIT 3;")
consultar("SELECT * FROM pagos LIMIT 3;")

# E1 · Predicción: ____
consultar("""
SELECT distrito, COUNT(cliente_id) AS n_clientes
FROM clientes
GROUP BY distrito
HAVING COUNT(cliente_id) >= 6
ORDER BY n_clientes DESC;
""")


# E2 
consultar("""
SELECT plazo_meses, COUNT(prestamo_id) as n_prestamos, ROUND(AVG(monto),2) as monto_promedio
FROM prestamos
GROUP BY plazo_meses
HAVING count(prestamo_id) >= 18
ORDER BY plazo_meses asc; """)

# J0 · Predicción: consulta A =  filas; consulta B = ____ filas
consultar("""
SELECT 'clientes' AS tabla, (SELECT COUNT(*) FROM clientes) AS filas,
       (SELECT COUNT(*) FROM pragma_table_info('clientes')) AS columnas
UNION ALL
SELECT 'prestamos', (SELECT COUNT(*) FROM prestamos),
       (SELECT COUNT(*) FROM pragma_table_info('prestamos'))
UNION ALL
SELECT 'pagos', (SELECT COUNT(*) FROM pagos),
       (SELECT COUNT(*) FROM pragma_table_info('pagos'));
""")
# Consulta A: con coma
consultar("""
SELECT COUNT(*) AS filas
FROM prestamos, clientes;
""")

# Consulta B: con JOIN
consultar("""
SELECT COUNT(*) AS filas
FROM prestamos AS p
JOIN clientes AS c ON p.cliente_id = c.cliente_id;
""")

# J1 · Predicción: Masivo = 83 préstamos y 286000.0 de monto; Premium = 23 préstamos y 413000.0 de monto
consultar("""
SELECT c.segmento, COUNT(p.prestamo_id) AS n_prestamos, SUM(p.monto) AS monto_total
FROM prestamos AS p
JOIN clientes AS c ON p.cliente_id = c.cliente_id
GROUP BY c.segmento;
""")

# J2 . Predicción: No cambiará mucho, será parecido, en un rango de 1000 a 500  de diferencia el del premium sí cambiará
consultar("""
SELECT c.segmento, p.plazo_meses, count(p.prestamo_id) AS n_prestamos, round(avg(p.monto)) as monto_promedio
FROM prestamos AS p
JOIN clientes AS c ON p.cliente_id = c.cliente_id
Group by c.segmento, p.plazo_meses
ORDER BY c.segmento, p.plazo_meses;
""")