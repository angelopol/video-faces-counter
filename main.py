import cv2
# Load the cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def FaceCount(VideoPath = '', ShowFaces = False):
    # Open a video capture
    cap = cv2.VideoCapture(VideoPath)
    num_faces = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Get the number of faces found
        num_faces = len(faces)

        # Display the frame with faces
        if ShowFaces:
            # Draw rectangles around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Face", frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Print the number of faces found
    return num_faces

if __name__ == "__main__":
    # Call the function with the path to your video file
    print(FaceCount('repository/855565-hd_1920_1080_24fps.mp4'))