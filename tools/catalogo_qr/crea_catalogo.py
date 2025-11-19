import os
import pandas as pd
AUTORESCSV = os.path.join(BASE, "tools", "catalogo_qr", "autores.csv")
LIBROSAUTORESCSV = os.path.join(BASE, "tools", "catalogo_qr", "libros_autores.csv")
LIBROSCSV = os.path.join(BASE, "tools", "catalogo_qr", "libros.csv")
RESUMENESCSV = os.path.join(BASE, "tools", "catalogo_qr", "resumenes.csv")

libros = pd.read_csv(LIBROSCSV)
autores = pd.read_csv(AUTORESCSV)
libros_autores = pd.read_csv(LIBROSAUTORESCSV)
resumenes = pd.read_csv(RESUMENESCSV)

la = libros_autores.merge(autores, left_on="id_autor", right_on="id_ath", how = "left")
