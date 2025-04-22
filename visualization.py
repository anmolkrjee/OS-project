#  visualization.py
import matplotlib.pyplot as plt
from typing import List
from scheduler import Process, CPU

def visualize_power_consumption(completed_processes: List[Process], cpu: CPU):
    if not cpu.power_history:
        print("No power history data to visualize.")
        return

    times, power = zip(*cpu.power_history)
    
    plt.figure(figsize=(10, 5))
    plt.step(times, power, where='post', label='Power (W)')
    plt.xlabel('Time (units)')
    plt.ylabel('Power (Watts)')
    plt.title('CPU Power Consumption')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

def visualize_gantt_chart(completed_processes: List[Process]):
    if not completed_processes:
        print("No processes to visualize.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    
    for i, process in enumerate(completed_processes):
        for start, end in process.execution_history:
            ax.barh(
                f'P{process.pid}',
                end - start,
                left=start,
                color='skyblue',
                edgecolor='black',
                alpha=0.7
            )
    
    ax.set_xlabel('Time (units)')
    ax.set_ylabel('Processes')
    ax.set_title('Gantt Chart')
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def visualize_frequency_usage(cpu: CPU):
    if not cpu.frequency_history:
        print("No frequency data to visualize.")
        return

    times, freq = zip(*cpu.frequency_history)
    
    plt.figure(figsize=(10, 5))
    plt.step(times, freq, where='post', label='Frequency (GHz)', color='orange')
    plt.xlabel('Time (units)')
    plt.ylabel('Frequency (GHz)')
    plt.title('CPU Frequency Scaling')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()
