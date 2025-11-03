#!/usr/bin/env
import csv, os, json
BASE = os.path.dirname(os.path.dirname(__file__))
DOCS = os.path.join(BASE, "docs")
CSV_PATH = os.path.join(BASE, "data", "catalogo.csv")

#Módulos propios
import escritor_catalogo #Escribe el texto que se agrega al catálogo
import crea_paginas #Crea las páginas completas de cada texto
import genera_json

#Corre el código al ejecutar el archivo
def main():
    
#-------------------------------------------------------- LECTURA DE BASE DE DATOS --------------------------------------------------------
    #Abre la base de datos CSV
    with open(CSV_PATH, newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f) #Reader de la base de datos
        filas = list(reader) #Convierte los datos a una lista
    print(f"Filas leídas: {len(filas)}") #Confirmación de lectura de fichas
    libros_dir = os.path.join(BASE,"docs","libros") #Dirección de guardado de los libros ---BASE/DOCS---- (Aquí se guardarán las páginas de MARKDOWN)
    os.makedirs(libros_dir,exist_ok=True) #Verifica la no sobrescritura del directorio
    orden_filas = sorted(filas,
           key = lambda r: ((r.get("autores") or ""), (r.get("titulo") or "").lower())
    ) #Ordena las filas de la lista; primero autores y después título. Regresa una lista ordenada.
#------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------- Escritura de catálogo  --------------------------------------------------------
    #Escribe el catálogo con titulo, identificador, coleccion, serie, estado y un separador; regresa una lista cuyas entradas son espacios y estos textos
    lineas = escritor_catalogo.lista_catalogo(orden_filas)
    catalogo_path = os.path.join(BASE, "docs", "catalogo.md") #Path para guardar el catálogo: BASE/docs
    with open(catalogo_path, "w", encoding = "utf-8") as fcat:
           fcat.write("\n".join(lineas))
    print("Catalogo actualizado")
#------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------- JSON, Buscador y páginas --------------------------------------------------------
    #Buscalibros
    DATA_DIR = os.path.join(DOCS, "data") #Establece dirección para el archivo JSON (DOCS/DATA)
    os.makedirs(DATA_DIR, exist_ok = True) #Verifica que exista para no sobrescribir
    data_json = []
    for fila in filas: #Genera catálogo JSON y escribe las páginas de las fichas
           data_json.append(genera_json.gjsn(fila))
           crea_paginas.fila_a_obj(fila)
    json_path = os.path.join(DATA_DIR, "catalogo.json") #Path del JSON
    with open(json_path, "w", encoding = "utf-8") as jf: #Abriendo el archivo JSON como JSNfile
           json.dump(data_json,jf,ensure_ascii = False, indent = 2)
    print("JSON exportado:", json_path)
#------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
            main()