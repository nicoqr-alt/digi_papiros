#tools/watermark_to_book_folders.py
#Usar: pip install reportlab pypdf

import io
import os
import csv
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from pypdf import PdfReader, PdfWriter

#Rutas de los PDF sin marcas de agua y del catálogo
DOCS = "docs"
SRC = os.path.join(DOCS, "assets", "pdfs_src") #Dirección de los PDFs de origen sin ninguna marca
CSV_PATH = os.path.join("data", "catalogo.csv") #Para enlazar con el catálogo

#Mensajes para agregar en los PDFs
MARCA = "Línea inferior de la marca\nLínea superior de la marca"
FOOTER = "Editorial de matemáticas - https://direccion/de/la/pagina"

def watermark_page(w: float, h:float):
    """
    Esta función crea una página PDF en memoria con:
     - Texto diagonal de marca (gris claro)
     - Pie de página con branding
     Devuelve un PageObject listo para fusionar con pypdf
    """
    buf = io.BytesIO()

    c = canvas.Canvas(buf, pagesize = (w,h))

    #-----Marca diagonal-----
    c.saveState()
    #Gris claro
    c.setFillColor(Color(0.2,0.2,0.2)) #Elige el color en formato RGB
    c.setFont ("Helvetica", 16) #Fuente y tamaño
    c.translate(w/2,h/2) #Toma el punto en la mitad de la página como (0,0)
    c.rotate(90) #Rotar 90 grados al sistema (e1,e2)
    lines = MARCA.split("\n") #Dividir en líneas el mensaje
    line_gap = 18 #Separación entre líneas
    altura_total = (len(lines)-1) * line_gap #Altura total del bloque de líneas
    y0= altura_total/2 #Posición Y de la primera línea
    for i, line in enumerate(lines):
        y = y0+ i * line_gap #Posición Y de la línea actual
        c.drawCentredString(0,y+w/3+20,line) #Considerando (1,1) como el (-1,1) original
    c.restoreState()

    #Pie de página
    c.setFont("Helvetica", 9) #Fuente y tamaño
    c.setFillColor(Color(0.2,0.2,0.2)) #Gris claro
    c.drawCentredString(w/2, 20, FOOTER) #Texto centrado en la parte inferior

    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]

#Esta función podría ser modificada para aceptar parámetros de texto que dependan del PDF a marcar
#Por ahora, es fija para todos los PDFs. 
def marcar_pdf(src_path: str, out_path: str, titulo: str = "Ed. Digitall"):
    """
    Esta función toma un PDF y lo regresa con la marca de agua fabricada con la función anterior
    """
    src = PdfReader(src_path) #Lectura del PDF de origen
    out = PdfWriter()   #PDF de salida

    w = float(src.pages[0].mediabox.width) #Ancho de la página
    h = float(src.pages[0].mediabox.height) #Alto de la página
    wm = watermark_page(w,h) #Genera la marca de agua. Aquí se podría modificar para aceptar parámetros
    for p in src.pages: #Merge de cada página con la marca
        p.merge_page(wm)
        out.add_page(p)
    out.add_metadata(
        {
            "/Title": titulo,
            "/Author": "Editorial de Matemáticas",
            "/Subject": "Distribución digital",
            "/Producer": "Pipeline Mkdocs",
            "/ModDate": datetime.utcnow().strftime("D:%Y%m%d%H%M%S+00'00")
        }
    )
    #Confirmación del marcado
    os.makedirs(os.path.dirname(out_path), exist_ok = True)
    with open(out_path, "wb") as f:
        out.write(f)
    print("Marcado hecho", out_path)
#Ejecución principal
def main():
    #Lee IDs y títulos desde el catálogo maestro
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            _id = (row.get("id") or "").strip()
            titulo = (row.get("titulo") or _id).strip()
            if not _id:
                continue
            src_pdf = os.path.join(SRC, f"{_id}.pdf")
            if not os.path.exists(src_pdf):
                print(f"- sin PDF de origen: {_id}")
                continue
            out_pdf = os.path.join(DOCS, "libros", _id, f"{_id}_mark.pdf")
            marcar_pdf(src_pdf, out_pdf, titulo)

if __name__ == "__main__":
    main()

