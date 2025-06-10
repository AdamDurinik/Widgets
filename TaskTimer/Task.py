from datetime import datetime

class Task:
    def __init__(self, name: str):
        self.name = name
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

        self.targetDuration = None  
        self.elapsedSeconds = 0     

        self.isRunning = False
        self.isPaused = False

    def Start(self):
        self.isRunning = True
        self.isPaused = False
        self.updatedAt = datetime.now()

    def Pause(self):
        self.isPaused = True
        self.isRunning = False
        self.updatedAt = datetime.now()

    def Reset(self):
        self.elapsedSeconds = 0
        self.isRunning = False
        self.isPaused = False
        self.updatedAt = datetime.now()

    def UpdateElapsed(self, seconds):
        self.elapsedSeconds += seconds
        self.updatedAt = datetime.now()

    def SetTargetDuration(self, minutes: int):
        self.targetDuration = minutes * 60
