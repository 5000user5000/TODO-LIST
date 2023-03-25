import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import END
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ToDoList:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")

        # 創建任務列表
        self.tasks = []

        # 創建任務列表框架
        self.task_frame = ttk.Frame(master)
        self.task_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 創建任務列表標題
        self.task_title = ttk.Label(self.task_frame, text="Tasks", font=("Helvetica", 18, "bold"))
        self.task_title.pack(side=tk.TOP, padx=10, pady=10)

        # 創建滾動條框架
        self.scroll_frame = ttk.Frame(master)
        self.scroll_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 創建滾動條
        self.scrollbar = ttk.Scrollbar(self.scroll_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 創建任務列表
        self.task_list = tk.Listbox(self.task_frame, yscrollcommand=self.scrollbar.set, font=("Helvetica", 14), activestyle="none")
        self.task_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.task_list.yview)

        # 創建子任務框架
        self.show_subtasks = self.show_subtasks

        # 創建添加任務按鈕
        self.add_button = ttk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 創建圖表框架
        self.chart_frame = ttk.Frame(master)
        self.chart_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # 創建圖表標題
        self.chart_title = ttk.Label(self.chart_frame, text="Task Progress Chart", font=("Helvetica", 18, "bold"))
        self.chart_title.pack(side=tk.TOP, padx=10, pady=10)

        # 創建圖表
        self.fig = plt.figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Task Progress")
        self.ax.set_xlabel("Task")
        self.ax.set_ylabel("Progress (%)")
        self.chart_canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
        self.chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 創建關閉按鈕
        self.close_button = tk.Button(self.master, text="Close", command=self.master.destroy)
        self.close_button.pack(padx=10, pady=10)

        # 更新圖表
        self.update_chart()

        # 選中任務時顯示子任務和完成時間
        #self.task_list.bind("<<ListboxSelect>>", self.show_subtasks)

    def update_list(self):
        # Clear the current list box #每次更新前先清空列表框，目的是避免重複顯示任務
        self.task_list.delete(0, END)
        
        count = 0
        # Insert the tasks
        for task in self.tasks:
            count += 1
            print(f"第{count}次")
            print("======= Task added update_list() ======== \n", task)
            self.task_list.insert(END, task["name"])

    def update_chart(self):
        # Clear the current figure
        self.fig.clear()
    
        # Create a new axis and set labels
        ax = self.fig.add_subplot(111)
        ax.set_xlabel('Time')
        ax.set_ylabel('Completion %')
    
        # Set the data for the chart
        x_values = []
        y_values = []
        try:
            for task in self.tasks:
                print("======= Task added update_chart() ======== \n", task)
                df= task["due"]
                day_of_year = df.strftime('%j')
                x_values.append(day_of_year)
                # TODO:先寫成這樣，該年的第幾天，因為他必須要放數字或字串，而不是datetime。但是圖表這樣畫有何意義?
        
                y_values.append(task["completed"]) #percent_complete
    
            # Plot the data and display the chart
            ax.plot(x_values, y_values)
            self.chart_canvas.draw()
        except:
            print("No tasks to display (update_chart)")
            pass

    def add_task(self):
        # 創建添加任務窗口
        self.add_window = tk.Toplevel(self.master)

        # 創建添加任務標題
        self.add_title = ttk.Label(self.add_window, text="Add Task", font=("Helvetica", 18, "bold"))
        self.add_title.pack(side=tk.TOP, padx=10, pady=10)

        # 創建任務名稱框架
        self.name_frame = ttk.Frame(self.add_window)
        self.name_frame.pack(side=tk.TOP, padx=10, pady=10)

        # 創建任務名稱標籤和輸入框
        self.name_label = ttk.Label(self.name_frame, text="Task Name", font=("Helvetica", 14))
        self.name_label.pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(self.name_frame, font=("Helvetica", 14))
        self.name_entry.pack(side=tk.RIGHT)

        # 創建任務期限框架
        self.due_frame = ttk.Frame(self.add_window)
        self.due_frame.pack(side=tk.TOP, padx=10, pady=10)

        # 創建任務期限標籤和輸入框
        self.due_label = ttk.Label(self.due_frame, text="Due Date (YYYY MM DD)", font=("Helvetica", 14))
        self.due_label.pack(side=tk.LEFT)
        self.due_entry = ttk.Entry(self.due_frame, font=("Helvetica", 14))
        self.due_entry.pack(side=tk.RIGHT)

        # 創建添加任務按鈕
        self.add_button = ttk.Button(self.add_window, text="Add", command=self.save_task)
        self.add_button.pack(side=tk.TOP, padx=10, pady=10)

        # 將任務添加到任務列表中
        task = {
            "name": "",
            "due": "",
            "completed": 0
        }
        task["name"] = self.name_entry.get()
        task["due"] = self.due_entry.get()
        task["completed"] = 0
        self.tasks.append(task)
        print("======= Task added add_task() ======== \n %s", task)

        

    def save_task(self):
        # 檢查輸入是否為空
        if not self.name_entry.get():
            messagebox.showwarning("Warning", "Please enter a task name")
            return
        if not self.due_entry.get():
            messagebox.showwarning("Warning", "Please enter a due date")
            return

        # 解析輸入的日期
        try:
            due_date = datetime.strptime(self.due_entry.get(), "%Y %m %d")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid due date (YYYY MM DD)")
            return

        # 創建任務物件
        task = {"name": self.name_entry.get(), "due": due_date, "completed": 0 , "subtasks": []}

        # 加入任務列表
        self.tasks.append(task)

        # 關閉添加任務窗口
        self.add_window.destroy()

        # 更新任務列表和圖表
        self.update_list()
        self.update_chart()
    
    def show_subtasks(self, event=None):
        """Shows the subtasks and completion time of the selected task."""
        # get the index of the selected task
        task_index = self.task_list.curselection()[0]
    
        # get the task object from the tasks list
        task = self.tasks[task_index]
    
        # create a new window to display subtasks and completion time
        subtask_window = tk.Toplevel(self.master)
        subtask_window.title(task.name + " Subtasks")
    
        # create a frame for the subtask list
        subtask_frame = ttk.Frame(subtask_window)
        subtask_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        # create a label for the completion time
        completion_label = ttk.Label(subtask_window, text="Completion time: " + str(task.completion_time))
        completion_label.pack(side=tk.TOP, padx=10, pady=10)
    
        # create a label for the subtask list
        subtask_title = ttk.Label(subtask_frame, text="Subtasks", font=("Helvetica", 14, "bold"))
        subtask_title.pack(side=tk.TOP, padx=10, pady=10)
    
        # create a listbox for the subtasks
        subtask_list = tk.Listbox(subtask_frame, font=("Helvetica", 12), activestyle="none")
        subtask_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        # add the subtasks to the listbox
        for subtask in task.subtasks:
            subtask_list.insert(tk.END, subtask.name + " (" + str(subtask.progress) + "%)")
    
        # create a button to add subtasks
        add_subtask_button = ttk.Button(subtask_frame, text="Add Subtask", command=lambda: self.add_subtask(task))
        add_subtask_button.pack(side=tk.BOTTOM, padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    todo = ToDoList(root)
    root.mainloop()
