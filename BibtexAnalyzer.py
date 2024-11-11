# bibtex_analyzer.py
from io import BytesIO
import base64
import random
import networkx as nx
from collections import Counter

from BibtexReader import BibtexReader
import os
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt

EQUIVALENCES = {
    "Classical Test Theory": ["Classical Test Theory", "CTT"],
    "Confirmatory Factor Analysis": ["Confirmatory Factor Analysis", "CFA"],
    "Exploratory Factor Analysis": ["Exploratory Factor Analysis", "EFA"],
    "Item Response Theory": ["Item Response Theory", "IRT"],
    "Structural Equation Model": ["Structural Equation Model", "SEM"],
}

CATEGORIES = {
    "Habilidades": [
        "Abstraction", "Algorithm", "Algorithmic thinking", "Coding", "Collaboration",
        "Cooperation", "Creativity", "Critical thinking", "Debug", "Decomposition",
        "Evaluation", "Generalization", "Logic", "Logical thinking", "Modularity",
        "Patterns recognition", "Problem solving", "Programming", "Representation",
        "Reuse", "Simulation"
    ],
    "ConceptosComputacionales": [
        "Conditionals", "Control structures", "Directions", "Events", "Functions",
        "Loops", "Modular structure", "Parallelism", "Sequences", "Software/hardware", "Variables"
    ],
    "Actitudes": [
        "Emotional", "Engagement", "Motivation", "Perceptions", "Persistence",
        "Self-efficacy", "Self-perceived"
    ],
    "Propiedades psicométricas": [
        "Classical Test Theory - CTT", "Confirmatory Factor Analysis - CFA", "Exploratory Factor Analysis - EFA",
        "Item Response Theory (IRT) - IRT", "Reliability", "Structural Equation Model - SEM", "Validity"
    ],
    "Herramienta de evaluación": [
        "Beginners Computational Thinking test - BCTt", "Coding Attitudes Survey - ESCAS",
        "Collaborative Computing Observation Instrument", "Competent Computational Thinking test - cCTt",
        "Computational thinking skills test - CTST", "Computational concepts",
        "Computational Thinking Assessment for Chinese Elementary Students - CTA-CES",
        "Computational Thinking Challenge - CTC", "Computational Thinking Levels Scale - CTLS",
        "Computational Thinking Scale - CTS", "Computational Thinking Skill Levels Scale - CTS",
        "Computational Thinking Test - CTt", "Computational Thinking Test",
        "Computational Thinking Test for Elementary School Students - CTT-ES",
        "Computational Thinking Test for Lower Primary - CTtLP", "Computational thinking-skill tasks on numbers and arithmetic",
        "Computerized Adaptive Programming Concepts Test - CAPCT", "CT Scale - CTS",
        "Elementary Student Coding Attitudes Survey - ESCAS", "General self-efficacy scale",
        "ICT competency test", "Instrument of computational identity", "KBIT fluid intelligence subtest",
        "Mastery of computational concepts Test and an Algorithmic Test",
        "Multidimensional 21st Century Skills Scale", "Self-efficacy scale", "STEM learning attitude scale - STEM-LAS",
        "The computational thinking scale"
    ],
    "Diseño de investigación": [
        "No experimental", "Experimental", "Longitudinal research", "Mixed methods",
        "Post-test", "Pre-test", "Quasi-experiments"
    ],
    "Nivel de escolaridad": [
        "Upper elementary education - Upper elementary school", "Primary school - Primary education - Elementary school",
        "Early childhood education – Kindergarten - Preschool", "Secondary school - Secondary education",
        "High school - Higher education", "University – College"
    ],
    "Medio": [
        "Block programming", "Mobile application", "Pair programming", "Plugged activities",
        "Programming", "Robotics", "Spreadsheet", "STEM", "Unplugged activities"
    ],
    "Estrategia": [
        "Construct-by-self mind mapping - CBS-MM", "Construct-on-scaffold mind mapping - COS-MM",
        "Design-based learning - CTDBL", "Design-based learning - DBL", "Evidence-centred design approach",
        "Gamification", "Reverse engineering pedagogy - REP", "Technology-enhanced learning",
        "Collaborative learning", "Cooperative learning", "Flipped classroom", "Game-based learning",
        "Inquiry-based learning", "Personalized learning", "Problem-based learning",
        "Project-based learning", "Universal design for learning"
    ],
    "Herramienta": [
        "Alice", "Arduino", "Scratch", "ScratchJr", "Blockly Games", "Code.org", "Codecombat",
        "CSUnplugged", "Robot Turtles", "Hello Ruby", "Kodable", "LightbotJr", "KIBO robots",
        "BEE BOT", "CUBETTO", "Minecraft", "Agent Sheets", "Mimo", "Py– Learn", "SpaceChem"
    ]
}


