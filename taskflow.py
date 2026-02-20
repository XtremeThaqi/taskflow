import tkinter as tk
from tkinter import messagebox, ttk

class TaskFlow:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow")
        self.root.geometry("580x660")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        self.pending_tasks = []
        self.completed_tasks = []

        self._setup_theme()
        self._create_ui()

        self.root.bind("<Return>", lambda e: self.add_task())

    def _setup_theme(self):
        # Dark professional palette - restrained & high-contrast
        self.colors = {
            "bg":           "#0d1117",      # very dark background
            "surface":      "#161b22",      # cards / panels
            "surface_alt":  "#1f2937",      # subtle variation
            "text":         "#e6edf3",      # main text
            "text_mute":    "#8b949e",      # secondary / completed
            "border":       "#30363d",      # subtle lines
            "accent":       "#58a6ff",      # blue links / primary action
            "accent_hover": "#388bfd",      # hover state
            "danger":       "#f85149",      # delete
            "success":      "#3fb950",      # complete (used subtly)
            "selection":    "#1f6feb",      # selected item bg
        }

        style = ttk.Style()
        style.theme_use("clam")

        # Button styling
        style.configure("TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=10,
                        background=self.colors["accent"],
                        foreground="white")
        style.map("TButton",
                  background=[("active", self.colors["accent_hover"]),
                              ("!disabled", self.colors["accent"])],
                  foreground=[("active", "white"), ("!disabled", "white")])

        # Accent button for Mark Complete
        style.configure("Success.TButton",
                        background=self.colors["success"],
                        foreground="white")
        style.map("Success.TButton",
                  background=[("active", "#2ea043")])

        # Delete button
        style.configure("Danger.TButton",
                        background=self.colors["danger"],
                        foreground="white")
        style.map("Danger.TButton",
                  background=[("active", "#d32f2f")])

    def _create_ui(self):
        c = self.colors

        main = ttk.Frame(self.root, padding="28 32 28 24", style="TFrame")
        main.pack(fill="both", expand=True)
        main.configure(style="TFrame")  # ensure bg
        ttk.Style().configure("TFrame", background=c["bg"])

        # Header
        header = tk.Label(main,
                          text="TaskFlow",
                          font=("Segoe UI", 24, "bold"),
                          bg=c["bg"],
                          fg=c["text"])
        header.pack(anchor="w", pady=(0, 32))

        # Input row
        input_row = tk.Frame(main, bg=c["bg"])
        input_row.pack(fill="x", pady=(0, 24))

        self.entry = tk.Entry(input_row,
                              font=("Segoe UI", 13),
                              bg=c["surface"],
                              fg=c["text"],
                              insertbackground=c["accent"],
                              relief="flat",
                              highlightthickness=1,
                              highlightbackground=c["border"],
                              highlightcolor=c["accent"],
                              bd=0)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 16))

        add_btn = ttk.Button(input_row,
                             text="Add Task",
                             command=self.add_task)
        add_btn.pack(side="right")

        # List container
        list_frame = tk.Frame(main, bg=c["bg"])
        list_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(list_frame,
                                  font=("Segoe UI", 12),
                                  bg=c["surface"],
                                  fg=c["text"],
                                  selectbackground=c["selection"],
                                  selectforeground="white",
                                  activestyle="none",
                                  bd=0,
                                  highlightthickness=0,
                                  yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.listbox.yview)

        # Bottom buttons
        btn_row = tk.Frame(main, bg=c["bg"])
        btn_row.pack(fill="x", pady=(24, 0))

        delete_btn = ttk.Button(btn_row,
                                text="Delete",
                                command=self.delete_task,
                                style="Danger.TButton")
        delete_btn.pack(side="left", padx=(0, 16))

        complete_btn = ttk.Button(btn_row,
                                  text="Mark Complete",
                                  command=self.mark_as_done,
                                  style="Success.TButton")
        complete_btn.pack(side="left")

        self._refresh_listbox()

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Input required", "Please type a task first.")
            return

        self.pending_tasks.append(text)
        self._refresh_listbox()
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("No selection", "Select a task first.")
            return

        idx = sel[0]
        offset = 1 if self.pending_tasks and self.completed_tasks else 0

        if idx < len(self.pending_tasks):
            del self.pending_tasks[idx]
        else:
            real_idx = idx - len(self.pending_tasks) - offset
            if 0 <= real_idx < len(self.completed_tasks):
                del self.completed_tasks[real_idx]

        self._refresh_listbox()

    def mark_as_done(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("No selection", "Select a task first.")
            return

        idx = sel[0]
        offset = 1 if self.pending_tasks and self.completed_tasks else 0

        if idx >= len(self.pending_tasks) + offset:
            messagebox.showinfo("Already done", "Task is already completed.")
            return

        if idx < len(self.pending_tasks):
            task = self.pending_tasks.pop(idx)
            self.completed_tasks.append(task)
            self._refresh_listbox()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        c = self.colors

        for task in self.pending_tasks:
            self.listbox.insert(tk.END, f"  •  {task}")

        if self.pending_tasks and self.completed_tasks:
            sep_idx = self.listbox.size()
            self.listbox.insert(tk.END, "  ─────────────  Completed  ─────────────")
            self.listbox.itemconfig(sep_idx, fg=c["text_mute"])

        for task in self.completed_tasks:
            idx = self.listbox.size()
            self.listbox.insert(tk.END, f"  ✓  {task}")
            self.listbox.itemconfig(idx, fg=c["text_mute"])

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskFlow(root)
    root.mainloop()