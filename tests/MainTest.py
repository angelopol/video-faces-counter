if 'sys' not in dir(): import sys; sys.path.append("./")
import json
from main import FaceCount

def facecount_accuracy(num_faces_detected, num_faces_real):
    if num_faces_real == 0:
        return 0.0
    precision = 100 * (1 - abs(num_faces_detected - num_faces_real) / num_faces_real)
    return max(0.0, precision)

with open('repository/repository.json', 'r') as file:
    data = json.load(file)

accuracies = []
for item in data['videos']:
    print("Processing video:", item['title'])
    num_faces = FaceCount(item['file'], True)
    print("Number of faces detected:", num_faces)
    accuracy = facecount_accuracy(num_faces, item['faces'])
    accuracies.append(accuracy)
    print("Acuracy:", accuracy, "%")
    print("--------------------------------------------------")

print("Average accuracy:", sum(accuracies)/len(accuracies), "%")