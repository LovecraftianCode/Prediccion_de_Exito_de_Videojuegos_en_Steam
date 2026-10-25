#  Prediccion de Exito de Videojuegos en Steam

##  Descripcion del Proyecto
Este proyecto utiliza tecnicas de Web Scraping y Machine Learning para predecir si un videojuego en Steam sera un exito comercial, basandose en sus metricas actuales de popularidad y calidad. 

**Definicion de Exito:** Un juego se considera exitoso si supera las **10,000 resenas** en la plataforma.

##  Tecnologias Utilizadas
*   **Python 3.12**
*   **Playwright:** Para la extraccion de datos (Web Scraping) de [SteamDB](https://steamdb.info/stats/gameratings/).
*   **Pandas & NumPy:** Para la limpieza y transformacion de datos.
*   **Scikit-Learn:** Para el modelado (Arbol de Decision).
*   **Matplotlib:** Para la visualizacion del arbol.

##  Proceso de Limpieza de Datos
Se extrajeron datos de mas de **9,500 juegos**. Durante la limpieza se realizaron las siguientes tareas:
<img width="953" height="848" alt="scrapper_debug" src="https://github.com/user-attachments/assets/410fac0d-53c9-4f9b-a93b-e15af7241261" />


1.  **Manejo de nulos:** Se eliminaron registros sin datos de pico de jugadores o seguidores.
2.  **Limpieza de precios:** Se transformaron textos como "Mex$ 129.99" y "Free" a valores numericos (float).
3.  **Limpieza de ratings:** Se removio el simbolo "%" y se convirtio a numerico.
4.  **Feature Engineering:** Se extrajo el ano de lanzamiento a partir del texto de la fecha.

##  Modelado y Resultados
Se entreno un **Arbol de Decision** (DecisionTreeClassifier) con una profundidad maxima de 4 niveles para evitar el sobreajuste. 

Debido al desbalance de clases (hay muchos mas juegos no exitosos que exitosos), se utilizo el parametro `class_weight='balanced'` con el objetivo de priorizar la deteccion de verdaderos positivos (juegos exitosos).

**Metricas del modelo:**
*   **Accuracy:** 90.07%
*   **Recall (Clase Exito):** 90% (El modelo es capaz de detectar al 90% de los juegos que seran exitosos).

###  Visualizacion del Arbol de Decision
Las variables mas importantes para predecir el exito son el **numero de seguidores** (`followers`), el **pico de jugadores concurrentes** (`peak`) y la **calificacion** (`rating`).

<img width="8197" height="2370" alt="arbol_decision_visual" src="https://github.com/user-attachments/assets/d5c4b863-d35e-446f-b575-a046b42338c8" />


##  Proximos Pasos
*   Extraer la categoria/genero de cada videojuego mediante la API de SteamSpy para enriquecer el modelo.
*   Probar modelos de ensamble como Random Forest o XGBoost.
