#!/usr/bin/env
import csv, os, json
from textwrap import dedent
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
       def g(name, alt = None, default = ""):
                  return (r.get(name) or (r.get(alt) if alt else "") or default).strip()
       #Obtenemos los autores
       autores = [a.strip() for a in g("autores").split(";") if a.strip()]
       anio = g("anio") #Aquí podría haber un error
       _id = g("id")
       titulo = g("titulo")
       coleccion = g("coleccion")
       serie = g("serie")
       tomo = g("tomo")
       editorial =g("editorial")
       edicion = g("edicion")
       isbn_col = g("isbn_col", "isbn_coleccion")
       isbn_libro = g("isbn:libro")
       estado = g("estado", default = "por_recibir")

       cover_rel = f"assets/covers/{_id}.jpeg"
       cover_abs = os.path.join(DOCS, cover_rel)
       cover_md = f'![Portada de "{titulo}"](../{cover_rel})\n' if os.path.exists(cover_abs) else ""

       def chip(label, val, emoji):
              return f'<span class ="chip"></span class ="icon">{emoji}</span>{val}</span>' if val else ""
       
       chips = " ".join(x for x in [chip("Serie", serie, "🏷"), chip("Colección", coleccion, "📚"), chip("Año", anio, "🗓"), chip("Estado", estado.replace("_", " "), "ℹ️") ] if x
                        )
       #Tabla de metadatos

       def opt(label, val):
              return f"| **{label}** | {val} | \n" if val else ""
       metadatos = (
              "|  |  |\n"
              "|---|---|\n"
              + opt("Autores", ", ".join(autores) if autores else "")
              + opt("Colección", coleccion)
              + opt("Serie", serie)
              + opt("Tomo", tomo)
              + opt("Año", anio)
              + opt("Editorial", editorial)
              + opt("Edición", edicion)
              + opt("ISBN (Colección)", isbn_col)
              + opt("ISBN (Libro)", isbn_libro)
              ).rstrip()

       #YAML front matter para SEO Bùsqueda (qué es esto????)
       front_matter = dedent(f"""\
       ---
       title: "{titulo}"
       authors: {autores if autores else []}
       tags: [{", ".join(t for t in [coleccion, serie, anio] if t)}]
       ---
       """)
       #Contenido de la ficha en MARKDOWN. Nota que quité la sangría porque estoy dentro del entorno con tres comillas, entonces no importa la indentación. Si esto no se hace así, la ficha no se genera correctamente.
       contenido = front_matter + dedent(f"""# {titulo}
<div class = "chips">{chips}</div>

{cover_md}

## Resumen
{(resumen if resumen else "_Resumen próximamente._")}

## Metadatos
{metadatos}

## Descargas
[Ver PDF]{{{{ .md-button }}}} [EPUB](#)
{{{{ .md-button }}}} [HTML](#)
{{{{ .md-button }}}}

!!!info "Estado de la publicación":
{estado.replace("_", " ")}

## Cómo citar
> {(", ".join(autores) +". ") if autores else ""}{f"({anio}). " if anio else ""}*{titulo}*. {editorial}{(", " + str(edicion)) if edicion else ""}

[Volver al catálogo](../catalogo.md)

[Explorar](../explorar.md)
""")
       #Crear el archivo con los datos
       out_path = os.path.join(libros_dir, f"{_id}.md")
       with open(out_path, "w", encoding="utf-8") as fh:
              fh.write(contenido)

       print("Ficha creada:, ", out_path)
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
       
    #Creamos el catálogo JSON
    data_json = [fila_a_obj(fila) for fila in filas]

    json_path = os.path.join(DATA_DIR, "catalogo.json")
    with open(json_path, "w", encoding = "utf-8") as jf: #Abriendo el archivo JSON como jASONfILE
           json.dump(data_json,jf,ensure_ascii = False, indent = 2)
    print("JSON exportado:", json_path)
     


if __name__ == "__main__":
            main()