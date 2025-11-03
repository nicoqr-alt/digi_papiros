import os
BASE = os.path.dirname(os.path.dirname(__file__))
DOCS = os.path.join(BASE, "docs")
CSV_PATH = os.path.join(BASE, "data", "catalogo.csv")
from textwrap import dedent
def bloque_pdf(_id: str) -> str:
       url = pdf_en_ficha(_id)
       if not url: #Aunque no haya PDF aparece un placeholder
              return '[Ver PDF](#) { .md-button .require-auth .download-link data-book-id="{_id}" }<span class = "muted">(disponible próximamente)</span>'
       return dedent(f"""

<summary> Datos BibTEX</summary>
<object data = "{url}" type="application/pdf" width="100%" height="700" >
<p> Tu navegador no puede mostrar PDF incrustado <a href="{url}" target="_blank" rel ="noopener"> Abrir PDF </a> o usa el botón "Descargar".</p>
</object>
</details>""").strip()

def escribe_metadatos(autores, coleccion, serie, tomo, anio, editorial, edicion, isbn_col, isbn_libro):
    def opt(label, val):
    #Minifuncion para evitar que los datos fallen al escribirse
        return f"| **{label}** | {val} | \n" if val else ""
    return   (
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