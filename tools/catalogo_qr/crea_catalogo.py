import os
import pandas as pd
# ==========================
# RUTAS DE ENTRADA / SALIDA
# ==========================
BASE = os.path.dirname(os.path.dirname(__file__))


AUTORES_CSV        = os.path.join(BASE, "catalogo_qr", "autores.csv")
AUTORES_LIBROS_CSV = os.path.join(BASE, "catalogo_qr", "libros_autores.csv")
RESUMENES_CSV      = os.path.join(BASE, "catalogo_qr", "resumenes.csv")
LIBROS_CSV         = os.path.join(BASE, "catalogo_qr", "libros.csv")

SALIDA_CSV         = "data/catalogo.csv"
print(BASE)

# Separador entre autores en la celda final (puedes cambiarlo si tu script espera otro)
SEPARADOR_ENTRE_AUTORES = "; "


# ==========================
# 1. LEER ARCHIVOS
# ==========================

autores        = pd.read_csv(AUTORES_CSV)        # columnas: id_autor, nombres, apellidos
autores_libros = pd.read_csv(AUTORES_LIBROS_CSV) # columnas: id_libro, id_autor
resumenes      = pd.read_csv(RESUMENES_CSV)      # columnas: id_libro, resumen
libros         = pd.read_csv(LIBROS_CSV)         # columnas: id, titulo, coleccion, ...

# Asegurarnos de tener nombres de columnas coherentes
# (renombramos id de libros a id_libro para los joins)
# Libros: renombrar id → id_libro
libros = libros.rename(columns={"id": "id_libro"})

# ==========
# AUTORES
# ==========

autores["id_autor"]  = autores["id_autor"].astype(str).str.strip()
autores["nombres"]   = autores["nombres"].fillna("").astype(str)
autores["apellidos"] = autores["apellidos"].fillna("").astype(str)
autores["autor_fmt"] = autores["nombres"] + ">" + autores["apellidos"]

# ==========
# AUTORES_LIBROS: reventar listas de ids
# ==========

# ==========
# 3. PROCESAR AUTORES_LIBROS
# ==========

autores_libros["id_libro"] = autores_libros["id_libro"].astype(str).str.strip()
autores_libros["id_autor"] = autores_libros["id_autor"].astype(str).str.strip()

# Si hay múltiples autores en una celda, dividirlos
# Ejemplo de celda: "mlhz;jprz;abcd"
autores_libros["id_autor_list"] = autores_libros["id_autor"].str.split(";")

# EXPLODE: una fila por cada autor
al = autores_libros.explode("id_autor_list").copy()

# Construir AHORA la columna id_autor a partir de la lista
al["id_autor"] = al["id_autor_list"].astype(str).str.strip()

# Ya no necesitamos la columna auxiliar
al = al.drop(columns=["id_autor_list"])
# ==========
# MERGE PARA OBTENER EL TEXTO DE CADA AUTOR
# ==========

al = al.merge(
    autores[["id_autor", "autor_fmt"]],
    on="id_autor",
    how="left"
)

# Evitar NaN y asegurarnos de que todo sea str
al["autor_fmt"] = al["autor_fmt"].fillna("").astype(str)

# ==========
# AGRUPAR POR LIBRO → CADENA CON TODOS LOS AUTORES
# ==========

autores_por_libro = (
    al.groupby("id_libro")["autor_fmt"]
      .apply(lambda s: ", ".join([x for x in s if x != ""]))
      .reset_index(name="autores")
)

# ==========================
# 4. UNIR LIBROS + AUTORES + RESÚMENES
# ==========================

# 4.1 Libros + autores
catalogo = libros.merge(
    autores_por_libro,
    on="id_libro",
    how="left"
)

# 4.2 Libros + resúmenes
catalogo = catalogo.merge(
    resumenes,
    on="id_libro",
    how="left"
)

# Volver a llamar 'id_libro' simplemente 'id' para el CSV final
catalogo = catalogo.rename(columns={"id_libro": "id"})
catalogo["anio"] = catalogo["anio"].astype(str).str.replace(".0", "", regex=False)
catalogo["edicion"] = catalogo["edicion"].astype(str).str.replace(".0", "", regex=False)
catalogo["tomo"] = catalogo["tomo"].astype(str).str.replace(".0", "", regex=False)
# ==========================
# 5. ORDENAR COLUMNAS COMO QUIERES
# ==========================

columnas_finales = [
    "id",
    "titulo",
    "autores",
    "coleccion",
    "serie",
    "num_serie",
    "isbn_col",
    "isbn_libro",
    "tomo",
    "anio",
    "editorial",
    "edicion",
    "resumen",
    "estado",
]

# Por si acaso alguna columna faltara, filtramos a las que existan
columnas_existentes = [c for c in columnas_finales if c in catalogo.columns]
catalogo = catalogo[columnas_existentes]

# ==========================
# 6. GUARDAR CSV FINAL
# ==========================

catalogo.to_csv(SALIDA_CSV, index=False)
print(f"Catálogo generado en: {SALIDA_CSV}")