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
#tipos de datos y operaciones
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
#estructuras avanzadas
condicion = r"\(\s*" + nombre_valido + r"\s*" + operacion + r"\s*" + valor + r"\s*\)"
estructura_control = r"(if|while)\s*"+ condicion + r"\s*\{"
cierre_bloque = r"\}"
declaracion_funcion = r"(int|bool|char|string|void)\s+" + nombre_valido + r"\s*\(\s*\)\s*\{"
declaracion_variable = r"(int|bool|char|string)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*"
retorno = r"return\s+" + nombre_valido + r"\s*;" 
comentario_one_line = r"//[a-zA-Z][a-zA-Z0-9]*"
comentario_multi_line = r"/\*[a-zA-Z][a-zA-Z0-9]*\*/"

#esta funcion busca las funciones (su estructura (bloques)) dentro del archivo y las guarda en una lista 
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
            match = re.search(r"[a-zA-Z_][a-zA-Z0-9_]*\(", linea_limpia)
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

#esta funcion revisa el nombre de la funcion y la clasifica en snake, camel o pascal
def clasificarAutor(bloque):
    lineas = bloque.split("\n")
    primera_linea = lineas[0].strip()
    match = re.search(r"[a-zA-Z_][a-zA-Z0-9_]*\(", primera_linea)
    if match:
        nombre = match.group(0).replace("(", "")
    else:
        return "Desconocido"
    if re.fullmatch(snake_case, nombre):
        return "Snake"
    elif re.fullmatch(camelCase, nombre):
        return "Camel"
    elif re.fullmatch(PascalCase, nombre):
        return "Pascal"
    else:
        return "Desconocido"

#esta funcion guarda las funciones en archivos (y a su vez crea los archivos) separados segun autor
def guardarFunciones(funciones):
    s = open("snake.txt", "w")
    c = open("camel.txt", "w")
    p = open("pascal.txt", "w")
    d = open("desconocido.txt", "w")
    for funcion in funciones:
        autor = clasificarAutor(funcion)
        if autor == "Snake":
            s.write(funcion + "\n")
        elif autor == "Camel":
            c.write(funcion + "\n")
        elif autor == "Pascal":
            p.write(funcion + "\n")
        else: 
            d.write(funcion + "\n")
    s.close()
    c.close()
    p.close()
    d.close()

#esta funcion cuenta las variables declaradas que hay dentro de una funcion 
def contarVariables(bloque):
    lineas = bloque.split("\n")
    cont = 0
    for linea in lineas:
        linea_limpia = linea.strip()
        if re.match(declaracion_variable, linea_limpia):
            cont += 1
    return cont 

#esta funcion revisa si el estilo del nombre de la variable no coincide con el estilo del autor y asi detecta diferencias 
def detectarDiferenciasEstilo(bloque, autor):
    lineas = bloque.split("\n")
    diferencias = 0
    for linea in lineas:
        linea_limpia = linea.strip()
        if re.match(declaracion_variable, linea_limpia):
            match = re.search(r"(int|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)", linea_limpia)
            if match:
                nombre = match.group(2)
                if autor == "Snake":
                    if not re.match(snake_case, nombre):
                        diferencias = diferencias + 1
                elif autor == "Camel":
                    if not re.match(camelCase, nombre):
                        diferencias = diferencias +1
                elif autor == "Pascal":
                    if not re.match(PascalCase, nombre):
                        diferencias = diferencias + 1
    return diferencias 

#esta funcion revisa los errores en la sintaxis al escribir una funcion, como un ; o llaves 
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

#esta funcion es necesaria para el reporte final, ya que sirve para identificar donde ocurre el error en "detalles"
def obtenerFuncion(bloque):
    lineas = bloque.split("\n")
    primera_linea = lineas[0]
    match = re.search(r"[a-zA-Z_][a-zA-Z0-9_]*\s*\(", primera_linea)
    if match:
        nombre = match.group(0)
        nombre = nombre.replace("(", "")
        return nombre
    return "desconocido"

#esta funcion arma el reporte final 
def generarReporte(funciones):
    reporte = {
        "Snake": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []},
        "Camel": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []},
        "Pascal": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []},
        "Desconocido": {"funciones": 0, "nombres": [], "variables":0, "diferencias": 0, "errores": 0, "detalle": []}
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
        if reporte[autor]["funciones"] == 0:
            continue
        print("PRACTICANTE:", autor)
        print("- Funciones creadas:", reporte[autor]["funciones"])
        print("- Variables declaradas:", reporte[autor]["variables"])
        print("- Diferencias de estilo:", reporte[autor]["diferencias"])
        print("- Errores de sintaxis:", reporte[autor]["errores"])
        if reporte[autor]["errores"] > 0:
            for error in reporte[autor]["detalle"]:
                print("- Error en:", error)
                
#int main para llamar las funciones 
funciones = detectarFunciones()
guardarFunciones(funciones)
generarReporte(funciones)
    
    
    

        

