#Con este código se redactan entradas para la base de datos
#id titulo autores coleccion numserie ibncol isbnlibro tomo anio editorial edicion resumen estado

def titulo():
    return input("Escribe el título: ")

def autores(n):
    if n==1:
        return [input("Escribe el nombre: ")]
    if n>1:
        noms = [input("Nombre "+str(i+1)+": ") for i in range(n)]
        print(noms)
        return noms
    
def coleccion():
    return input("Coleccion: ")

def serie():
    return input("Serie: ")

def numserie():
    return input("Número de serie: ")

def isbncol():
    return input("ISBN de la colección: ")

def isbnlibro():
    return input("ISBN del libro: ")

def tomo():
    return input("Tomo: ")

def anio():
    return input("Año: ")

def editorial():
    return input("Editorial: ")

def edicion():
    return input("Edición: ")

def resumen():
    return input("Resumen: ")

def estado():
    return input("Estado: ")

def id(coleccion, serie="x", numserie):
    if serie == "x":
        return coleccion[0:3].lower() + "-" + serie[0:3].lower() + "-" + str(numserie)
    else:
        return coleccion[0:3].lower() + "-x-" + str(numserie)

