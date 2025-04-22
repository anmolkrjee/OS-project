#  main.py
from scheduler import Process
from simulation import simulate_round_robin
from visualization import visualize_power_consumption

if __name__ == "__main__":
    try:
        processes = [
            Process(1, 0, 100, 1),
            Process(2, 1, 5, 2),
            Process(3, 2, 8, 1),
            Process(4, 3, 2, 2)
        ]
        
        time_quantum = 3
        completed, cpu = simulate_round_robin(processes, time_quantum)
        visualize_power_consumption(completed, cpu)
    
    except Exception as e:
        print(f"Error: {e}") 
