import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from datetime import datetime

class ProDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Dashboard")
        self.root.geometry("1100x750")
        
        self.themes = {
            'light': {
                'bg': '#f5f5f7', 'panel': '#ffffff', 'panel_alt': '#f0f0f0',
                'fg': '#1d1d1f', 'muted': '#86868b', 'accent': '#0071e3', 'danger': '#ff3b30',
                'live_bg': '#e6f2ff'
            },
            'dark': {
                'bg': '#000000', 'panel': '#1c1c1e', 'panel_alt': '#2c2c2e',
                'fg': '#f5f5f7', 'muted': '#a1a1a6', 'accent': '#0a84ff', 'danger': '#ff453a',
                'live_bg': '#003366'
            }
        }
        self.current_theme_name = 'light'
        self.theme = self.themes[self.current_theme_name]
        
        self.schedule = []
        self.tasks = []
        self.doubts = []
        self.schedule_ui = []
        
        self.load_data()
        self.setup_ui()
        self.apply_theme()
        self.update_clock()

    def default_schedule(self):
        return [
            {"time": "06:30 AM", "task": "Wake up & Fresh"},
            {"time": "07:00 AM", "task": "Morning Study (Core Java / C#)"},
            {"time": "09:30 AM", "task": "Breakfast & Ready for College"},
            {"time": "10:45 AM", "task": "College Lectures & Practicals"},
            {"time": "03:00 PM", "task": "Home, Rest, Tea/Coffee Break"},
            {"time": "04:00 PM", "task": "Shop Duty (Read Python / English Notes)"},
            {"time": "10:00 PM", "task": "Dinner & Relax"},
            {"time": "10:30 PM", "task": "Revision (React JS / Clear Doubts)"},
            {"time": "11:30 PM", "task": "Sleep (Minimum 7 hours)"}
        ]

    def load_data(self):
        if os.path.exists('study_dashboard_data.json'):
            try:
                with open('study_dashboard_data.json', 'r') as f:
                    data = json.load(f)
                    self.schedule = data.get('schedule', self.default_schedule())
                    self.tasks = data.get('tasks', [])
                    self.doubts = data.get('doubts', [])
                    self.current_theme_name = data.get('theme', 'light')
                    self.theme = self.themes[self.current_theme_name]
            except:
                self.schedule = self.default_schedule()
        else:
            self.schedule = self.default_schedule()

    def save_data(self):
        data = {
            'schedule': self.schedule,
            'tasks': self.tasks,
            'doubts': self.doubts,
            'theme': self.current_theme_name
        }
        with open('study_dashboard_data.json', 'w') as f:
            json.dump(data, f)

    def setup_ui(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.header_frame = tk.Frame(self.main_container)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.clock_frame = tk.Frame(self.header_frame)
        self.clock_frame.pack(side="left")
        
        self.time_lbl = tk.Label(self.clock_frame, text="00:00:00", font=("Arial", 36, "bold"))
        self.time_lbl.pack(anchor="w")
        
        self.date_lbl = tk.Label(self.clock_frame, text="Loading...", font=("Arial", 12))
        self.date_lbl.pack(anchor="w")
        
        self.controls_frame = tk.Frame(self.header_frame)
        self.controls_frame.pack(side="right", anchor="s")
        
        tk.Button(self.controls_frame, text="📤 Export Data", bg="#0071e3", fg="white", bd=0, padx=10, pady=5, font=("Arial", 10, "bold"), command=self.export_data).pack(side="left", padx=5)
        tk.Button(self.controls_frame, text="📥 Import Data", bg="#0071e3", fg="white", bd=0, padx=10, pady=5, font=("Arial", 10, "bold"), command=self.import_data).pack(side="left", padx=5)
        self.theme_btn = tk.Button(self.controls_frame, text="🌓 Theme", bd=0, padx=10, pady=5, font=("Arial", 10, "bold"), command=self.toggle_theme)
        self.theme_btn.pack(side="left", padx=5)
        self.reset_btn = tk.Button(self.controls_frame, text="🔄 Reset", bd=0, padx=10, pady=5, font=("Arial", 10, "bold"), command=self.reset_schedule)
        self.reset_btn.pack(side="left", padx=5)
        
        self.content_frame = tk.Frame(self.main_container)
        self.content_frame.pack(fill="both", expand=True)
        
        self.left_panel = tk.Frame(self.content_frame, bd=1, relief="solid")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(self.left_panel, text="📅 Daily Schedule (Click any time/task to edit)", font=("Arial", 14, "bold")).pack(anchor="w", padx=20, pady=15)
        self.schedule_container = tk.Frame(self.left_panel)
        self.schedule_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.right_panel = tk.Frame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.doubts_panel = tk.Frame(self.right_panel, bd=1, relief="solid")
        self.doubts_panel.pack(fill="both", expand=True, pady=(0, 10))
        
        tk.Label(self.doubts_panel, text="🤔 Doubts & Homework Tracker", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=15)
        
        d_input_frame = tk.Frame(self.doubts_panel)
        d_input_frame.pack(fill="x", padx=15)
        self.doubt_sub = ttk.Combobox(d_input_frame, values=["Core Java", "C# Prog.", "React JS", "Python", "English", "Other"], width=12, state="readonly")
        self.doubt_sub.current(3)
        self.doubt_sub.pack(side="left", padx=(0, 10))
        self.doubt_entry = tk.Entry(d_input_frame, font=("Arial", 11), bd=1, relief="solid")
        self.doubt_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.doubt_entry.bind('<Return>', lambda e: self.add_doubt())
        tk.Button(d_input_frame, text="Add", bg="#0071e3", fg="white", bd=0, font=("Arial", 10, "bold"), command=self.add_doubt).pack(side="left")
        
        self.doubts_list_frame = tk.Frame(self.doubts_panel)
        self.doubts_list_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.tasks_panel = tk.Frame(self.right_panel, bd=1, relief="solid")
        self.tasks_panel.pack(fill="both", expand=True, pady=(10, 0))
        
        tk.Label(self.tasks_panel, text="📝 Normal Assignments / Tasks", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=15)
        
        t_input_frame = tk.Frame(self.tasks_panel)
        t_input_frame.pack(fill="x", padx=15)
        self.task_entry = tk.Entry(t_input_frame, font=("Arial", 11), bd=1, relief="solid")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        tk.Button(t_input_frame, text="Add", bg="#0071e3", fg="white", bd=0, font=("Arial", 10, "bold"), command=self.add_task).pack(side="left")
        
        self.tasks_list_frame = tk.Frame(self.tasks_panel)
        self.tasks_list_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.render_schedule()
        self.render_doubts()
        self.render_tasks()

    def toggle_theme(self):
        self.current_theme_name = 'dark' if self.current_theme_name == 'light' else 'light'
        self.theme = self.themes[self.current_theme_name]
        self.save_data()
        self.apply_theme()
        self.render_schedule()
        self.render_doubts()
        self.render_tasks()
        self.check_live_task()

    def apply_theme(self):
        t = self.theme
        self.root.configure(bg=t['bg'])
        self.main_container.configure(bg=t['bg'])
        self.header_frame.configure(bg=t['bg'])
        self.clock_frame.configure(bg=t['bg'])
        self.controls_frame.configure(bg=t['bg'])
        self.content_frame.configure(bg=t['bg'])
        self.right_panel.configure(bg=t['bg'])
        
        self.time_lbl.configure(bg=t['bg'], fg=t['fg'])
        self.date_lbl.configure(bg=t['bg'], fg=t['muted'])
        
        self.theme_btn.configure(bg=t['panel'], fg=t['fg'])
        self.reset_btn.configure(bg=t['panel'], fg=t['fg'])
        
        for panel in (self.left_panel, self.doubts_panel, self.tasks_panel):
            panel.configure(bg=t['panel'], highlightbackground=t['muted'], highlightcolor=t['muted'])
            for child in panel.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=t['panel'], fg=t['fg'])
                elif isinstance(child, tk.Frame):
                    child.configure(bg=t['panel'])

    def edit_schedule(self, index, field):
        if messagebox.askyesno("Confirm", "Kya aap sach mein isko edit karna chahte ho?"):
            old_val = self.schedule[index][field]
            new_val = simpledialog.askstring("Edit", "Naya text type karein:", initialvalue=old_val)
            if new_val and new_val.strip():
                self.schedule[index][field] = new_val.strip()
                self.save_data()
                self.render_schedule()
                self.check_live_task()

    def render_schedule(self):
        for widget in self.schedule_container.winfo_children():
            widget.destroy()
            
        self.schedule_ui = []
        t = self.theme
        
        for i, item in enumerate(self.schedule):
            row = tk.Frame(self.schedule_container, bg=t['panel'], pady=10, padx=10)
            row.pack(fill="x", pady=2)
            
            top_frame = tk.Frame(row, bg=t['panel'])
            top_frame.pack(fill="x")
            
            live_lbl = tk.Label(top_frame, text="● LIVE", fg=t['danger'], bg=t['panel'], font=("Arial", 9, "bold"), width=8, anchor="w")
            live_lbl.pack(side="left")
            
            time_lbl = tk.Label(top_frame, text=item['time'], fg=t['accent'], bg=t['panel'], font=("Arial", 11, "bold"), cursor="hand2", width=10, anchor="w")
            time_lbl.pack(side="left")
            time_lbl.bind("<Button-1>", lambda e, idx=i: self.edit_schedule(idx, 'time'))
            
            task_lbl = tk.Label(top_frame, text=item['task'], fg=t['fg'], bg=t['panel'], font=("Arial", 11), cursor="hand2", anchor="w")
            task_lbl.pack(side="left", fill="x", expand=True)
            task_lbl.bind("<Button-1>", lambda e, idx=i: self.edit_schedule(idx, 'task'))
            
            dur_lbl = tk.Label(row, text="", fg=t['danger'], bg=t['panel'], font=("Arial", 9, "bold"))
            dur_lbl.pack(anchor="w", padx=(65, 0))
            
            self.schedule_ui.append({
                'row': row, 'top': top_frame, 'live': live_lbl, 
                'time': time_lbl, 'task': task_lbl, 'dur': dur_lbl
            })

    def parse_time_to_minutes(self, t_str):
        try:
            dt = datetime.strptime(t_str.strip(), "%I:%M %p")
            return dt.hour * 60 + dt.minute
        except:
            return -1

    def check_live_task(self):
        now = datetime.now()
        current_mins = now.hour * 60 + now.minute
        parsed_times = [self.parse_time_to_minutes(s['time']) for s in self.schedule]
        
        active_index = -1
        
        for i in range(len(parsed_times)):
            if parsed_times[i] == -1: continue
            next_index = (i + 1) % len(parsed_times)
            start_time = parsed_times[i]
            end_time = parsed_times[next_index]
            
            if end_time <= start_time:
                if current_mins >= start_time or current_mins < end_time:
                    active_index = i
            else:
                if current_mins >= start_time and current_mins < end_time:
                    active_index = i

        t = self.theme
        for i, ui in enumerate(self.schedule_ui):
            if i == active_index:
                ui['row'].configure(bg=t['live_bg'])
                ui['top'].configure(bg=t['live_bg'])
                ui['live'].configure(bg=t['live_bg'], fg=t['danger'])
                ui['time'].configure(bg=t['live_bg'])
                ui['task'].configure(bg=t['live_bg'])
                ui['dur'].configure(bg=t['live_bg'])
                
                next_index = (i + 1) % len(self.schedule)
                ui['dur'].configure(text=f"⏳ Shuru: {self.schedule[i]['time']} | Khatam: {self.schedule[next_index]['time']}")
            else:
                ui['row'].configure(bg=t['panel'])
                ui['top'].configure(bg=t['panel'])
                ui['live'].configure(bg=t['panel'], fg=t['panel'])
                ui['time'].configure(bg=t['panel'])
                ui['task'].configure(bg=t['panel'])
                ui['dur'].configure(bg=t['panel'], text="")

    def update_clock(self):
        now = datetime.now()
        self.time_lbl.configure(text=now.strftime("%I:%M:%S %p"))
        self.date_lbl.configure(text=now.strftime("%A, %B %d, %Y"))
        if now.second == 0:
            self.check_live_task()
        self.root.after(1000, self.update_clock)

    def reset_schedule(self):
        if messagebox.askyesno("Confirm", "Reset karne par default time-table wapas aa jayega. Continue?"):
            self.schedule = self.default_schedule()
            self.save_data()
            self.render_schedule()
            self.check_live_task()

    def add_doubt(self):
        text = self.doubt_entry.get().strip()
        sub = self.doubt_sub.get()
        if text:
            self.doubts.append({"sub": sub, "text": text})
            self.doubt_entry.delete(0, tk.END)
            self.save_data()
            self.render_doubts()

    def render_doubts(self):
        for w in self.doubts_list_frame.winfo_children():
            w.destroy()
        t = self.theme
        for i, doubt in enumerate(self.doubts):
            f = tk.Frame(self.doubts_list_frame, bg=t['panel_alt'], pady=8, padx=10)
            f.pack(fill="x", pady=4)
            lbl = tk.Label(f, text=f"[{doubt['sub']}] {doubt['text']}", bg=t['panel_alt'], fg=t['fg'], font=("Arial", 10))
            lbl.pack(side="left", fill="x", expand=True, anchor="w")
            tk.Button(f, text="✔ Solved", bg="#34c759", fg="white", bd=0, font=("Arial", 9, "bold"), command=lambda idx=i: self.remove_doubt(idx)).pack(side="right")

    def remove_doubt(self, index):
        del self.doubts[index]
        self.save_data()
        self.render_doubts()

    def add_task(self):
        text = self.task_entry.get().strip()
        if text:
            self.tasks.append(text)
            self.task_entry.delete(0, tk.END)
            self.save_data()
            self.render_tasks()

    def render_tasks(self):
        for w in self.tasks_list_frame.winfo_children():
            w.destroy()
        t = self.theme
        for i, task in enumerate(self.tasks):
            f = tk.Frame(self.tasks_list_frame, bg=t['panel_alt'], pady=8, padx=10)
            f.pack(fill="x", pady=4)
            lbl = tk.Label(f, text=task, bg=t['panel_alt'], fg=t['fg'], font=("Arial", 10))
            lbl.pack(side="left", fill="x", expand=True, anchor="w")
            tk.Button(f, text="✔ Done", bg="#34c759", fg="white", bd=0, font=("Arial", 9, "bold"), command=lambda idx=i: self.remove_task(idx)).pack(side="right")

    def remove_task(self, index):
        del self.tasks[index]
        self.save_data()
        self.render_tasks()

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile="MyStudyData.json")
        if file_path:
            data = {
                'schedule': self.schedule,
                'tasks': self.tasks,
                'doubts': self.doubts,
                'theme': self.current_theme_name
            }
            with open(file_path, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo("Success", "Data export successful!")

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                if 'schedule' in data: self.schedule = data['schedule']
                if 'tasks' in data: self.tasks = data['tasks']
                if 'doubts' in data: self.doubts = data['doubts']
                if 'theme' in data: 
                    self.current_theme_name = data['theme']
                    self.theme = self.themes[self.current_theme_name]
                
                self.save_data()
                self.apply_theme()
                self.render_schedule()
                self.render_doubts()
                self.render_tasks()
                self.check_live_task()
                messagebox.showinfo("Success", "Data successfully import ho gaya hai!")
            except:
                messagebox.showerror("Error", "Error! File format sahi nahi hai.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProDashboard(root)
    root.mainloop()