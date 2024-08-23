import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, jsonify, request

# 1. Web Scraping (Obteniendo datos de una página web)

# URL de la página web de la que queremos extraer datos
PAGINA_PRINCIPAL = "https://www.scrapethissite.com/pages/forms/"

# Abrimos el navegador (como si lo abriéramos manualmente)
navegador = webdriver.Chrome()

# Vamos a la página web que queremos visitar
navegador.get(PAGINA_PRINCIPAL)  

# Esperamos un poco para asegurarnos de que la página esté cargada
navegador.implicitly_wait(10)

# Creamos una lista vacía para guardar los datos que vamos a extraer
datos = []

# Encontramos todos los elementos en la página que contienen información de los equipos
equipos = navegador.find_elements(By.CLASS_NAME, 'team')

# Recorremos cada equipo encontrado y extraemos su información
for equipo in equipos:
    # Extraemos el nombre del equipo
    nombre = equipo.find_element(By.CLASS_NAME, 'name')
    # Extraemos el año en que el equipo jugó
    year = equipo.find_element(By.CLASS_NAME, 'year')
    # Extraemos cuántos partidos ganó el equipo
    wins = equipo.find_element(By.CLASS_NAME, 'wins')
    # Extraemos cuántos partidos perdió el equipo
    losses = equipo.find_element(By.CLASS_NAME, 'losses')

    # Guardamos toda esta información en la lista 'datos'
    datos.append({
        'Nombre': nombre.text,
        'Año': year.text,
        'Victorias': wins.text,
        'Derrotas': losses.text
    })

# Cerramos el navegador cuando terminamos de extraer los datos
navegador.quit()

# Creamos un DataFrame (como una tabla en Excel) con los datos extraídos
df = pd.DataFrame(datos)

# Mostramos la tabla en la consola para asegurarnos de que los datos se extrajeron correctamente
print(df)

# Guardamos la tabla en un archivo de Excel para poder usarla más tarde
ruta = "C:/Users/usuario/Downloads/PROYECTO_FINAL_NAYIB/proyecto_final_nayib.csv"
df.to_csv(ruta, index=False)


# 2. Desarrollo de una API con Flask (Un lugar para compartir los datos en internet)

# Creamos una aplicación Flask para manejar las solicitudes de datos
app = Flask(__name__)

# Definimos una ruta ('/api/datos') donde otros pueden pedir los datos
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    # Buscamos si el usuario quiere filtrar los datos por el nombre de algún equipo
    filtro = request.args.get('filtro', default=None, type=str)
    
    # Si hay un filtro, solo mostramos los equipos que coinciden con ese filtro
    if filtro:
        datos_filtrados = df[df['Nombre'].str.contains(filtro, case=False, na=False)]
    # Si no hay filtro, mostramos todos los datos
    else:
        datos_filtrados = df
    
    # Devolvemos los datos como un archivo JSON para que la computadora del usuario pueda entenderlo
    return jsonify(datos_filtrados.to_dict(orient='records'))

# Ponemos la aplicación en marcha para que esté lista para recibir solicitudes
if __name__ == '__main__':
    app.run(debug=True)
