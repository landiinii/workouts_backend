import json

with open("excersizes.json", "r") as file:
    exercises = json.load(file)

print(len(exercises.keys()))
