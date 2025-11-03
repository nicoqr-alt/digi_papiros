import os
BASE = os.path.dirname(os.path.dirname(__file__))
DOCS = os.path.join(BASE, "docs")
CSV_PATH = os.path.join(BASE, "data", "catalogo.csv")
from textwrap import dedent
def pdf_en_ficha(_id: str) -> str:
       """
       Devuelve la ruta relativa al PDF marcado si existe, o un dirección dummy
       """
       rel = f"{_id}_mark.pdf"
       #./<id>_mark.pdf
       abs_path = os.path.join(DOCS, "libros", _id, rel)
       return rel if os.path.exists(abs_path) else ""

def bloque_pdf(_id: str) -> str:
       url = pdf_en_ficha(_id)
       if not url: #Aunque no haya PDF aparece un placeholder
              return '[Ver PDF](#) { .md-button .require-auth .download-link data-book-id="{_id}" }<span class = "muted">(disponible próximamente)</span>'
       return dedent(f"""
<p>Para poder descargar el archivo o mostrar en el explorador necesitas crear una cuenta e iniciar sesión.</p>
<a class="md-button require-auth data-book-id={_id} download-link" data-book-id="{_id}" href = "{url}" target = "_blank" rel ="noopener" > Abrir PDF </a>
<a class="md-button require-auth data-book-id={_id} download-link" data-book-id="{_id}" href ="{url}" download> Descargar</a>
<details>
<summary> Ver en línea (vista previa)</summary>
<object data = "{url}" type="application/pdf" width="100%" height="700" >
<p> Tu navegador no puede mostrar PDF incrustado <a href="{url}" target="_blank" rel ="noopener"> Abrir PDF </a> o usa el botón "Descargar".</p>
</object>
</details>""").strip()

