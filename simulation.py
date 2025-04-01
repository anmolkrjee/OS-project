# simulation.py
from scheduler import Process, CPU, round_robin_scheduling
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def calculate_metrics(completed_processes, cpu):
    total_turnaround = sum(p.finish_time - p.arrival_time for p in completed_processes)
    total_waiting = sum((p.finish_time - p.arrival_time - p.burst_time) for p in completed_processes)
    
    return {
        "avg_turnaround": total_turnaround / len(completed_processes),
        "avg_waiting": total_waiting / len(completed_processes),
        "total_power": cpu.power_consumption,
        "idle_time": cpu.idle_time
    }

def simulate_round_robin(processes, time_quantum):
    if not processes:
        raise ValueError("Process list is empty")
    if time_quantum <= 0:
        raise ValueError("Time quantum must be positive")

    logging.info("Starting simulation...")
    cpu = CPU()
    completed_processes = round_robin_scheduling(processes, time_quantum, cpu)

    metrics = calculate_metrics(completed_processes, cpu)
    logging.info(f"Average Turnaround Time: {metrics['avg_turnaround']:.2f}")
    logging.info(f"Average Waiting Time: {metrics['avg_waiting']:.2f}")
    logging.info(f"Total Power: {metrics['total_power']:.2f} Joules")
    logging.info(f"Idle Time: {metrics['idle_time']} units")

    return completed_processes, cpu