# Flujo Funcional: Video Faces Counter

El paquete `video-faces-counter` está diseñado para automatizar el conteo de pasajeros (o personas) extrayendo métricas de un archivo de video. Internamente, orquesta OpenCV para la manipulación de frames de video y el servicio AWS Rekognition para la detección de características biométricas (rostros). 

A continuación, se detalla el ciclo de vida y flujo funcional del aplicativo cuando un usuario ejecuta el método principal `FaceCount()`.

---

## 1. Inicialización y Limpieza
El usuario invoca la función principal pasándole la ruta del video (ej. `video.mp4`).
* **Parámetros del usuario:** Puede configurar opciones visuales como mostrar en vivo qué ve el algoritmo (`ShowFaces`), remarcar exclusivamente los rostros nuevos recién encontrados (`ShowNewFaces`), y si deben eliminarse los rostros temporales de la memoria caché al finalizar (`delete_faces`).
* **Directorio de caché:** El algoritmo purga preventivamente el directorio `repository/data` para asegurarse de que no haya rostros "fantasmas" almacenados de ejecuciones o corridas anteriores.
* **Captura:** El video se carga a través de OpenCV y se computa automáticamente su tasa nativa de cuadros por segundo (FPS).

## 2. Lectura y Muestreo del Video (Sampling)
En lugar de analizar todos los cuadros producidos por la cámara (lo que sería costoso y redundante), el algoritmo realiza un muestreo de **1 frame por segundo**.
* El bucle lee las tramas del video, descartando y saltando matemáticamente todos aquellos cuadros que no coincidan de forma precisa con el intervalo del segundo exacto.
* Al recuperar el frame objetivo, el mismo es codificado comprimido en formato `.jpg` en memoria RAM para asegurar un tamaño de byte transportable hacia la API en la nube.

## 3. Detección Inteligente de Rostros (AWS Rekognition)
Se envía el cuadro muestreado a AWS Rekognition usando el método `detect_faces()`.
AWS devuelve de manera genérica todos los objetos que aparentan ser caras en la imagen. No obstante, para garantizar calidad y certeza en el conteo, el sistema local implementa **Tres Filtros Estrictos de Calidad**:
1. **Umbral de Confianza:** Destruye o ignora las caras que devuelvan una certeza de viabilidad (Confidence) menor al 95%.
2. **Postura Frontal:** Se descartan perfiles y cabezas agachadas o de espalda. Exclusivamente se admiten rostros en posición anatómica frontal.
3. **Oclusión (Tapabocas / Sombreros):** Si AWS detecta que el rostro está fuertemente ocluido (con una confianza superior al 90%), se procede a descartarlo automáticamente puesto a que sería difícil comparar su identidad a futuro.

## 4. Prevención de Duplicados (Comparación Biométrica)
Si una cara recién analizada superó los tres filtros estrictos del paso anterior, el escáner se dispone a averiguar si **ya fue contada antes** en algún segundo previo del video. 
* El sistema recorta un cuadrado perfecto con la cara de la persona.
* El algoritmo toma este rostro y recurre a la base de datos temporal (llamada "Collage") alojada en el caché.
* Emplea el método `compare_faces()` de AWS cotejando a este pasajero contra todos los rostros del mosaico.
    * **SI HAY COINCIDENCIA:** Significa que el usuario sigue de pie estático frente a la cámara. Su conteo se **descarta** ya que fue registrado con antelación.
    * **SI NO HAY COINCIDENCIA:** El algoritmo concluye que se trata de un nuevo usuario/pasajero ingresando. En ese instante, el número del conteo general suma `+1`, se le dibuja un cuadro verde si se pre-configuró UI, y por último el recorte de su cara es almacenada a lo interno de un `collage.jpg`.

## 5. Paginación de Collages (Gestor de Limites de AWS)
Dado que Amazon Web Services (Rekognition) posee una estricta directriz máxima de comparación sobre **"100 rostros por imagen"**, el script del flujo funcional posee un calculador condicional:
* Cada vez que se cuentan 100 personas de forma única, el multiplicador (`cycles`) aumenta; permitiendo así que el rostro número 101 se guarde de forma inteligente en un nuevo bloque (`collage_path+2.jpg`) y no devuelva errores HTTP de desbordamiento por requerimiento de la API.

## 6. Salida de Resultados y Finalización
El ciclo recursivo de muestreo se mantiene latente analizando los cuadros y creando el caché a través de todo lo que dure el metraje del video a menos que el usuario presione la tecla <kbd>Q</kbd> en el teclado, lo que fuerza un truncamiento del proceso.

Una vez agotado el video:
* La lectura en memoria de OpenCV es apagada y las ventanas destruidas.
* Si el campo `delete_faces` es booleano `True` (opción predeterminada), toda la caché generada (los collages de rastreo) es limpiada del disco duro protegiendo la privacidad e higiene geométrica del almacenamiento.
* **El Return:** Se retorna como dígito final el índice total de `num_faces`, concluyendo de manera oficial el funcionamiento del paquete.
