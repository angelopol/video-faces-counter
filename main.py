import cv2  
import dlib

def FaceCount(VideoPath = '', ShowFaces = False):
    cap = cv2.VideoCapture(VideoPath)  
    detector = dlib.get_frontal_face_detector() 
    face_count = 0 
    
    while True:  
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
        faces = detector(gray)  
          
        for face in faces:  
            face_count += 1

            if ShowFaces:
                x, y = face.left(), face.top()  
                x1, y1 = face.right(), face.bottom()  
                cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)  
                cv2.putText(frame, f'Face {face_count}', (x-10, y-10),  
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        if ShowFaces:
            cv2.imshow('Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break  
    
    cap.release()  
    cv2.destroyAllWindows()

    return face_count

if __name__ == "__main__":
    # Call the function with the path to your video file
    print(FaceCount('repository/855565-hd_1920_1080_24fps.mp4', True))