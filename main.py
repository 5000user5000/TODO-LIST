import tkinter as tk

class ToDoList:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")

        # 創建任務列表
        self.tasks = []

        # 創建任務列表框架
        self.task_frame = tk.Frame(master)
        self.task_frame.pack(side=tk.TOP)

        # 創建滾動條框架
        self.scroll_frame = tk.Frame(master)
        self.scroll_frame.pack(side=tk.BOTTOM)

        # 創建滾動條
        self.scrollbar = tk.Scrollbar(self.scroll_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 創建任務列表
        self.task_list = tk.Listbox(self.task_frame, yscrollcommand=self.scrollbar.set)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.task_list.yview)

        # 創建添加任務按鈕
        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.TOP)

    def add_task(self):
        # 創建添加任務窗口
        self.add_window = tk.Toplevel(self.master)

        # 創建添加任務標題
        self.add_title = tk.Label(self.add_window, text="Add Task")
        self.add_title.pack(side=tk.TOP)

        # 創建任務輸入框
        self.task_entry = tk.Entry(self.add_window)
        self.task_entry.pack(side=tk.TOP)

        # 創建添加任務按鈕
        self.add_button = tk.Button(self.add_window, text="Add", command=self.save_task)
        self.add_button.pack(side=tk.TOP)

    def save_task(self):
        # 將新任務添加到任務列表中
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_list.insert(tk.END, task)
            self.add_window.destroy()

root = tk.Tk()
todo = ToDoList(root)
root.mainloop()
