import os 
import pandas as pd
from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    datos_juegos = []
    url = "https://steamdb.info/stats/gameratings/?min_reviews=500"
    print(f"Navegando a {url}...")
    page.goto(url)
    page.wait_for_selector("#DataTables_Table_0 tbody tr", timeout=30000)
    time.sleep(3)

    # --- 1. OBTENER LOS NOMBRES DE LAS COLUMNAS ---
    # Buscamos todos los <th> de la tabla y extraemos su atributo 'data-name'
    encabezados = page.locator("#DataTables_Table_0 thead th").all()
    nombres_columnas = []
    for encabezado in encabezados:
        nombre = encabezado.get_attribute("data-name")
        if nombre: # Ignoramos si no tiene nombre
            nombres_columnas.append(nombre)
    
    print(f"Columnas detectadas: {nombres_columnas}")
    # Nota: 'logo' estara en la lista, pero luego lo ignoraremos al extraer.

    total_paginas = 2 # Intentaremos hasta la 100

    for num_pagina in range(1, total_paginas + 1):
        print(f"\n--- Extrayendo pagina {num_pagina} ---")
        
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.5)
        
        filas = page.locator("#DataTables_Table_0 tbody tr").all()
        
        for fila in filas:
            # En lugar de agarrar todos los <td>, iteramos sobre los encabezados para saber que columna es cual
            datos_fila = {}
            celdas = fila.locator("td").all()
            
            # Nos aseguramos de que haya suficientes celdas
            if len(celdas) < len(nombres_columnas):
                continue

            for i, nombre_col in enumerate(nombres_columnas):
                # Si la columna es 'logo', la saltamos (esta en el indice 1)
                if nombre_col == "logo":
                    continue
                
                # Extraemos el texto de la celda correspondiente
                texto = celdas[i].text_content().strip()
                # Si el texto esta vacio, lo dejamos como string vacio
                datos_fila[nombre_col] = texto
            
            datos_juegos.append(datos_fila)
        
        print(f"Se extrajeron {len(filas)} juegos en esta pagina.")

        # --- 2. NAVEGACION ---
        if num_pagina < total_paginas:
            pagina_siguiente = str(num_pagina + 1)
            try:
                # Intentamos hacer clic en el numero de la pagina siguiente
                # Si no esta visible, Playwright fallara y cazaremos el error
                page.get_by_role("link", name=pagina_siguiente, exact=True).click(force=True, timeout=5000)
                time.sleep(3)
            except Exception as e:
                print(f" No se pudo avanzar a la pagina {pagina_siguiente}. Posiblemente no esta visible.")
                print("Intentando hacer clic en el boton 'Siguiente' (Next)...")
                try:
                    # Si falla, intentamos con el boton 'Next' estandar de DataTables
                    page.locator("a.paginate_button.next").click(force=True, timeout=5000)
                    time.sleep(3)
                except:
                    print(" No se pudo navegar a la siguiente pagina. Deteniendo extraccion.")
                    break

    context.close()
    browser.close()
    return datos_juegos

with sync_playwright() as playwright:
    lista_datos = run(playwright)

if lista_datos:
    df = pd.DataFrame(lista_datos)
    
    # Limpiamos las comas de los numeros (ej. "1,113,494" -> 1113494)
    # para que Pandas los reconozca como numeros y no como texto.
    columnas_numericas = ['followers', 'reviews', 'peak']
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = df[col].str.replace(',', '', regex=False)
    
    # Convertimos a numerico
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
    df['peak'] = pd.to_numeric(df['peak'], errors='coerce')
    df['followers'] = pd.to_numeric(df['followers'], errors='coerce')

    # Guardamos
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(carpeta_actual, "steamdb_ratings_limpio.csv")
    df.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
    print(f"\n Se guardaron {len(df)} juegos en 'steamdb_ratings_limpio.csv'")
else:
    print("\n No se obtuvieron datos.")