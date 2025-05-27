if 'sys' not in dir(): import sys; sys.path.append("rekognition")
from image import RekognitionImage

import boto3
import cv2

# Leer la imagen desde la carpeta local
image_path = "repository/images/test.jpg"
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()

# Crear el cliente de Rekognition
rekognition_client = boto3.client("rekognition")

# Crear la instancia de RekognitionImage
image = {"Bytes": image_bytes}
image_name = "test.jpg"

rekognition_image = RekognitionImage(image, image_name, rekognition_client)
faces = rekognition_image.detect_faces()

# --- DIBUJAR RECTÁNGULOS EN LAS CARAS ---
# Leer la imagen con OpenCV
img = cv2.imread(image_path)
height, width, _ = img.shape

for face in faces:
    cv2.rectangle(img, *RekognitionImage.get_cv2_dimensions(face['BoundingBox'], width, height))

# Guardar la imagen resultante
while True:
    cv2.imshow("output.jpg", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break