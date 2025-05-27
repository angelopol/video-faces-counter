import cv2
import os
import numpy as np

class RekognitionImage:
    """
    Encapsulates an Amazon Rekognition image. This class is a thin wrapper
    around parts of the Boto3 Amazon Rekognition API.
    """

    def __init__(self, image, image_name, rekognition_client):
        """
        Initializes the image object.

        :param image: Data that defines the image, either the image bytes or
                      an Amazon S3 bucket and object key.
        :param image_name: The name of the image.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client

    def detect_faces(self):
        """
        Detects faces in the image.

        :return: The list of faces found in the image.
        """
        try:
            response = self.rekognition_client.detect_faces(
                Image=self.image, Attributes=["DEFAULT"]
            )
            faces = [face for face in response["FaceDetails"]]
        except Exception as e:
            raise Exception(
                f"Error detecting faces in image {self.image_name}: {e}"
            )
        else:
            return faces
        
    def compare_faces(self, source_image, target_image):
        """
        Compares faces in the image with the largest face in the target image.

        :param target_image: The target image to compare against.
        :param similarity: Faces in the image must have a similarity value greater
                           than this value to be included in the results.
        :return: A tuple. The first element is the list of faces that match the
                 reference image. The second element is the list of faces that have
                 a similarity value below the specified threshold.
        """
        try:
            response = self.rekognition_client.compare_faces(
                SourceImage=source_image,
                TargetImage=target_image,
                SimilarityThreshold=90.0,
                QualityFilter="AUTO"
            )
            matches = [
                match["Face"] for match in response["FaceMatches"]
            ]
            unmatches = [face for face in response["UnmatchedFaces"]]
        except Exception as e:
            raise Exception(
                f"Error comparing faces: {e}"
            )
        else:
            return matches, unmatches
        
    @staticmethod

    def get_cv2_dimensions(box, width, height):
        left = int(box['Left'] * width)
        top = int(box['Top'] * height)
        right = int((box['Left'] + box['Width']) * width)
        bottom = int((box['Top'] + box['Height']) * height)
        
        return left, top, right, bottom
    
    def save_face(face_img, output_path="repository/data/collage.jpg"):
        if face_img.size == 0:
            return  # No guardar si el recorte está vacío

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Si el collage ya existe, cargarlo y añadir la nueva cara
        if os.path.exists(output_path):
            collage_img = cv2.imread(output_path)
            # Igualar la altura de la nueva cara al collage si es necesario
            collage_height = collage_img.shape[0]
            face_height = face_img.shape[0]
            if face_height < collage_height:
                pad = np.zeros((collage_height - face_height, face_img.shape[1], 3), dtype=np.uint8)
                face_img = np.vstack([face_img, pad])
            elif face_height > collage_height:
                pad = np.zeros((face_height - collage_height, collage_img.shape[1], 3), dtype=np.uint8)
                collage_img = np.vstack([collage_img, pad])
            # Añadir la nueva cara al final (horizontalmente)
            collage_img = np.hstack([collage_img, face_img])
        else:
            collage_img = face_img

        cv2.imwrite(output_path, collage_img)

if __name__ == "__main__":
    import boto3

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
    print(faces)