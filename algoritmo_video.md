# 🧠 Algoritmo de Procesamiento: Video Faces Counter

Este documento detalla la lógica secuencial y matemática detrás de la aplicación **Video Faces Counter**, diseñada para procesar archivos de video pre-grabados (ej. MP4) y contabilizar pasajeros mediante el servicio en la nube de AWS Rekognition.

> [!NOTE]
> Este módulo opera bajo un paradigma de **Post-Procesamiento**, ideal para auditorías diferidas de cintas de seguridad donde el tiempo real no es un requerimiento estricto.

---

## ⚙️ Diagrama Lógico del Algoritmo

El algoritmo procesa el video fotograma a fotograma utilizando la librería OpenCV, aplicando filtros de limpieza antes de enviar la carga útil a la inteligencia artificial.

### 1. Muestreo de Fotogramas (Frame Sampling)
Para evitar el colapso de la API y reducir costos operativos, el algoritmo no procesa los 30 o 60 fotogramas por segundo (fps) del video original.
*   **Cálculo de Salto:** Se define una variable `frames_per_second` (ej. 1 frame por segundo). El algoritmo salta los fotogramas intermedios usando el módulo matemático (`current_frame % (frame_rate / frames_per_second) != 0`).
*   **Decodificación:** El frame seleccionado se convierte de la matriz nativa de OpenCV (BGR) a una cadena de bytes JPEG (Base64) lista para el tránsito HTTP.

### 2. Inferencia y Filtrado Geométrico
El frame en crudo se envía al endpoint de **AWS Rekognition** (`detect_faces`).
*   **Umbral de Confianza:** Se descartan las detecciones donde la red neuronal tenga una certeza inferior al 95%.
*   **Evaluación de Postura:** Llama a `is_frontal_face()` para asegurar que el rostro tenga un ángulo de Yaw/Pitch manejable, ignorando nucas o perfiles extremos.
*   **Filtro de Oclusión:** Revisa el diccionario `FaceOccluded`. Si un rostro está tapado (ej. bufanda/mano) con una confianza mayor al 90%, se descarta para evitar falsos positivos.

### 3. Motor de Deduplicación (Lógica de Collage)
Este es el núcleo de protección financiera del script. Evita contar a la misma persona si aparece en 10 fotogramas seguidos.
*   **Recorte Facial (Cropping):** Usando las coordenadas del `BoundingBox` devueltas por AWS, el script recorta exactamente el cuadro del rostro del pasajero del fotograma general.
*   **Collage de Memoria:** El sistema mantiene una carpeta virtual (Collage) donde guarda en disco (o RAM) un "expediente" visual de cada rostro válido encontrado hasta el momento.
*   **Comparación Uno-a-Muchos:** Por cada rostro nuevo en el frame actual, el algoritmo itera sobre todas las fotos del Collage y ejecuta la API `compare_faces` de AWS.
    *   **Coincidencia (Match):** Si el índice de similitud es alto, la persona ya fue contada anteriormente. Se ignora.
    *   **Rostro Inédito:** Si `len(matches) == 0`, significa que es un pasajero nuevo. Se suma `+1` al contador global y la foto del pasajero se guarda inmediatamente en el Collage para futuras comparaciones.

### 4. Reciclaje de Ciclos (Gestión de Memoria)
*   **Límite de Collage:** Para evitar que la carpeta de Collage crezca infinitamente (lo cual haría la comparación logarítmicamente más lenta y costosa), se implementa un tope dinámico por `cycles`.
*   **Limpieza:** Al finalizar el análisis del video, la bandera `delete_faces` asegura que se ejecute un `shutil.rmtree` para destruir los rostros almacenados temporalmente, cumpliendo con la privacidad por diseño.

---

## 📈 Análisis de Complejidad

*   **Ventajas:** Alta precisión gracias al uso de modelos robustos en la nube. Tolerancia a cambios drásticos de iluminación.
*   **Desventajas:** Alta dependencia de red. Costo económico directamente proporcional a la longitud del video debido a las llamadas constantes a la API `compare_faces`.
*   **Casos de Uso:** Auditorías gerenciales sobre videos extraídos manualmente del DVR del autobús tras sospechas de fraude masivo.

---

**Fuente:** Documentación Técnica de Algoritmos (2026).
