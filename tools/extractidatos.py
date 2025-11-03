#Este código extrae los datos de una entrada de la base de datos
from mostrador_PDF import pdf_en_ficha, bloque_pdf
def extractidatos(r):
    '''Esta función toma una entrada de documento y regresa, en este orden, la siguiente info: autores, anio, id, titulo, coleccion, serie, tomo, editorial, edicion, isbn de la coleccion, isbn del libro, estado, resumen y descargas'''
        #Recibe una fila (entrada) y la convierte en un objeto para crear la página
        #Limpiador
        #cada fila (del diccionario) es re-hecha para que los campos con entradas múltiples (e.g., múltiples autores) se vuelvan una lista
    def g(name, alt = None, default = ""):
        return (r.get(name) or (r.get(alt) if alt else "") or default).strip()
    return [a.strip() for a in g("autores").split(";") if a.strip()], g("anio"), g("id"), g("titulo"), g("coleccion"), g("serie"), g("tomo"), g("editorial"), g("edicion"), g("isbn_col", "isbn_coleccion"), g("isbn:libro"), g("estado", default = "por_recibir"), g("resumen", default = "proximamente"), bloque_pdf(g("id"))
      
