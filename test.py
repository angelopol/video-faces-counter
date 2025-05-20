import json
from main import FaceCount

with open('repository/repository.json', 'r') as file:
    data = json.load(file)

accuracies = []
for item in data['videos']:
    print("Processing video:", item['title'])
    num_faces = FaceCount(item['file'])
    print("Number of faces detected:", num_faces)
    accuracy = (num_faces*100)/item['faces']
    accuracies.append(accuracy)
    print("Acuracy:", accuracy, "%")
    print("--------------------------------------------------")

print("Average accuracy:", sum(accuracies)/len(accuracies), "%")