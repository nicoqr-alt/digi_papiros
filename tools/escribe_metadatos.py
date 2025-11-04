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

