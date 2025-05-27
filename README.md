Algorithm:

- Reduce the video frames to 3 fps.
- Detect faces in a frame.
- Store the faces locally.
- Detect faces in the next frame.
- Compare the faces detected in the new frame with the stored faces.
    - If the face has not been stored, meaning it does not resemble any of the already stored faces, then it should be stored.
    - If the detected face matches more than one of the stored faces, then the stored faces should be deleted and the detected face should be saved.
- The total number of stored faces will be equal to the total number of faces detected in the video.
- After analyzing the entire video, all stored faces should be deleted by removing the storage folder.

Testing functionalities:

- Display the detected faces while the video is playing.
- Display only the new faces detected while the video is playing.
- Store the recognition results in a JSON file with the following attributes:
    - Input video (video).
    - File (file).
    - Faces detected by a person (FacesPerson).
    - Faces detected using the video faces counter (FacesCounter).
    - Recognition average (average).