import cv2
# Load the cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open a video capture
cap = cv2.VideoCapture('/content/video.mp4')  # Replace 'your_video.mp4' with the path to your video file

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Get the number of faces found
    num_faces = len(faces)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with faces
    cv2.imshow(frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Print the number of faces found
print("Number of faces detected: " + str(num_faces))

print("Number of faces detected: " + str(num_faces))