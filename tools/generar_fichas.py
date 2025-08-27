#!/usr/bin/env
import csv, os
BASE = os.path.dirname(os.path.dirname(__file__))
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


if __name__ == "__main__":
            main()