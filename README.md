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

Dentro de los archivos que encontrarán en este repositorio estará el archivo generado, lo que proporcionará una idea de cómo se muestra una vez generado. Es de suma importancia mencionar que, ese NO es el archivo que se comparte a la líder sino que luego se realizan ajustes para compartirlo por medio de correo corporativo con la etiqueta que corresponda.

## Paso a paso 
1. Abrir un libro en blanco en Excel: Inicia Excel y crea un nuevo libro en blanco.
2.Pestaña de datos y Obtener datos: Dirígete a la pestaña "Datos" en la barra de menú superior. Hacer en el botón "Obtener datos" y selecciona la opción que te permita importar datos desde un archivo CSV. Selecciona el archivo generado por el script de Python.
3.Vista previa y transformación de datos: Una vez que se carguen los datos, se mostrará una vista previa de los mismos. Haz clic en el botón "Transformar datos" para abrir el Editor de Power Query.
5. Configuración de la consulta en Power Query: En el Editor de Power Query, en la parte derecha de la pantalla, aparecerá la configuración de la consulta. Aquí, buscar y hacer clic en la "X" al lado de cualquier "TIPO CAMBIADO". Esto es puede ser cambios en el tipo de datos que Power Query haya aplicado automáticamente.
6. Cierre y carga de la tabla: Una vez realizados los ajustes necesarios en la configuración de la consulta, cerrar el Editor de Power Query.
7. Reemplazo de puntos por comas: Es esencial reemplazar los puntos por comas en las columnas necesarias para ajustar los datos según lo esperado.
