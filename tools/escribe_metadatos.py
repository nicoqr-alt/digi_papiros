def escribe_metadatos(autores, coleccion, serie, tomo, anio, editorial, edicion, isbn_col, isbn_libro):
    #Lista con autores de nombre y apellio completo en una sola string
    auts = [", ".join(autor[0]) + " " + ", ".join(autor[1]) for autor in autores]


    def opt(label, val):
    #Minifuncion para evitar que los datos fallen al escribirse
        return f"| **{label}** | {val} | \n" if val else ""
    return   (
                "|  |  |\n"
                "|---|---|\n"
                + opt("Autores", ", ".join(auts) if auts else "")
                + opt("Colección", coleccion)
                + opt("Serie", serie)
                + opt("Tomo", tomo)
                + opt("Año", anio)
                + opt("Editorial", editorial)
                + opt("Edición", edicion)
                + opt("ISBN (Colección)", isbn_col)
                + opt("ISBN (Texto)", isbn_libro)
                ).rstrip()