class BibtexAnalyzer:
    def __init__(self):
        """
        Inicializa el analizador con las entradas de BibTeX y las equivalencias de variables.
        """
        # Asegúrate de que el archivo .bib esté en la ubicación correcta
        file_path = os.path.join(os.path.dirname(__file__), 'todo_filtrado.bib')
        self.reader = BibtexReader(file_path)
        self.categories = CATEGORIES
        self.equivalences = EQUIVALENCES
        self.frequencyTable = None  # Inicializa como None o un diccionario vacío
        self.entries = self.reader.load_entries()
        self.graph = nx.Graph()

##REQUISITO 2

    def plot_graph(self, variable1, variable2):
        """
        Dibuja un gráfico basado en las dos variables proporcionadas,
        limitando a los 15 pares más frecuentes y devuelve el gráfico
        como una imagen en formato base64.
        """
        # Inicializamos las listas de agrupación
        var1_values = []
        var2_values = []
        
        # Extraemos las variables correspondientes de cada entrada
        for entry in self.entries:
            if variable1 in entry and variable2 in entry:
                var1_values.append(entry[variable1])
                var2_values.append(entry[variable2])

        # Contamos las ocurrencias de cada par de valores
        data = Counter(zip(var1_values, var2_values))

        # Ordenamos los resultados por cantidad de publicaciones (en orden descendente)
        top_data = data.most_common(15)

        # Separar los resultados para graficarlos
        labels = [f"{v[0][0]} - {v[0][1]}" for v in top_data]
        counts = [v[1] for v in top_data]
        
        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.barh(labels, counts, color='skyblue')
        plt.title(f'Publicaciones por {variable1} y {variable2}')
        plt.xlabel('Cantidad de Publicaciones')
        plt.ylabel(f'{variable1} - {variable2}')
        plt.tight_layout()

        # Convertir la imagen del gráfico a base64
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='PNG')  # Guarda la imagen en el buffer de memoria
        plt.close()  # Cerrar la figura para liberar memoria
        img_buffer.seek(0)
        
        # Convertir el contenido del buffer en base64
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return img_base64

##REQUISITO 3
    def analyze_frequency(self):
        """
        Analiza la frecuencia de aparición de las variables en los abstracts.
        :return: Diccionario con la frecuencia de las variables por categoría.
        """
        logging.debug("Iniciando la ejecución de analyze_frequency...")
        
        frequency_data = {}

        # Inicializa el diccionario por cada categoría
        for category in self.categories:
            frequency_data[category] = {}

        # Procesar los abstracts
        for entry in self.entries:
            abstract = entry.get('abstract', '').lower()  # Convertir el abstract a minúsculas

            for category, variables in self.categories.items():
                for variable in variables:
                    # Unificar las equivalencias
                    for eq in self.equivalences.get(variable, [variable]):
                        eq_lower = eq.lower()

                        # Si la variable contiene un guion, dividir en ambas partes y contar cada una
                        if "-" in eq_lower:
                            part1, part2 = map(str.strip, eq_lower.split("-", 1))
                            count = abstract.count(part1) + abstract.count(part2)
                        else:
                            count = abstract.count(eq_lower)

                        # Agregar el conteo al diccionario de frecuencias
                        if eq_lower not in frequency_data[category]:
                            frequency_data[category][eq_lower] = 0
                        frequency_data[category][eq_lower] += count

        logging.debug("Finalizando analyze_frequency...")
        self.frequencyTable = frequency_data  # Actualiza el atributo de instancia
        return frequency_data


##REQUISITO 4
    def plot_word_cloud(self):
        """
        Genera y devuelve una nube de palabras en formato base64.
        """
        # Combinar todas las frecuencias en un solo diccionario
        combined_frequencies = {}
        for category, words in self.frequencyTable.items():
            for word, freq in words.items():
                combined_frequencies[word] = combined_frequencies.get(word, 0) + freq

        # Generar la nube de palabras
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(combined_frequencies)

        # Convertir la imagen de la nube de palabras a base64
        img_buffer = BytesIO()
        wordcloud.to_image().save(img_buffer, format="PNG")
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        return img_base64

