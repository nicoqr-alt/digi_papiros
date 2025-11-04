En esta carpeta se encuentran los scripts de python usados para generar los archivos de la página. El script central es *pipeline_archivos.py*. 

pipeline_archivos: 
    Accede a data/catalogo.csv y lee cada una de las entradas.  
    Escribe el catálogo y lo guarda en docs/catalogo.md 
    Genera un json en docs/data/catalogo.json este se usa para generar el buscador. 
    Crea las páginas de cada libro en docs/libros/id.md (por cada id de cada libro)

crea_paginas.py:
    Dada una entrada de libro, escribe su página y la guarda en docs/libros/id.md con id el identificador único para cada libro

escribe_metadatos.py:
    Recibe informacion de una entrada y escribe una tabla de metadatos

escritor_bibtex.py:
    Dados los datos de una entrada regresa un texto para crear la tabla de bibtex

escritor_catalogo.py:
    Dada una lista de datos, crea una lista donde cada entrada es una línea del catálogo de libros

extractidatos.py:
    Dada una entrada de la base de datos ya procesada, extrae todos los datos de la misma y los almacena en variables locales (autores, anio, etc...)

genera_json.py:
    Dada una fila de datos, los extrae y genera un diccionario para generar un archivo JSON.

mostrador_pdf.py:
    Escribe los bloques de texto necesarios para mostrar los PDFs de los libros

watermark_to_book_folders.py:
    Dado un archivo PDF, regresa un PDF con una marca de agua (es ajustable). Lo guarda en docs/libros/id/id_mark.pdf