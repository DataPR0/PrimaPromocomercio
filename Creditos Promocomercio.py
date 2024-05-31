import pandas as pd
import os
import numpy as np
pd.set_option('display.float_format', '{:.2f}'.format)
import pyodbc # Importando la librería pyodbc para conectarse a bases de datos ODBC 

cnxn = pyodbc.connect('DRIVER=SQL Server;Server=192.168.50.175\planning;Database=Cartera;Port=1433;Trusted_Connection=yes')

os.chdir(r"C:\Users\maryi.trujillo\Documents\Prima Promocomercio")

cnxn = pyodbc.connect('DRIVER=SQL Server;Server=192.168.50.175\planning;Database=Cartera;Port=1433;Trusted_Connection=yes')

# df_original = pd.read_excel("Base incio producto 70.xlsx", sheet_name="Base")

df_original = pd.read_sql(sql= "SELECT * FROM [Cartera].[dbo].[Prima_promocomercio_base_inicio_producto70];", con=cnxn)

# names = ["credito", "Año+mes informacion desde comite", "Saldocapital", "numero_dias_mora", "valor recaudado", "Año+Mes inicio como producto 70"]

#  Se debe conservar el valor de Recaudo Original
df_original["valor recaudado Original"] = df_original["valor recaudado"]

# todos los recaudos negativos se pasan a 0
df_original.loc[df_original["valor recaudado"] < 0, "valor recaudado"] = 0

#  Se transforma la columna a fecha
df_original["Fecha"] = pd.to_datetime(df_original["Año+mes informacion desde comite"].astype(int), format='%Y%m')

# Se ordena el dataframe primero por numero de Credito, y luego por fecha
df_original.sort_values(["credito", "Fecha"], inplace=True)

# Se resetea el indice
df_original.reset_index(drop=True, inplace=True)


# indices de los saldo a capital y valore recaudo = 0
index_drop =  df_original[(df_original["Saldocapital"] == 0) & (df_original["valor recaudado"] == 0)].index

# eliminamos los que son saldo a capital y valor recaudo = 0
df = df_original[~df_original.index.isin(index_drop)].copy().reset_index(drop=True)

# df = df_original.copy()

#Rango de Mora Maxima
criteria = [df["numero_dias_mora"].between(0,90), 
        df["numero_dias_mora"].between(91,180), 
        df["numero_dias_mora"].between(181,360), 
        df["numero_dias_mora"].between(360,1000000)]


# Posibles valores de rango de mora
values = ["0 a 90", "91 a 180", "181 a 360", "> 360"]

# Se asignan los valores de rango de mora
df['rango de mora'] = np.select(criteria, values, 0)

# Diccionario para mapear el rango de mora a un código
mora_map = {"0 a 90": 0, "91 a 180": 1, "181 a 360": 2, "> 360": 3}

# Convertir rango de mora a código usando el diccionario
df['codigo_mora'] = df['rango de mora'].map(mora_map)


# posibles reglas

# Regla de 3 (> 360)
# 1. de "> 360" a "0 a 90": -3 que debe ser 4 "0 a 90" 
# 2. de "> 360" a "91 a 180": -2 que debe ser 3 "91 a 180" 
# 3. de "> 360" a "181 a 360": -1 que debe ser 2 "181 a 360" 

# Regla de 2 ("181 a 360")
# 1. de "181 a 360" a "0 a 90": -2 que debe ser 4 "0 a 90" 
# 2. de "181 a 360" a "91 a 180": -1 que debe ser 3 "91 a 180" 
# 3. de "181 a 360" a "> 360": 1 que debe ser 5 "> 360" 

# Regla de 1 ("181 a 360")
# 1. de "91 a 180" a "0 a 90": -1 que debe ser 4 "0 a 90" 
# 2. de "91 a 180" a "181 a 360": 1 que debe ser 5 "181 a 360" 
# 3. de "91 a 180" a "> 360": 2 que debe ser 5 "> 360" 

# Regla de 1 ("181 a 360")
# 1. de "0 a 90" a "91 a 180": 1 que debe ser 5 "91 a 180" 
# 2. de "0 a 90" a "181 a 360": 2 que debe ser 5 "181 a 360" 
# 3. de "0 a 90" a "> 360": 3 que debe ser 5 "> 360" 

# Función para determinar el código según el cambio en el rango de mora
# def asignar_codigo(grupo):
#     grupo['codigo_cambio'] = grupo['codigo_mora'].diff()
#     grupo['codigo_cambio'] = grupo['codigo_cambio'].map({-1: 2, -2: 3, -3: 4, 1: 5, 2: 5, 3: 5, 0:"same"})
#     return grupo

# Diccionario de codigos segun si se recupera o mantiene
recupera_mantiene_map = {0: 8, 1: 6, 2: 4, 3: 2}

