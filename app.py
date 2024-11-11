from flask import Flask, render_template, request, jsonify, send_file
import io
import matplotlib

matplotlib.use('Agg')  # Establece el backend a uno sin GUI
import matplotlib.pyplot as plt
import random
from flask_cors import CORS
# En app.py
from src.bibtex_analyzer import BibtexAnalyzer
app = Flask(__name__)  # Primero creas la aplicación Flask
CORS(app)  # Luego habilitas CORS para todas las rutas

# Ruta principal para servir la interfaz
@app.route('/')
def home():
    return render_template('index.html')


# Endpoint para generar estadísticos (Requerimiento 2 - 4 gráficos)
@app.route('/generar_grafico', methods=['POST'])
def estadisticos():
    # Obtén los valores de variable1 y variable2 desde la solicitud o usa valores predeterminados
    variable1 = request.json.get('variable1')
    variable2 = request.json.get('variable2')
    
    # Crea una instancia del analizador y genera el gráfico
    analyzer = BibtexAnalyzer()
    wordcloud_base64 = analyzer.plot_graph(variable1, variable2)
    
    # Devolver la imagen de la nube de palabras en formato base64
    return jsonify({'status': 'success', 'data': wordcloud_base64})


@app.route('/frecuencia', methods=['GET'])
def frecuencia():
    """
    Endpoint para analizar la frecuencia de aparición de variables en los abstracts.
    """
    # Crear una instancia de BibtexAnalyzer
    analyzer = BibtexAnalyzer()

    # Ejecutar el análisis de frecuencia
    frequency_data = analyzer.analyze_frequency()

    # Retornar los datos de frecuencia como respuesta JSON
    return jsonify({'status': 'success', 'data': frequency_data})

@app.route('/nube_palabras', methods=['GET'])
def nube_palabras():
    """
    Endpoint para generar una nube de palabras y retornarla en formato base64.
    """
    analyzer = BibtexAnalyzer()
    # Asegúrate de haber ejecutado `analyze_frequency` previamente para tener `frequencyTable` completo
    analyzer.analyze_frequency()
    
    # Generar la nube de palabras
    wordcloud_base64 = analyzer.plot_word_cloud()
    
    # Devolver la imagen de la nube de palabras en formato base64
    return jsonify({'status': 'success', 'data': wordcloud_base64})

@app.route('/generar_grafo', methods=['GET'])
def generar_grafo():
    analyzer = BibtexAnalyzer()
    # Llama a la función que genera el grafo
    analyzer.create_graph()  # Primero crea el grafo con nodos y aristas
    wordcloud_base64 = analyzer.generate_graph()  # Luego genera la disposición y configuración del grafo

    # Devolver la imagen de la nube de palabras en formato base64
    return jsonify({'status': 'success', 'data': wordcloud_base64})

# Para pruebas locales, podemos usar el puerto estándar
if __name__ == '__main__':
    app.run(debug=True)
