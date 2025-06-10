import customtkinter as ctk
from Task import Task
from Timer import Timer
from Storage import SaveTasks, LoadTasks

class TaskManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack_propagate(False)
        self.taskList = []
        savedTasks = LoadTasks()
        for task in savedTasks:
            self.AddTaskCard(task.name, preloadTask=task)
        inputFrame = ctk.CTkFrame(self)
        inputFrame.pack(fill="x", padx=20, pady=(20, 10))

        self.taskNameEntry = ctk.CTkEntry(inputFrame, placeholder_text="Enter Task Name...")
        self.taskNameEntry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.addTaskButton = ctk.CTkButton(inputFrame, text="Add Task", command=self.OnAddTask)
        self.addTaskButton.pack(side="left")

        self.taskListFrame = ctk.CTkScrollableFrame(self)
        self.taskListFrame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def OnAddTask(self):
        taskName = self.taskNameEntry.get().strip()
        if not taskName:
            return
        self.AddTaskCard(taskName)
        self.taskNameEntry.delete(0, "end")

 
    def AddTaskCard(self, taskName, preloadTask=None):
        cardFrame = ctk.CTkFrame(self.taskListFrame, corner_radius=10)
        cardFrame.pack(fill="x", pady=8, padx=10)

        task = Task(taskName)
        timerLabel = ctk.CTkLabel(cardFrame, text="00:00:00", font=ctk.CTkFont(size=14))
        timerLabel.pack(side="left", padx=10)

        task = preloadTask if preloadTask else Task(taskName)
        cardFrame.linkedTask = task
        self.taskList.append(task)

        def UpdateTimerLabel(seconds):
            hrs, rem = divmod(seconds, 3600)
            mins, secs = divmod(rem, 60)
            timerLabel.configure(text=f"{hrs:02}:{mins:02}:{secs:02}")
            task.elapsedSeconds = seconds

        timer = Timer(self, onTick=UpdateTimerLabel)

        def StartDrag(event):
            cardFrame.startY = event.y_root
            cardFrame.lift()
            SaveTasks()

        def OnDrag(event):
            dy = event.y_root - cardFrame.startY
            cardFrame.place_configure(y=cardFrame.winfo_y() + dy)
            cardFrame.startY = event.y_root

        def EndDrag(event):
            cardFrame.place_forget()
            cardFrame.pack(fill="x", pady=8, padx=10)

            widgets = self.taskListFrame.winfo_children()
            sortedWidgets = sorted(widgets, key=lambda w: w.winfo_y())

            for widget in sortedWidgets:
                widget.pack_forget()
            for widget in sortedWidgets:
                widget.pack(fill="x", pady=8, padx=10)

            newTaskList = []
            for widget in sortedWidgets:
                task = getattr(widget, "linkedTask", None)
                if task:
                    newTaskList.append(task)
            self.taskList = newTaskList
            SaveTasks()

        cardFrame.bind("<ButtonPress-1>", StartDrag)
        cardFrame.bind("<B1-Motion>", OnDrag)
        cardFrame.bind("<ButtonRelease-1>", EndDrag)
        cardFrame.linkedTask = task 
        nameLabel = ctk.CTkLabel(cardFrame, text=task.name, font=ctk.CTkFont(size=15, weight="bold"))
        nameLabel.pack(side="left", padx=15)

        controlsFrame = ctk.CTkFrame(cardFrame, fg_color="transparent")
        controlsFrame.pack(side="right", padx=10)

        nameVar = ctk.StringVar(value=task.name)
        nameLabel = ctk.CTkLabel(cardFrame, textvariable=nameVar, font=ctk.CTkFont(size=15, weight="bold"))
        nameLabel.pack(side="left", padx=15)

        def Start(): 
            timer.Start()
            task.Start()
            SaveTasks()

        def Pause(): 
            timer.Pause()
            task.Pause()
            SaveTasks()

        def Reset():
            timer.Reset()
            task.Reset()
            UpdateTimerLabel(0)
            SaveTasks()

        def Delete():
            timer.Pause()
            cardFrame.destroy()
            self.taskList.remove(task)
            SaveTasks()

        def Edit():
            nameLabel.pack_forget()
            editEntry = ctk.CTkEntry(cardFrame)
            editEntry.insert(0, task.name)
            editEntry.pack(side="left", padx=15)
            editEntry.focus()

            def SaveEdit(event=None):
                newName = editEntry.get().strip()
                if newName:
                    task.name = newName
                    nameVar.set(newName)
                editEntry.destroy()
                nameLabel.pack(side="left", padx=15)
                SaveTasks()

            editEntry.bind("<Return>", SaveEdit)
            editEntry.bind("<FocusOut>", SaveEdit)

        startButton = ctk.CTkButton(controlsFrame, text="Start", width=60, command=Start)
        pauseButton = ctk.CTkButton(controlsFrame, text="Pause", width=60, command=Pause)
        resetButton = ctk.CTkButton(controlsFrame, text="Reset", width=60, command=Reset)
        editButton = ctk.CTkButton(controlsFrame, text="Edit", width=60, command=Edit) 
        deleteButton = ctk.CTkButton(controlsFrame, text="Delete", width=60, command=Delete)

        for btn in [startButton, pauseButton, resetButton, editButton, deleteButton]:
            btn.pack(side="left", padx=5)

        self.taskList.append(task)
