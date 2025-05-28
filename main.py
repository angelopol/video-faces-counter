if 'sys' not in dir(): import sys; sys.path.append("rekognition")
import cv2
from image import RekognitionImage
import boto3
import math
import os
import shutil

rekognition_client = boto3.client("rekognition")

def FaceCount(VideoPath = '', ShowFaces = False, delete_faces = True):
    shutil.rmtree("repository/data", ignore_errors=True)
    cap = cv2.VideoCapture(VideoPath)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    collage_path = "repository/data/collage"
    current_frame = 0
    num_faces = 0
    cycles = 1
    face_confidence_threshold = 95
    face_occluded_threshold = 90
    frames_per_second = 1
    if frames_per_second > frame_rate or frames_per_second == -1:
        frames_per_second = frame_rate

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        current_frame += 1
        if current_frame % (math.floor(frame_rate/frames_per_second)) != 0:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        image_bytes = buffer.tobytes()
        image = {"Bytes": image_bytes}
        image_name = "test.jpg"

        rekognition_image = RekognitionImage(image, image_name, rekognition_client)
        faces = rekognition_image.detect_faces()
        
        n = 0
        for face in faces:
            if face['Confidence'] < face_confidence_threshold or not RekognitionImage.is_frontal_face(face) or (face['FaceOccluded']['Value'] and face['FaceOccluded']['Confidence'] > face_occluded_threshold):
                continue
            n += 1
            height, width, _ = frame.shape
            left, top, right, bottom = RekognitionImage.get_cv2_dimensions(face['BoundingBox'], width, height)
            img_frame = frame[top:bottom, left:right]
            if img_frame.size == 0:
                continue
            if os.path.exists(collage_path+"1.jpg"):
                for i in range(cycles):
                    with open(collage_path+str(i+1)+".jpg", "rb") as image_file:
                        target_bytes = image_file.read()
                    _, face_buffer = cv2.imencode('.jpg', img_frame)
                    try:
                        matches, _ = rekognition_image.compare_faces({"Bytes": face_buffer.tobytes()}, {"Bytes": target_bytes})
                        if len(matches) == 0:
                            RekognitionImage.save_face(img_frame, collage_path+str(i+1)+".jpg")
                            num_faces += 1
                    except Exception as e:
                        pass
            else:
                RekognitionImage.save_face(img_frame)
                num_faces += 1
            if ShowFaces:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        if num_faces/cycles == 100:
            cycles += 1
        if ShowFaces:
            cv2.imshow("Face", frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    if delete_faces:
        shutil.rmtree("repository/data", ignore_errors=True)
    # Print the number of faces found
    return num_faces

if __name__ == "__main__":
    # Call the function with the path to your video file
    print(FaceCount('repository/videos/855565-hd_1920_1080_24fps.mp4', True, False))