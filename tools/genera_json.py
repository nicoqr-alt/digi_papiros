from mostrador_PDF import pdf_en_ficha, bloque_pdf
import os
BASE = os.path.dirname(os.path.dirname(__file__))
DOCS = os.path.join(BASE, "docs")
CSV_PATH = os.path.join(BASE, "data", "catalogo.csv")
import extractidatos
def gjsn(r):
       #Recibe una fila (entrada) y la convierte en un objeto para crear la página
       #Limpiador
       #cada fila (del diccionario) es re-hecha para que los campos con entradas múltiples (e.g., múltiples autores) se vuelvan una lista
       autores, anio, _id, titulo, coleccion, serie, tomo, editorial, edicion, isbn_col, isbn_libro, estado, extra1, extra2 = extractidatos.extractidatos(r)
       autores = [" ".join(autor[0]) + " " + " ".join(autor[1]) for autor in autores]
       #print(autores)
       return{
              "id": _id,
              "titulo": titulo,
              "autores": autores,
              "coleccion": coleccion,
              "serie": serie,
              "tomo": tomo,
              "anio": anio,
              "editorial": editorial,
              "edicion": edicion,
              "isbn_col": isbn_col,
              "isbn_libro": isbn_libro,
              "estado": estado,
       }

