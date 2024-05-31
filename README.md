# PrimaPromocomercio
Este proceso se ejecuta mensualmente cuando el equipo de Estrategia de Negocios actualiza la información en las siguientes tablas: 
[Cartera].[dbo].[Prima_promocomercio_base_inicio_producto70]
[Cartera].[dbo].[Reporte_recaudos_baseusegundametadiaria(Promocomercio)].
Una vez actualizadas las tablas, utilizamos un script en Python para generar el archivo Excel correspondiente. Este archivo se envía posteriormente a las partes interesadas. 
El objetivo de este proceso es asegurar que la información esté actualizada y disponible para su análisis y toma de decisiones.

# Accesos y Programas Requeridos

Para ejecutar el script de Python, puedes utilizar Anaconda o Visual Studio Code. Es imprescindible tener acceso a las tablas mencionadas previamente, las cuales se encuentran en el servidor 192.168.50.175\PLANNING.

# Tiempo de Ejecución

El tiempo de ejecución debe ser inferior a 5 minutos.

# Archivos Generados

El archivo generado es un CSV (Comma-Separated Values), compatible con Microsoft Excel y otros programas de hojas de cálculo. Es crucial cambiar la ruta donde se aloja el archivo mencionado después de la ejecución del script.

### Nota: 

Dentro de los archivos que encontrarán en este repositorio estará el archivo generado, lo que proporcionará una idea de cómo se muestra una vez generado. Es de suma importancia mencionar que, ese NO es el archivo que se comparte a la líder sino que luego se realizan ajustes para compartirlo por medio de correo corporativo con la etiqueta quee corresponda 

# 
