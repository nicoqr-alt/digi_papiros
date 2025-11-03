def lista_catalogo(lista_datos):
    lineas =["#Catálogo", ""]
    for r in lista_datos:
        ident = r["id"].strip()
        titulo = r["titulo"].strip()
        coleccion = r["coleccion"].strip()
        estado = (r.get("estado") or "Por recibir")
        serie = (r.get("serie") or "")
        lineas.append(f"- **[{titulo}](libros/{ident}.md)** {coleccion} {serie} - {estado}")
        lineas.append("")
    return lineas