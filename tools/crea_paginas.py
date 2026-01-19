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

       #Autores normal:
       autsnor = [", ".join(autor[0]) + " " + ", ".join(autor[1]) for autor in autores]

       #Autores bibtex:
       
       autbib =  [autor[1][0] +", "+ autor[0][0] for autor in autores]


       #Obtención de gráficos
       covername = f"assets/covers/{_id}"
       cover_rel = covername+".png" 
       cover_abs = os.path.join(DOCS, cover_rel)
       cover_md = f'![Portada de "{titulo}"](../{cover_rel})\n' if os.path.exists(cover_abs) else ""
       cover_file = f'\"../../{cover_rel}\"' if os.path.exists(cover_abs) else '\"../../'+covername+'.jpg\"'

       #Escritor de chip para la página de ficha
       def chip(label, val, emoji):
              return f'<span class ="chip"></span class ="icon">{emoji}</span> {val}</span>' if val else ""
       chips = " ".join(x for x in [chip("Serie", serie, "🏷"), chip("Colección", coleccion, "📚"), chip("Año", anio, "🗓"), chip("Estado", estado.replace("_", " "), "ℹ️") ] if x
                        )
       #Tabla de metadatos
       metadatos = escribe_metadatos.escribe_metadatos(autores, coleccion, serie, tomo, anio, editorial, edicion, isbn_col, isbn_libro)

       #YAML front matter para búsqueda SEO
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

<p align = "left"> <img src = {cover_file} width="500" height="600"></p>



## Resumen
{(resumen if resumen else "_Resumen próximamente._")}

## Metadatos
{metadatos}

## Descargas
{downs}

!!! info "Aviso"
    Documento con marca de agua para distribución **digital**.

## Cómo citar
> {(", ".join(autsnor) +". ") if autores else ""}{f"({anio}). " if anio else ""}*{titulo}*. {editorial}{(", " + str(edicion)) if edicion else ""}

<details>
<summary>BibTeX</summary>
<textarea id="myInput" rows="6" cols="80" class="verbatim">
@BOOK{{{_id}, 
title = {{{titulo}}}, 
author = {{{" and ".join(autbib) if autores else ""}}}, 
year = {{{anio}}}, 
publisher = {{{editorial}}}, 
address = {{México}}}}
</textarea>
<br>
<button style ="cursor:pointer; background-color: #ecf3ff; color: #448aff; padding: 3px 6px; border-radius: 6px; text-align: center" onclick="myFunction()">Copiar BibTeX</button>

<style>
  .verbatim {{
    font-family: monospace;
    white-space: pre;
  }}
</style>

<script>
function myFunction() {{
  const copyText = document.getElementById("myInput");
  copyText.select();
  navigator.clipboard.writeText(copyText.value);
  alert("¡Copiado!");
}}
</script>
</details>


[Volver al catálogo](../catalogo.md)

[Explorar](../explorar.md)
""")
       #Crear el archivo con los datos
       out_path = os.path.join(os.path.join(BASE,"docs","libros"), f"{_id}.md")
       with open(out_path, "w", encoding="utf-8") as fh:
              fh.write(contenido)

