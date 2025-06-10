import customtkinter as ctk
from Ui import TaskManager

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Timer")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.taskManager = TaskManager(self)
        self.taskManager.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
