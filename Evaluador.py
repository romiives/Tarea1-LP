import re
#funcion para leer archivo
def leerArchivo():
    f = open("programa.txt")
    info = f.read()
    f.close()
    return info 

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
declaracion_funcion = r"(int|bool|char|string|void) ([a-z]+(_[a-z]+)*|[a-z]+([A-Z][a-z]+)*|[A-Z][a-z]+([A-Z][a-z]+)*)\(\)\{"
declaracion_variable = r"(int|bool|char|string|void) ([a-z]+(_[a-z]+)*|[a-z]+([A-Z][a-z]+)*|[A-Z][a-z]+([A-Z][a-z]+)*) (\+|-|/|\*|=|==|<|>) ([0-9]|true|false|\"[a-zA-Z][a-zA-Z0-9]*\"|'[a-zA-Z]\');"
retorno = r"return ([a-z]+(_[a-z]+)*|[a-z]+([A-Z][a-z]+)*|[A-Z][a-z]+([A-Z][a-z]+)*)"
comentario_one_line = r"//[a-zA-Z][a-zA-Z0-9]*"
comentario_multi_line = r"/\*[a-zA-Z][a-zA-Z0-9]*\*/"


