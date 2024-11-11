// Función para generar la tabla con la respuesta del backend
async function generarFrecuencia() {
    console.log("Iniciando la solicitud de frecuencia...");

    try {
        // Hacer la solicitud GET al backend para obtener la frecuencia
        const response = await fetch('/frecuencia', {
            method: 'GET', // Usamos GET porque el endpoint es un GET
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Verificamos si la respuesta es exitosa
        if (!response.ok) {
            throw new Error('Error al obtener los datos de frecuencia');
        }

        // Convertir la respuesta a JSON
        const data = await response.json();
        console.log("Datos recibidos del backend:", data);

        // Ahora que tenemos los datos, generamos la tabla
        generarTablaFrecuencia(data.data);

    } catch (error) {
        console.error("Hubo un error en la solicitud:", error);
    }

    console.log("Finalizó la solicitud de frecuencia.");
}

// Función para generar la tabla con los datos de frecuencia
function generarTablaFrecuencia(data) {
    const contenedorTabla = document.getElementById('imagenes-generadas'); // Cambié el contenedor aquí
    let html = '';

    // Iterar sobre las categorías y crear una tabla por cada categoría
    for (const categoria in data) {
        html += `<h3>${categoria}</h3>`;
        html += '<table border="1"><tr><th>Concepto</th><th>Frecuencia</th></tr>';
        
        // Iterar sobre los conceptos dentro de cada categoría
        for (const concepto in data[categoria]) {
            html += `<tr><td>${concepto}</td><td>${data[categoria][concepto]}</td></tr>`;
        }
        
        html += '</table><br>';
    }

    // Inyectar el HTML generado en el contenedor
    contenedorTabla.innerHTML = html;
}

// Asignar el evento al botón para generar la frecuencia
document.getElementById("generar-frecuencia").addEventListener("click", generarFrecuencia);


// Función para cargar y mostrar la nube de palabras
async function cargarNubePalabras() {
    console.log("Cargando la nube de palabras...");

    try {
        const response = await fetch('/nube_palabras', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener la nube de palabras');
        }

        const data = await response.json();
        
        if (data.status === 'success') {
            const resultContainer = document.getElementById('imagenes-generadas');
            
            // Limpiar el contenedor antes de mostrar la nube de palabras
            resultContainer.innerHTML = '';

            // Crear la imagen de la nube de palabras
            const img = document.createElement('img');
            img.src = `data:image/png;base64,${data.data}`;
            img.alt = 'Nube de Palabras';

            // Agregar la imagen al contenedor
            resultContainer.appendChild(img);
        } else {
            console.error("No se recibió una respuesta exitosa para la nube de palabras.");
        }

    } catch (error) {
        console.error("Error al cargar la nube de palabras:", error);
    }

    console.log("Finalizó la carga de la nube de palabras.");
}

// Asignar evento al botón para cargar la nube de palabras
document.getElementById('generar-nube-palabras').addEventListener('click', cargarNubePalabras);


// Función para cargar y mostrar el grafo generado
async function cargarGrafo() {
    console.log("Cargando el grafo...");

    try {
        const response = await fetch('/generar_grafo', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener la imagen del grafo');
        }

        const data = await response.json();

        if (data.status === 'success') {
            const resultContainer = document.getElementById('imagenes-generadas');
            
            // Limpiar el contenedor antes de mostrar el grafo
            resultContainer.innerHTML = '';

            // Crear la imagen del grafo
            const img = document.createElement('img');
            img.src = `data:image/png;base64,${data.data}`;
            img.alt = 'Grafo de Journals, Artículos y Países';

            // Agregar la imagen al contenedor
            resultContainer.appendChild(img);
        } else {
            console.error("No se recibió una respuesta exitosa para el grafo.");
        }

    } catch (error) {
        console.error("Error al cargar el grafo:", error);
    }

    console.log("Finalizó la carga del grafo.");
}

// Asignar evento al botón para cargar el grafo
document.getElementById('generar-grafo').addEventListener('click', cargarGrafo);


// Función para generar el gráfico con las variables seleccionadas
async function generarGrafico() {
    console.log("Iniciando la solicitud para generar el gráfico...");

    // Obtener las variables seleccionadas por el usuario
    const variable1 = document.getElementById("variable1").value;
    const variable2 = document.getElementById("variable2").value;

    try {
        // Hacer la solicitud al backend para obtener el gráfico
        const response = await fetch('/generar_grafico', {
            method: 'POST', // Usamos POST porque enviaremos los datos al backend
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                variable1: variable1,
                variable2: variable2
            })
        });

        // Verificamos si la respuesta es exitosa
        if (!response.ok) {
            throw new Error('Error al generar el gráfico');
        }

        // Convertir la respuesta a JSON
        const data = await response.json();
        console.log("Datos recibidos del backend:", data);

        // Comprobar si la respuesta es exitosa
        if (data.status === 'success') {
            const resultContainer = document.getElementById('imagenes-generadas');
            
            // Limpiar el contenedor antes de mostrar el gráfico
            resultContainer.innerHTML = '';

            // Crear la imagen del gráfico
            const img = document.createElement('img');
            img.src = `data:image/png;base64,${data.data}`; // Se espera que el backend retorne la imagen en base64
            img.alt = 'Gráfico generado';

            // Agregar la imagen al contenedor
            resultContainer.appendChild(img);
        } else {
            console.error("No se recibió una respuesta exitosa para el gráfico.");
        }

    } catch (error) {
        console.error("Hubo un error al generar el gráfico:", error);
    }

    console.log("Finalizó la solicitud para generar el gráfico.");
}

// Asignar evento al botón para generar el gráfico
document.getElementById('generar-estadisticos').addEventListener('click', generarGrafico);
