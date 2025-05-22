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
        
    def compare_faces(self, target_image):
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
                SourceImage=self.image,
                TargetImage=target_image.image
            )
            matches = [
                match["Face"] for match in response["FaceMatches"]
            ]
            unmatches = [face for face in response["UnmatchedFaces"]]
        except Exception as e:
            raise Exception(
                f"Error comparing faces in image {self.image_name} to {target_image.image_name}: {e}"
            )
        else:
            return matches, unmatches
        
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