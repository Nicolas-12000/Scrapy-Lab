"""
Análisis SQL sobre la tabla productos.

Ejecuta cada consulta y la imprime formateada como tabla.
"""
import pandas as pd

from database.connection import get_connection

# ------------------------------------------------------------------ #
# Utilidad                                                             #
# ------------------------------------------------------------------ #

def run_query(sql: str, title: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query(sql, conn)
    conn.close()
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(df.to_string(index=False))
    return df


# ------------------------------------------------------------------ #
# Consultas                                                            #
# ------------------------------------------------------------------ #

Q1 = """
-- 1. Precio promedio por categoría
SELECT
    categoria,
    ROUND(AVG(precio_actual)::NUMERIC, 2) AS precio_promedio
FROM productos
WHERE precio_actual IS NOT NULL
GROUP BY categoria
ORDER BY precio_promedio DESC;
"""

Q2 = """
-- 2. Producto más costoso dentro de cada categoría
SELECT DISTINCT ON (categoria)
    categoria,
    nombre,
    precio_actual
FROM productos
WHERE precio_actual IS NOT NULL
ORDER BY categoria, precio_actual DESC;
"""

Q3 = """
-- 3. Cantidad de productos con envío gratis
SELECT
    envio_gratis,
    COUNT(*) AS cantidad
FROM productos
GROUP BY envio_gratis
ORDER BY envio_gratis DESC;
"""

Q4 = """
-- 4. Ciudad/ubicación con mayor número de publicaciones
SELECT
    COALESCE(NULLIF(TRIM(ubicacion), ''), 'Sin ubicación') AS ubicacion,
    COUNT(*) AS publicaciones
FROM productos
GROUP BY ubicacion
ORDER BY publicaciones DESC
LIMIT 10;
"""

Q5 = """
-- 5. Descuento promedio por categoría
SELECT
    categoria,
    ROUND(AVG(descuento)::NUMERIC, 1) AS descuento_promedio_pct
FROM productos
WHERE descuento IS NOT NULL
GROUP BY categoria
ORDER BY descuento_promedio_pct DESC;
"""

Q6 = """
-- 6. Cantidad de productos por encima del precio promedio general
SELECT COUNT(*) AS sobre_promedio
FROM productos
WHERE precio_actual > (
    SELECT AVG(precio_actual) FROM productos WHERE precio_actual IS NOT NULL
);
"""

Q7 = """
-- 7. Los 5 productos más económicos en cada categoría
SELECT categoria, nombre, precio_actual
FROM (
    SELECT
        categoria,
        nombre,
        precio_actual,
        ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY precio_actual ASC) AS rn
    FROM productos
    WHERE precio_actual IS NOT NULL
) ranked
WHERE rn <= 5
ORDER BY categoria, precio_actual;
"""

Q8 = """
-- 8. Ahorro promedio cuando existe precio anterior
SELECT
    categoria,
    ROUND(AVG(precio_anterior - precio_actual)::NUMERIC, 2) AS ahorro_promedio
FROM productos
WHERE precio_anterior IS NOT NULL
  AND precio_actual   IS NOT NULL
  AND precio_anterior > precio_actual
GROUP BY categoria
ORDER BY ahorro_promedio DESC;
"""

Q9 = """
-- 9. Distribución de productos por rango de precio
SELECT
    CASE
        WHEN precio_actual < 500000   THEN 'Bajo  (< 500k)'
        WHEN precio_actual < 1500000  THEN 'Medio (500k – 1.5M)'
        ELSE                               'Alto  (> 1.5M)'
    END AS rango,
    COUNT(*) AS cantidad
FROM productos
WHERE precio_actual IS NOT NULL
GROUP BY rango
ORDER BY MIN(precio_actual);
"""


QUERIES = [
    (Q1, "1. Precio promedio por categoría"),
    (Q2, "2. Producto más costoso por categoría"),
    (Q3, "3. Productos con / sin envío gratis"),
    (Q4, "4. Ubicaciones con más publicaciones (top 10)"),
    (Q5, "5. Descuento promedio por categoría"),
    (Q6, "6. Productos sobre el precio promedio general"),
    (Q7, "7. Los 5 más económicos por categoría"),
    (Q8, "8. Ahorro promedio (precio anterior vs actual)"),
    (Q9, "9. Distribución por rango de precio"),
]


def run_all():
    results = {}
    for sql, title in QUERIES:
        df = run_query(sql, title)
        results[title] = df
    print("\n[ANÁLISIS] Todas las consultas ejecutadas correctamente.\n")
    return results


if __name__ == "__main__":
    run_all()
