#!/usr/bin/env
import csv, os, json
BASE = os.path.dirname(os.path.dirname(__file__))
DOCS = os.path.join(BASE, "docs")
CSV_PATH = os.path.join(BASE, "data", "catalogo.csv")

def main():
    #Leer el CSV y listar lo que tiene
    with open(CSV_PATH, newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = list(reader)
    #Mostrar las filas leídas
    print(f"Filas leídas: {len(filas)}")
    #Para crear el directorio
    libros_dir = os.path.join(BASE,"docs","libros")
    os.makedirs(libros_dir,exist_ok=True)

    for row in filas:
           #Obtener los datos de cada elemento
           _id = row["id"].strip()
           tomo = row.get("tomo","no aplica")
           resumen = row["resumen"].strip()

           #En caso de que haya un error en la correspondencia de la información, agregar un str(row) para ver el diccionario asociado, imprimirlo y verificar los datos. Agregar {diccionario} al contenido para verlo.
           contenido = f"""# {row["titulo"].strip()}
           **Autores:** {row["autores"].strip()}
           **Colección:** {row["coleccion"].strip()}
           **Serie:** {row["serie"].strip()}
           **Tomo:** {tomo if tomo else "No aplica"}
           **Año:** {row["anio"].strip()}
           **Editorial:** {row["editorial"].strip()}
           **Edición:**{row["edicion"].strip()}
           **ISBN (Colección):** {row["isbn_col"].strip()}
           **ISBN (Libro):** {row["isbn_libro"].strip()}
           !!! info "Estado"
                {row.get("estado", "por determinar")}

            ### Resumen
            {resumen if resumen else "Próximamente"}
            """


           #Crear el archivo con los datos
           out_path = os.path.join(libros_dir, f"{_id}.md")
           with open(out_path, "w", encoding="utf-8") as fh:
                  fh.write(contenido)

           print("Ficha cread(fa:, ", out_path)
    
    orden_filas = sorted(
           filas,
           key = lambda r: ((r.get("autores") or ""), (r.get("titulo") or "").lower())
    )

    lineas =["#Catálogo", ""]
    for r in orden_filas:
           ident = r["id"].strip()
           titulo = r["titulo"].strip()
           coleccion = r["coleccion"].strip()
           estado = (r.get("estado") or "Por recibir")
           serie = (r.get("serie") or "")
           lineas.append(f"- **[{titulo}](libros/{ident}.md)** {coleccion} {serie} - {estado}")
    lineas.append("")

    catalogo_path = os.path.join(BASE, "docs", "catalogo.md")
    with open(catalogo_path, "w", encoding = "utf-8") as fcat:
           fcat.write("\n".join(lineas))
    print("Catalogo actualizado")
    
    #Crear los archivos para hacer el buscalibros
    DATA_DIR = os.path.join(DOCS, "data")
    os.makedirs(DATA_DIR, exist_ok = True)
    #Pasar las cosas al formato JSON
    def fila_a_obj(r):
       #limpiador
       #cada fila(diccionario) es re-hecho para que los campos con entradas múltiples se vuelvan una lista
       def g(name, alt = None):
                  return (r.get(name) or (r.get(alt) if alt else "") or "").strip()
       #Obtenemos los autores
       autores = [a.strip() for a in g("autores").split(";") if a.strip()]
       anio = g("anio") #Aquí podría haber un error
       return{
       "id": g("id"),
       "titulo": g("titulo"),
       "autores": autores,
       "coleccion": g("coleccion"),
       "serie":g("serie"),
       "tomo":g("tomo"),
       "anio": anio,
       "editorial": g("editorial"),
       "edicion": g("edicion"),
       "isbn_col": g("isbn_col", "isbn_coleccion"),
       "isbn_libro": g("isbn:libro"),
       "estado": g("estado") or "por_recibir"
       }
    
    #Creamos el catálogo JSON
    data_json = [fila_a_obj(fila) for fila in filas]

    json_path = os.path.join(DATA_DIR, "catalogo.json")
    with open(json_path, "w", encoding = "utf-8") as jf: #Abriendo el archivo JSON como jASONfILE
           json.dump(data_json,jf,ensure_ascii = False, indent = 2)
    print("JSON exportado:", json_path)
     


if __name__ == "__main__":
            main()