##REQUISITO 5
    def get_top_10_journals(self):
        """
        Identifica los 10 journals con la mayor cantidad de artículos publicados.
        Si un artículo no tiene el nombre del journal, se utiliza el campo ISSN.
        
        :return: Lista de los 10 journals con más artículos publicados.
        """
        journal_counts = {}

        for entry in self.entries:
            journal_name = entry.get('journal') or entry.get('issn')
            if journal_name:
                journal_counts[journal_name] = journal_counts.get(journal_name, 0) + 1

        self.top_10_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return self.top_10_journals

    def get_top_articles_with_random_country(self):
        """
        Para cada uno de los 10 journals principales, selecciona los primeros 5 artículos
        y asigna un país aleatorio a cada uno.
        
        :return: Diccionario con los journals y una lista de los 5 artículos con país asignado.
        """
        countries = [
            'USA', 'UK', 'Germany', 'Canada', 'Australia', 'France', 'Japan', 'China', 'India', 'Brazil', 
            'Mexico', 'Italy', 'South Korea', 'Spain', 'Russia', 'Netherlands', 'Turkey', 'Switzerland', 
            'Sweden', 'Belgium', 'Argentina', 'Norway', 'Austria', 'Denmark', 'South Africa', 'Ireland', 
            'New Zealand', 'Singapore', 'Finland', 'Poland', 'Greece', 'Portugal', 'Czech Republic', 
            'Israel', 'Chile', 'Hungary', 'Saudi Arabia', 'Colombia', 'Philippines', 'Malaysia', 
            'United Arab Emirates', 'Thailand', 'Egypt', 'Indonesia', 'Vietnam', 'Pakistan', 'Nigeria', 
            'Bangladesh', 'Ukraine', 'Romania', 'Peru', 'Hong Kong', 'Venezuela', 'Ecuador', 'Morocco', 
            'Slovakia', 'Bulgaria', 'Croatia', 'Lithuania', 'Slovenia', 'Estonia', 'Latvia', 'Serbia', 
            'Iceland', 'Luxembourg', 'Malta', 'Cyprus', 'Jordan', 'Uruguay', 'Panama', 'Bolivia', 'Paraguay', 
            'Honduras', 'El Salvador', 'Costa Rica', 'Guatemala', 'Trinidad and Tobago', 'Bosnia and Herzegovina', 
            'Macedonia', 'Montenegro', 'Albania', 'Georgia', 'Armenia', 'Azerbaijan', 'Kazakhstan'
        ]
        
        journal_articles = {}

        for journal in self.top_10_journals:
            journal_id = journal[0]
            articles = [entry for entry in self.entries if entry.get('journal') == journal_id or entry.get('issn') == journal_id]
            selected_articles = articles[:5]

            articles_with_countries = [
                {
                    'title': article.get('title', 'No title'),
                    'country': random.choice(countries)
                }
                for article in selected_articles
            ]

            journal_articles[journal_id] = articles_with_countries

        return journal_articles

    def create_graph(self):
        """
        Crea el grafo que relaciona journals, artículos y países.
        """
        self.get_top_10_journals()  # Asegurarse de obtener y almacenar los 10 journals
        journal_articles = self.get_top_articles_with_random_country()

        for journal, articles in journal_articles.items():
            self.graph.add_node(journal, type='journal')

            for article_info in articles:
                article_title = article_info['title']
                country = article_info['country']

                self.graph.add_node(article_title, type='article')
                self.graph.add_node(country, type='country')

                # Crear las aristas (edges) entre los journals, artículos y países
                self.graph.add_edge(journal, article_title)
                self.graph.add_edge(article_title, country)

    def generate_graph(self):
        """
        Genera y devuelve el grafo en formato base64.
        """
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        journals = [node for node, attr in self.graph.nodes(data=True) if attr["type"] == "journal"]
        articles = [node for node, attr in self.graph.nodes(data=True) if attr["type"] == "article"]
        countries = [node for node, attr in self.graph.nodes(data=True) if attr["type"] == "country"]

        # Crear la figura del grafo
        plt.figure(figsize=(25, 25))
        nx.draw_networkx_nodes(self.graph, pos, nodelist=journals, node_color="lightcoral", node_size=2000, label="Journals")
        nx.draw_networkx_nodes(self.graph, pos, nodelist=articles, node_color="skyblue", node_size=1500, label="Articles")
        nx.draw_networkx_nodes(self.graph, pos, nodelist=countries, node_color="lightgreen", node_size=1000, label="Countries")
        nx.draw_networkx_edges(self.graph, pos, edge_color="gray", alpha=0.5)
        nx.draw_networkx_labels(self.graph, pos, font_size=5, font_weight="bold")

        # Convertir la figura del grafo a base64 en lugar de guardarla en el disco
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='PNG')  # Guarda la imagen en el buffer de memoria
        plt.close()  # Cerrar la figura para liberar memoria
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return img_base64
