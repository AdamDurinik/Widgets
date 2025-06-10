import json
from Task import Task
from datetime import datetime

FILE_PATH = "tasks.json"

def SaveTasks(taskList):
    try:
        data = []
        for task in taskList:
            data.append({
                "name": task.name,
                "elapsedSeconds": task.elapsedSeconds,
                "createdAt": task.createdAt.isoformat(),
                "updatedAt": task.updatedAt.isoformat(),
            })
        with open(FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Error saving tasks:", e)

def LoadTasks():
    tasks = []
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
            for item in data:
                task = Task(item["name"])
                task.elapsedSeconds = item.get("elapsedSeconds", 0)
                task.createdAt = datetime.fromisoformat(item["createdAt"])
                task.updatedAt = datetime.fromisoformat(item["updatedAt"])
                tasks.append(task)
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Error loading tasks:", e)
    return tasks
