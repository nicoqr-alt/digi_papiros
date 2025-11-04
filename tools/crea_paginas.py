from mostrador_PDF import bloque_pdf
import os
BASE = os.path.dirname(os.path.dirname(__file__))
DOCS = os.path.join(BASE, "docs")
CSV_PATH = os.path.join(BASE, "data", "catalogo.csv")
from textwrap import dedent
import extractidatos
import escribe_metadatos
def fila_a_obj(r):
       #Recibe una fila (entrada) y la convierte en un objeto para crear la página
       #Limpiador
       #cada fila (del diccionario) es re-hecha para que los campos con entradas múltiples (e.g., múltiples autores) se vuelvan una lista
       autores, anio, _id, titulo, coleccion, serie, tomo, editorial, edicion, isbn_col, isbn_libro, estado, resumen, downs = extractidatos.extractidatos(r)

       #Obtención de gráficos
       cover_rel = f"assets/covers/{_id}.jpeg"
       cover_abs = os.path.join(DOCS, cover_rel)
       cover_md = f'![Portada de "{titulo}"](../{cover_rel})\n' if os.path.exists(cover_abs) else ""

       #Escritor de chip para la página de ficha
       def chip(label, val, emoji):
              return f'<span class ="chip"></span class ="icon">{emoji}</span>{val}</span>' if val else ""
       chips = " ".join(x for x in [chip("Serie", serie, "🏷"), chip("Colección", coleccion, "📚"), chip("Año", anio, "🗓"), chip("Estado", estado.replace("_", " "), "ℹ️") ] if x
                        )
       #Tabla de metadatos
       metadatos = escribe_metadatos.escribe_metadatos(autores, coleccion, serie, tomo, anio, editorial, edicion, isbn_col, isbn_libro)

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
{downs}

!!! info "Aviso"
    Documento con marca de agua para distribución **digital**.

## Cómo citar
> {(", ".join(autores) +". ") if autores else ""}{f"({anio}). " if anio else ""}*{titulo}*. {editorial}{(", " + str(edicion)) if edicion else ""}

<details>
  <summary>BibTeX</summary>
  <p style="font-family:'Courier New'">@book _id, <br>title = {titulo}, <br>author = {", ".join(autores) if autores else ""}, <br>year = {anio}, <br>publisher = editorial, <br>address = México </p>
</details>


[Volver al catálogo](../catalogo.md)

[Explorar](../explorar.md)
""")
       #Crear el archivo con los datos
       out_path = os.path.join(os.path.join(BASE,"docs","libros"), f"{_id}.md")
       with open(out_path, "w", encoding="utf-8") as fh:
              fh.write(contenido)

