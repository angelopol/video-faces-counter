# Video Faces Counter

Librería Python para contar rostros únicos en un video usando AWS Rekognition.

## Algoritmo

1. Reduce los frames del video a 3 fps
2. Detecta rostros en cada frame
3. Almacena los rostros localmente en un collage
4. Compara rostros detectados con los almacenados
   - Si el rostro no ha sido almacenado, se guarda
   - Si hay más de 100 rostros, se crea un nuevo collage
5. El total de rostros almacenados = total de rostros únicos en el video
6. Al finalizar, se elimina la carpeta de almacenamiento

## Instalación

```bash
git clone https://github.com/angelopol/video-faces-counter.git
cd video-faces-counter
pip install -e .
```

## Configuración de AWS

### Opción 1: Archivo .env (recomendado)

```bash
cp .env.example .env
```

Editar `.env`:
```
AWS_ACCESS_KEY_ID=tu_access_key_aqui
AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui
AWS_REGION=us-east-1
```

### Opción 2: Parámetros directos

```python
from VideoFacesCounter import get_rekognition_client, FaceCount

# Cliente con credenciales explícitas
client = get_rekognition_client(
    aws_access_key_id="AKIA...",
    aws_secret_access_key="...",
    region="us-east-1"
)

# Usar el cliente personalizado
FaceCount("video.mp4", rekognition_client=client)
```

### Opción 3: AWS CLI

```bash
aws configure
```

## Uso

```python
from VideoFacesCounter import FaceCount

# Contar rostros en un video
total_faces = FaceCount("video.mp4")
print(f"Total de rostros únicos: {total_faces}")

# Con visualización de rostros detectados
FaceCount("video.mp4", ShowFaces=True)

# Mostrar solo rostros nuevos
FaceCount("video.mp4", ShowNewFaces=True)

# Mantener los rostros después del análisis
FaceCount("video.mp4", delete_faces=False)
```

## Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `VideoPath` | str | '' | Ruta al archivo de video |
| `ShowFaces` | bool | False | Mostrar rostros detectados |
| `delete_faces` | bool | True | Eliminar almacenamiento al finalizar |
| `ShowNewFaces` | bool | False | Mostrar solo rostros nuevos |
| `rekognition_client` | boto3.client | None | Cliente Rekognition personalizado |

## Licencia

MIT License