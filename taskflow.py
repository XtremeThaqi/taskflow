import tkinter as tk
from tkinter import messagebox, ttk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow")
        self.root.geometry("540x620")
        self.root.configure(bg="#f5f7fa")
        self.root.resizable(False, False)

        self.pending_tasks = []
        self.completed_tasks = []

        self._setup_style()
        self._create_widgets()
        self.root.bind("<Return>", lambda event: self.add_task())

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        font=("Helvetica", 12, "bold"),
                        padding=10)
        style.map("TButton",
                  background=[("active", "#3b82f6"), ("!disabled", "#2563eb")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.configure("Accent.TButton",
                        background="#10b981",
                        foreground="white")
        style.map("Accent.TButton",
                  background=[("active", "#059669")])

        style.configure("TFrame", background="#f5f7fa")

    def _create_widgets(self):
        main_container = ttk.Frame(self.root, padding="20 25 20 15")
        main_container.pack(fill="both", expand=True)

        header = tk.Label(main_container,
                          text="TaskFlow",
                          font=("Helvetica", 24, "bold"),
                          bg="#f5f7fa",
                          fg="#1e293b")
        header.pack(pady=(0, 25))

        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill="x", pady=(0, 20))

        self.task_entry = tk.Entry(input_frame,
                                   font=("Helvetica", 14),
                                   relief="flat",
                                   bg="white",
                                   insertbackground="#2563eb",
                                   highlightthickness=2,
                                   highlightcolor="#bfdbfe",
                                   highlightbackground="#bfdbfe")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))

        add_button = ttk.Button(input_frame,
                                text="Add Task",
                                command=self.add_task,
                                style="TButton",
                                width=12)
        add_button.pack(side="right")

        list_container = ttk.Frame(main_container)
        list_container.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")

        self.task_listbox = tk.Listbox(list_container,
                                       font=("Helvetica", 13),
                                       selectbackground="#dbeafe",
                                       selectforeground="#1e40af",
                                       activestyle="none",
                                       bd=0,
                                       highlightthickness=0,
                                       bg="white",
                                       fg="#1e293b",
                                       yscrollcommand=scrollbar.set)
        self.task_listbox.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.task_listbox.yview)

        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill="x", pady=(20, 10))

        delete_button = ttk.Button(button_frame,
                                   text="Delete",
                                   command=self.delete_task,
                                   style="TButton")
        delete_button.pack(side="left", padx=(0, 12))

        done_button = ttk.Button(button_frame,
                                 text="Mark Complete",
                                 command=self.mark_as_done,
                                 style="Accent.TButton")
        done_button.pack(side="left")

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Input Required", "Please enter a task.")
            return

        self.pending_tasks.append(task_text)
        self._refresh_listbox()

        self.task_entry.delete(0, tk.END)
        self.task_entry.focus()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a task first.")
            return

        index = selection[0]

        if index < len(self.pending_tasks):
            del self.pending_tasks[index]
        else:
            real_index = index - len(self.pending_tasks) - (1 if self.pending_tasks and self.completed_tasks else 0)
            del self.completed_tasks[real_index]

        self._refresh_listbox()

    def mark_as_done(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a task first.")
            return

        index = selection[0]

        if index >= len(self.pending_tasks) + (1 if self.pending_tasks and self.completed_tasks else 0):
            messagebox.showinfo("Already Completed", "This task is already marked as done.")
            return

        if index < len(self.pending_tasks):
            task = self.pending_tasks.pop(index)
            self.completed_tasks.append(task)
            self._refresh_listbox()

    def _refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)

        for task in self.pending_tasks:
            self.task_listbox.insert(tk.END, f"  •  {task}")

        if self.pending_tasks and self.completed_tasks:
            self.task_listbox.insert(tk.END, "  ───────────────  Completed  ───────────────")

        for task in self.completed_tasks:
            idx = self.task_listbox.size()
            self.task_listbox.insert(tk.END, f"  ✓  {task}")
            self.task_listbox.itemconfig(idx, fg="#6b7280")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()