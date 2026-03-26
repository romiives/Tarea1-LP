Alumno = Romina Valdés
Rol = 202473517-9

## Descripción
Mi programa analiza un archivo "programa.txt" el cual contiene funciones escritas en un lenguaje tipo C, el ejemplo que tome de archivo fue el que venía incluido en el pdf de la tarea pero le agregue casos de funciones que se incluiran en un estilo desconocido. El código incluido en Evaluador.py detecta cada función, clasifica su estilo (pudiendo ser snake, camel o pascal) y genera archivos separados por cada estilo, incluyendo un archivo para casos desconocidos. También, siguiendo lo mencionado en la tarea, el código realiza un análisis básico de sintaxis, detecta errores como la falta de punto y coma o bloques sin cerrar (estructura de una función).

## Ejecución del código
Quiero mecionar que en mi código se consideran los siguientes casos:
- Agregue funciones como "mi_Funcion" y "calcular" para poder clasificarlas como "Desconocido"
- Las funciones que estan dentro de un bloque mal cerrado son detectadas y tratadas como nuevas funciones.
- Se detectan errores de sintaxis como mencione en la descripción.
- Se generan los siguientes archivos: snake.txt, camel.txt, pascal.txt y desconocido.txt

## Sobre el código
- Utilicé re.fullmatch en lugar de re.match para asegurar que el nombre de la función cumpla con lo pedido.
- En mi código definí expresiones regulares globales para identificar los estilos pero como se podrá observar en algunos casos opté por no utilizarlas directamente ya que al ser muy estrictas no me detectaba correctamente lo que necesitaba. 







