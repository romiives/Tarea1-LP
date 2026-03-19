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
nombre_valido = r"(" + snake_case + r"|" + camelCase + r"|" + PascalCase + r")"
#estructurasavanzadas
condicion = r"\(\s*" + nombre_valido + r"\s*" + operacion + r"\s*" + valor + r"\s*\)"
estructura_control = r"(if|while)\s*"+ condicion + r"\s*\{"
cierre_bloque = r"\}"
declaracion_funcion = r"(int|bool|char|string|void)\s+" + nombre_valido + r"\s*\(\s*\)\s*\{"
declaracion_variable = r"(int|bool|char|string)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*"
retorno = r"return\s+" + nombre_valido + r"\s*;" 
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
    match = re.search(r"[a-zA-Z_][a-zA-Z0-9_]*\(", primera_linea)
    if match:
        nombre = match.group(0).replace("(", "")
    else:
        return "desconocido"
    if re.fullmatch(snake_case, nombre):
        return "snake"
    elif re.fullmatch(camelCase, nombre):
        return "camel"
    elif re.fullmatch(PascalCase, nombre):
        return "pascal"
    else:
        return "desconocido"

def guardarFunciones(funciones):
    s = open("snake.txt", "w")
    c = open("camel.txt", "w")
    p = open("pascal.txt", "w")
    d = open("desconocido.txt", "w")
    for funcion in funciones:
        autor = clasificarAutor(funcion)
        if autor == "snake":
            s.write(funcion + "\n")
        elif autor == "camel":
            c.write(funcion + "\n")
        elif autor == "pascal":
            p.write(funcion + "\n")
        else: 
            d.write(funcion + "\n")
    s.close()
    c.close()
    p.close()
    d.close()

def contarVariables(bloque):
    lineas = bloque.split("\n")
    cont = 0
    for linea in lineas:
        linea_limpia = linea.strip()
        if re.match(declaracion_variable, linea_limpia):
            cont += 1
    return cont 

def detectarDiferenciasEstilo(bloque, autor):
    lineas = bloque.split("\n")
    diferencias = 0
    for linea in lineas:
        linea_limpia = linea.strip()
        if re.match(declaracion_variable, linea_limpia):
            match = re.search(r"(int|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)", linea_limpia)
            if match:
                nombre = match.group(2)
                if autor == "snake":
                    if not re.match(snake_case, nombre):
                        diferencias = diferencias + 1
                elif autor == "camel":
                    if not re.match(camelCase, nombre):
                        diferencias = diferencias +1
                elif autor == "pascal":
                    if not re.match(PascalCase, nombre):
                        diferencias = diferencias + 1
    return diferencias 

def detectarErroresSintaxis(bloque):
    lineas = bloque.split("\n")
    errores = []
    llaves = 0
    for linea in lineas:
        linea_limpia = linea.strip()
        llaves += linea.count("{")
        llaves -= linea.count("}")
        if re.match(declaracion_variable, linea_limpia):
            if not linea_limpia.endswith(";"):
                errores.append("Falta ; en: " + linea_limpia)
        if linea_limpia.startswith("return"):
            if not linea_limpia.endswith(";"):
                errores.append("Falta ; en return: " + linea_limpia)
    if llaves > 0:
        errores.append("Faltan llaves de cierre")
    return errores

#funcion necesaria para reporte final
def obtenerFuncion(bloque):
    lineas = bloque.split("\n")
    primera_linea = lineas[0]
    match = re.search(r"[a-zA-Z_][a-zA-Z0-9_]*\s*\(", primera_linea)
    if match:
        nombre = match.group(0)
        nombre = nombre.replace("(", "")
        return nombre
    return "desconocido"

#reportefinal
def generarReporte(funciones):
    reporte = {
        "snake": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []},
        "camel": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []},
        "pascal": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []},
        "desconocido": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []}
    }
    for funcion in funciones:
        autor = clasificarAutor(funcion)
        nombre = obtenerFuncion(funcion)
        variables = contarVariables(funcion)
        diferencias = detectarDiferenciasEstilo(funcion, autor)
        errores = detectarErroresSintaxis(funcion)
        reporte[autor]["funciones"] += 1
        reporte[autor]["nombres"].append(nombre)
        reporte[autor]["variables"] += variables
        reporte[autor]["diferencias"] += diferencias
        reporte[autor]["errores"] += len(errores)
        for error in errores:
            reporte[autor]["detalle"].append(error)
    print("REPORTE DE EVALUACIÓN DE PRACTICANTES")
    for autor in reporte:
        print("PRACTICANTE:", autor)
        print("- Funciones creadas:", reporte[autor]["funciones"])
        print("- Variables declaradas:", reporte[autor]["variables"])
        print("- Diferencias de estilo:", reporte[autor]["diferencias"])
        print("- Errores de sintaxis:", reporte[autor]["errores"])
        print("- Error en:")
        for error in reporte[autor]["detalle"]:
            print("  *", error)
        print("")
   
#intmain
funciones = detectarFunciones()
guardarFunciones(funciones)
generarReporte(funciones)
    
    
    

        

