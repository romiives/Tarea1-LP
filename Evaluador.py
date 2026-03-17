import re
#funcion para leer archivo
def leerArchivo():
    f = open("programa.txt")
    archivo = f.read()
    f.close()
    return archivo

#regrex 
#basicas
digito = r"[0-9]"
letra_min = r"[a-z]"
letra_may = r"[A-Z]"
letra = r"[a-zA-Z]"
palabra = r"[a-zA-Z][a-zA-Z0-9]*"
#tiposdedatosyoperaciones
operacion = r"(\+|-|/|\*|=|==|<|>)"
booleano = r"(true|false)"
cadena_texto = r"\"[a-zA-Z][a-zA-Z][0-9]*\""
caracter = r"\'[a-zA-Z]\'"
valor = r"([0-9]|true|false|\"[a-zA-Z][a-zA-Z0-9]*\"|'[a-zA-Z]\')"
tipo_dato = r"(int|bool|char|string|void)"
#estilos
snake_case = r"[a-z]+(_[a-z]+)*"
camelCase = r"[a-z]+([A-Z][a-z]+)*"
PascalCase = r"[A-Z][a-z]+([A-Z][a-z]+)*"
nombre_valido = r"([a-z]+(_[a-z]+)*|[a-z]+([A-Z][a-z]+)*|[A-Z][a-z]+([A-Z][a-z]+)*)"
#estructurasavanzadas
condicion = r"\([a-zA-Z][a-zA-Z0-9]* (\+|-|/|\*|=|==|<|>) ([0-9]|true|false|\"[a-zA-Z][a-zA-Z0-9]*\"|'[a-zA-Z]')\)"
estructura_control = r"(if|while) \([a-zA-Z][a-zA-Z0-9]* (\+|-|/|\*|=|==|<|>) ([0-9]|true|false|\"[a-zA-Z][a-zA-Z0-9]*\"|'[a-zA-Z]')\{"
cierre_bloque = r"\}"
declaracion_funcion = r"(int|bool|char|string|void)\s+[a-zA-Z_][A-Za-z0-9_]*\s*\(\)\s*\{"
declaracion_variable = r"(int|bool|char|string|void) ([a-z]+(_[a-z]+)*|[a-z]+([A-Z][a-z]+)*|[A-Z][a-z]+([A-Z][a-z]+)*) (\+|-|/|\*|=|==|<|>) ([0-9]|true|false|\"[a-zA-Z][a-zA-Z0-9]*\"|'[a-zA-Z]\');"
retorno = r"return ([a-z]+(_[a-z]+)*|[a-z]+([A-Z][a-z]+)*|[A-Z][a-z]+([A-Z][a-z]+)*)"
comentario_one_line = r"//[a-zA-Z][a-zA-Z0-9]*"
comentario_multi_line = r"/\*[a-zA-Z][a-zA-Z0-9]*\*/"

def detectarFunciones():
    archivo = leerArchivo()
    lineas = archivo.split("\n")
    lista_bloques = []
    bloque_actual = ""
    dentro_funcion = False
    llaves = 0
    nombre_funcion_actual = ""
    for linea in lineas:
        linea_limpia = linea.strip()
        if not dentro_funcion and re.match(declaracion_funcion, linea_limpia):
            dentro_funcion = True
            bloque_actual = linea + "\n"
            llaves = linea.count("{") - linea.count("}")
            match = re.search("[a-zA-Z_][a-zA-Z0-9_]*\(", linea_limpia)
            if match:
                nombre_funcion_actual = match.group(0).replace("(", "")
        elif dentro_funcion:
            bloque_actual += linea + "\n"
            llaves += linea.count("{") 
            llaves -= linea.count("}")
            if llaves == 0:
                lista_bloques.append(bloque_actual)
                bloque_actual = ""
                dentro_funcion = False 
                llaves = 0
                nombre_funcion_actual = ""
    if dentro_funcion:
        lista_bloques.append(bloque_actual)
        return lista_bloques


def clasificarAutor(bloque):
    lineas = bloque.split("\n")
    primera_linea = lineas[0].strip()
    match = re.search("[a-zA-Z_][a-zA-Z0-9_]*\(", primera_linea)
    if match:
        nombre = match.group(0).replace("(", "")
    else:
        return "Desconocido"
    if re.match(snake_case, nombre):
        return "snake"
    elif re.match(camelCase, nombre):
        return "camel"
    elif re.match(PascalCase, nombre):
        return "pascal"
    else:
        return "Desconocido"


funciones = detectarFunciones()
print("Cantidad de funciones:", len(funciones))
for f in funciones:
    autor = clasificarAutor(f)
    print("AUTOR:", autor)
    print("FUNCION DETECTADA:")
    print (f)

        