def asignar_valor(grupo):
    grupo['Puntaje Rodamiento'] = -grupo['codigo_mora'].diff() 

    # Si el crédito se recuperó o se mantuvo
    grupo.loc[grupo['Puntaje Rodamiento'] > 0, 'Puntaje Rodamiento'] = grupo.loc[grupo['Puntaje Rodamiento'] > 0, 'codigo_mora'].map(recupera_mantiene_map)

    # Si el crédito se deterioró
    grupo.loc[grupo['Puntaje Rodamiento'] < 0, 'Puntaje Rodamiento'] = 10

    # Si el crédito se mantuvo en el mismo rango
    grupo.loc[grupo['Puntaje Rodamiento'] == 0, 'Puntaje Rodamiento'] = grupo.loc[grupo['Puntaje Rodamiento'] == 0, 'codigo_mora'].map(recupera_mantiene_map)

    return grupo



# Aplicar la función al dataframe agrupado por 'credito'
df = df.groupby('credito', as_index=False).apply(asignar_valor)

df.reset_index(drop=True, inplace=True)

# Establecer el valor por defecto para filas donde 'codigo_cambio' todavía es 'same'
# df.loc[df['codigo_cambio'] == "same", 'codigo_cambio'] = 1

# Diccionario para mapear el rango de mora a un código si no hay cambio
# mora_map_sin_cambio = {"0 a 90": 4, "91 a 180": 3, "181 a 360": 2, "> 360": 1}

# Llenar los valores NA en 'codigo_cambio' con los valores correspondientes de 'rango de mora' si no hay cambio
# df['codigo_cambio'] = df['codigo_cambio'].fillna(df['rango de mora'].map(mora_map_sin_cambio))

# lista vacia
l1 = []

# se itera sobre la totalidad de las filas
for i in np.arange(df.shape[0]):  
    # se conoce la condicion de su saldo a capital es > 0
    if df["Saldocapital"][i] > 0:
        # si es > 0: valores recaudo/saldo a capital
        l1.append(df["valor recaudado"][i]/df["Saldocapital"][i])
    # si se conoce que saldo a capital = 0 Y valor del recaudo > 0
    elif (df["Saldocapital"][i] <= 0) and (df["valor recaudado"][i]>0):
        # se dice que se recupero el 100% (1)
        l1.append(1)
    else:
        l1.append(np.nan)

len(l1)

# Se asigna los valores de las lista    
df["recaudo/Saldo a Capital"] = l1


# Lista vacia para almacenar el Umbral
umbral = []
for i in np.arange(df.shape[0]):
    # Se analiza segun las condicines que se tengan
    if df["rango de mora"][i] == "0 a 90" and df['recaudo/Saldo a Capital'][i] >= 0.1005:
        umbral.append(10)
    elif df["rango de mora"][i] == "91 a 180" and df['recaudo/Saldo a Capital'][i] >= 0.2190:
        umbral.append(8)
    elif df["rango de mora"][i] == "181 a 360" and df['recaudo/Saldo a Capital'][i] >= 0.0634:
        umbral.append(4)   
    elif df["rango de mora"][i] == "> 360" and df['recaudo/Saldo a Capital'][i] >= 0.0232:
        umbral.append(2)
    else:
        umbral.append(10)  

# Se agregan los valores de la lista
df["Puntaje Recaudo"] = umbral

# Para el puntaje de rodamiento, se reemplazan los valores tipo NaN por 0
df["Puntaje Rodamiento"] = df["Puntaje Rodamiento"].replace(np.nan, 0)

#  se unen las dos bases
df_final =  pd.concat([df, df_original[df_original.index.isin(index_drop)]], axis="index")

# Se suman los dos puntajes
df_final["Suma Puntaje"] = df_final["Puntaje Rodamiento"] + df_final["Puntaje Recaudo"]

# funcion para dejar la primera observacion de "Suma Puntaje" en 0
def primera_obs(data):
    # todas los primeros registros de la columna "Suma Puntaje", se pasan a 0
    data.iloc[0, df_final.shape[1]-1] = 0
    
    return data

# Se aplica la funcion
df_final = df_final.groupby("credito").apply(primera_obs)

df_final.reset_index(drop = True, inplace = True)

# df_final[df_final["credito"] == 17160]
# df_final[df_final["credito"] == 210812]

# Se divide la suma puntaje por 100 para sacar la proporcion
df_final["prop. Prima"] = df_final["Suma Puntaje"]/100

# Se multiplica la Proporcion de la prima por el valor original del valor recaudo
df_final["Valor prima"] = df_final["prop. Prima"]*df_final["valor recaudado Original"]

df_original["credito"].nunique()

df_final["credito"].nunique()

# df_final.sort_values('valor recaudado Original')

df_final.to_csv("Prima Promocomercio 2024-05-marzo.csv", index=False)

os.startfile("Prima Promocomercio 2024-05-marzo.csv")

os.getcwd()

