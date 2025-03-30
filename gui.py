# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import json
from scheduler import Process, CPU, round_robin_scheduling
from matplotlib.ticker import MaxNLocator

class EnergyEfficientSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy-Efficient CPU Scheduler")
        self.root.geometry("1400x900")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_widgets()
        self.setup_layout()
        self.processes = []
        
    def configure_styles(self):
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        self.style.configure('Treeview', rowheight=25, font=('Segoe UI', 9))
        self.style.map('TButton',
                      foreground=[('active', 'black'), ('disabled', 'gray')],
                      background=[('active', '#e1e1e1'), ('disabled', '#f5f5f5')])
        self.style.configure('TNotebook', background='#f5f5f5')
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'))
    
    def create_widgets(self):
        self.left_frame = ttk.Frame(self.root, padding=10)
        self.right_frame = ttk.Frame(self.root, padding=10)
        
        # Process input
        self.input_frame = ttk.LabelFrame(self.left_frame, text="Process Input", padding=10)
        self.create_process_input_widgets()
        
        # Controls
        self.control_frame = ttk.LabelFrame(self.left_frame, text="Simulation Controls", padding=10)
        self.create_control_widgets()
        
        # Results
        self.result_frame = ttk.LabelFrame(self.right_frame, text="Results", padding=10)
        self.create_result_widgets()
        
        # Visualizations
        self.visualization_frame = ttk.LabelFrame(self.right_frame, text="Visualizations", padding=10)
        self.create_visualization_widgets()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
    
    def create_process_input_widgets(self):
        columns = ("PID", "Arrival Time", "Burst Time", "Priority")
        self.process_table = ttk.Treeview(self.input_frame, columns=columns, show="headings", height=8)
        
        for col, width in zip(columns, [50, 90, 80, 70]):
            self.process_table.heading(col, text=col)
            self.process_table.column(col, width=width, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(self.input_frame, orient=tk.VERTICAL, command=self.process_table.yview)
        self.process_table.configure(yscrollcommand=scrollbar.set)
        
        # Entry fields
        self.pid_var = tk.IntVar()
        self.arrival_var = tk.IntVar()
        self.burst_var = tk.IntVar()
        self.priority_var = tk.IntVar(value=1)
        
        ttk.Label(self.input_frame, text="PID:").grid(row=1, column=0, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.pid_var, width=8).grid(row=1, column=1)
        
        ttk.Label(self.input_frame, text="Arrival Time:").grid(row=1, column=2, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.arrival_var, width=8).grid(row=1, column=3)
        
        ttk.Label(self.input_frame, text="Burst Time:").grid(row=2, column=0, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.burst_var, width=8).grid(row=2, column=1)
        
        ttk.Label(self.input_frame, text="Priority:").grid(row=2, column=2, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.priority_var, width=8).grid(row=2, column=3)
        
        # Buttons
        button_frame = ttk.Frame(self.input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        ttk.Button(button_frame, text="Add Process", command=self.add_process).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_process).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_processes).pack(side=tk.LEFT, padx=5)
        
        # Import/Export
        io_frame = ttk.Frame(self.input_frame)
        io_frame.grid(row=4, column=0, columnspan=4)
        ttk.Button(io_frame, text="Import", command=self.import_processes).pack(side=tk.LEFT, padx=5)
        ttk.Button(io_frame, text="Export", command=self.export_processes).pack(side=tk.LEFT, padx=5)
        
        # Layout
        self.process_table.grid(row=0, column=0, columnspan=4, sticky='nsew')
        scrollbar.grid(row=0, column=4, sticky='ns')

    def add_process(self):
        try:
            pid = self.pid_var.get()
            arrival = self.arrival_var.get()
            burst = self.burst_var.get()
            priority = self.priority_var.get()
            
            if pid <= 0 or arrival < 0 or burst <= 0 or priority <= 0:
                raise ValueError("All values must be positive integers")
            
            for item in self.process_table.get_children():
                if self.process_table.item(item)['values'][0] == pid:
                    raise ValueError(f"PID {pid} already exists")
            
            self.process_table.insert("", "end", values=(pid, arrival, burst, priority))
            self.pid_var.set(pid + 1)
            self.arrival_var.set("")
            self.burst_var.set("")
            self.status_var.set(f"Added process {pid}")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error adding process")

    def remove_process(self):
        try:
            selected = self.process_table.selection()
            if not selected:
                raise ValueError("No process selected")
            
            pid = self.process_table.item(selected)['values'][0]
            self.process_table.delete(selected)
            self.status_var.set(f"Removed process {pid}")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error removing process")

    def clear_processes(self):
        for item in self.process_table.get_children():
            self.process_table.delete(item)
        self.status_var.set("Cleared all processes")

    def import_processes(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
            if not filepath:
                return
            
            with open(filepath, 'r') as f:
                processes = json.load(f)
            
            self.clear_processes()
            for proc in processes:
                self.process_table.insert("", "end", values=(
                    proc['pid'], proc['arrival'], proc['burst'], proc['priority']
                ))
            
            self.status_var.set(f"Imported {len(processes)} processes")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Import failed")

    def export_processes(self):
        try:
            processes = []
            for item in self.process_table.get_children():
                pid, arrival, burst, priority = self.process_table.item(item)['values']
                processes.append({
                    'pid': pid,
                    'arrival': arrival,
                    'burst': burst,
                    'priority': priority
                })
            
            if not processes:
                raise ValueError("No processes to export")
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON", "*.json")]
            )
            
            if not filepath:
                return
            
            with open(filepath, 'w') as f:
                json.dump(processes, f, indent=2)
            
            self.status_var.set(f"Exported {len(processes)} processes")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Export failed")

    def create_control_widgets(self):
        # Time quantum
        ttk.Label(self.control_frame, text="Time Quantum:").grid(row=0, column=0, sticky='e')
        self.quantum_var = tk.IntVar(value=3)
        ttk.Entry(self.control_frame, textvariable=self.quantum_var, width=8).grid(row=0, column=1, sticky='w')
        
        # CPU params
        ttk.Label(self.control_frame, text="CPU Parameters", style='Header.TLabel').grid(row=1, column=0, columnspan=2)
        
        params = [
            ("Base Power (W):", "base_power_var", 100),
            ("Max Freq (GHz):", "max_freq_var", 3.0),
            ("Min Freq (GHz):", "min_freq_var", 1.0)
        ]
        
        for i, (label, var_name, default) in enumerate(params):
            setattr(self, var_name, tk.DoubleVar(value=default))
            ttk.Label(self.control_frame, text=label).grid(row=i+2, column=0, sticky='e')
            ttk.Entry(self.control_frame, textvariable=getattr(self, var_name), width=8).grid(row=i+2, column=1, sticky='w')
        
        # Run button
        ttk.Button(
            self.control_frame,
            text="Run Simulation",
            command=self.run_simulation
        ).grid(row=5, column=0, columnspan=2, pady=15)

    def create_result_widgets(self):
        columns = ("PID", "Start", "Finish", "Turnaround", "Waiting")
        self.result_table = ttk.Treeview(self.result_frame, columns=columns, show="headings", height=8)
        
        for col, width in zip(columns, [50, 80, 80, 80, 80]):
            self.result_table.heading(col, text=col)
            self.result_table.column(col, width=width, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_table.yview)
        self.result_table.configure(yscrollcommand=scrollbar.set)
        
        # Metrics
        self.metrics_frame = ttk.Frame(self.result_frame)
        self.avg_turnaround_var = tk.StringVar(value="Avg Turnaround: -")
        self.avg_waiting_var = tk.StringVar(value="Avg Waiting: -")
        self.power_var = tk.StringVar(value="Power Used: - J")
        self.idle_var = tk.StringVar(value="Idle Time: -")
        self.savings_var = tk.StringVar(value="Energy Saved: -%")
        
        for var in [self.avg_turnaround_var, self.avg_waiting_var, self.power_var, self.idle_var, self.savings_var]:
            ttk.Label(self.metrics_frame, textvariable=var).pack(anchor=tk.W)
        
        # Layout
        self.result_table.pack(fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.metrics_frame.pack(fill=tk.X)

    def create_visualization_widgets(self):
        self.notebook = ttk.Notebook(self.visualization_frame)
        
        # Power tab
        self.power_tab = ttk.Frame(self.notebook)
        self.power_fig, self.power_ax = plt.subplots(figsize=(10, 4))
        self.power_canvas = FigureCanvasTkAgg(self.power_fig, self.power_tab)
        self.power_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.power_tab, text="Power")
        
        # Gantt tab
        self.gantt_tab = ttk.Frame(self.notebook)
        self.gantt_fig, self.gantt_ax = plt.subplots(figsize=(10, 4))
        self.gantt_canvas = FigureCanvasTkAgg(self.gantt_fig, self.gantt_tab)
        self.gantt_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.gantt_tab, text="Gantt")
        
        # Freq tab
        self.freq_tab = ttk.Frame(self.notebook)
        self.freq_fig, self.freq_ax = plt.subplots(figsize=(10, 4))
        self.freq_canvas = FigureCanvasTkAgg(self.freq_fig, self.freq_tab)
        self.freq_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.freq_tab, text="Frequency")
        
        self.notebook.pack(fill=tk.BOTH, expand=True)

    def setup_layout(self):
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.input_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        self.control_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.result_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        self.visualization_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def run_simulation(self):
        try:
            # Get processes
            processes = []
            for item in self.process_table.get_children():
                pid, arrival, burst, priority = self.process_table.item(item)['values']
                processes.append(Process(pid, arrival, burst, priority))
            
            if not processes:
                raise ValueError("No processes to simulate")
            
            # Get params
            quantum = self.quantum_var.get()
            cpu = CPU(
                base_power=self.base_power_var.get(),
                max_frequency=self.max_freq_var.get(),
                min_frequency=self.min_freq_var.get()
            )
            
            # Run simulation
            completed = round_robin_scheduling(processes, quantum, cpu)
            
            # Update results
            self.result_table.delete(*self.result_table.get_children())
            total_turnaround = 0
            total_waiting = 0
            
            for proc in completed:
                turnaround = proc.finish_time - proc.arrival_time
                waiting = turnaround - proc.burst_time
                total_turnaround += turnaround
                total_waiting += waiting
                
                self.result_table.insert("", "end", values=(
                    proc.pid,
                    proc.start_time,
                    proc.finish_time,
                    turnaround,
                    waiting
                ))
            
            # Update metrics
            n = len(completed)
            self.avg_turnaround_var.set(f"Avg Turnaround: {total_turnaround/n:.2f}")
            self.avg_waiting_var.set(f"Avg Waiting: {total_waiting/n:.2f}")
            self.power_var.set(f"Power Used: {cpu.power_consumption:.2f} J")
            self.idle_var.set(f"Idle Time: {cpu.idle_time}")
            
            # Energy savings
            baseline = sum(p.burst_time for p in processes) * cpu.base_power
            savings = ((baseline - cpu.power_consumption) / baseline) * 100
            self.savings_var.set(f"Energy Saved: {savings:.1f}%")
            
            # Update plots
            self.update_plots(completed, cpu)
            self.status_var.set("Simulation completed")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Simulation failed")

    def update_plots(self, processes, cpu):
        # Power plot
        self.power_ax.clear()
        if cpu.power_history:
            times, power = zip(*cpu.power_history)
            self.power_ax.step(times, power, where='post', label='Power (W)')
            self.power_ax.set_xlabel("Time")
            self.power_ax.set_ylabel("Power (W)")
            self.power_ax.legend()
            self.power_ax.grid(True)
            self.power_canvas.draw()
        
        # Gantt chart
        self.gantt_ax.clear()
        for proc in processes:
            for start, end in proc.execution_history:
                self.gantt_ax.barh(
                    f"P{proc.pid}",
                    end - start,
                    left=start,
                    color='skyblue',
                    edgecolor='black'
                )
        self.gantt_ax.set_xlabel("Time")
        self.gantt_ax.invert_yaxis()
        self.gantt_canvas.draw()
        
        # Frequency plot
        self.freq_ax.clear()
        if cpu.frequency_history:
            times, freq = zip(*cpu.frequency_history)
            self.freq_ax.step(times, freq, where='post', label='Freq (GHz)', color='orange')
            self.freq_ax.set_xlabel("Time")
            self.freq_ax.set_ylabel("Frequency (GHz)")
            self.freq_ax.legend()
            self.freq_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyEfficientSchedulerGUI(root)
    root.mainloop()