# scheduler.py
from dataclasses import dataclass
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    priority: int
    remaining_time: int = None
    start_time: int = -1
    finish_time: int = -1
    execution_history: List[Tuple[int, int]] = None

    def __post_init__(self):
        self.remaining_time = self.burst_time
        self.execution_history = []

class CPU:
    def __init__(self, base_power: float = 100.0, max_frequency: float = 3.0, min_frequency: float = 1.0):
        self.base_power = base_power
        self.max_frequency = max_frequency
        self.min_frequency = min_frequency
        self.current_frequency = max_frequency
        self.power_consumption = 0.0
        self.idle_time = 0
        self.power_history = []
        self.frequency_history = []

    def execute(self, process: Process, time_units: int, current_time: int):
        if process.start_time == -1:
            process.start_time = current_time

        self.current_frequency = self.max_frequency if process.priority == 1 else self.min_frequency
        self.frequency_history.append((current_time, self.current_frequency))

        power = self.base_power * (self.current_frequency / self.max_frequency)
        self.power_consumption += power * time_units
        self.power_history.append((current_time, power))

        process.remaining_time -= time_units
        process.execution_history.append((current_time, current_time + time_units))

        if process.remaining_time <= 0:
            process.finish_time = current_time + time_units + process.remaining_time

    def idle(self, time_units: int, current_time: int):
        self.idle_time += time_units
        self.power_history.append((current_time, self.base_power * 0.1))
        self.frequency_history.append((current_time, self.min_frequency))

def round_robin_scheduling(processes: List[Process], time_quantum: int, cpu: CPU) -> List[Process]:
    queue = []
    current_time = 0
    completed_processes = []
    remaining_processes = processes.copy()

    while remaining_processes or queue:
        new_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
        for p in new_processes:
            queue.append(p)
            remaining_processes.remove(p)

        if queue:
            current_process = queue.pop(0)
            execution_time = min(time_quantum, current_process.remaining_time)
            cpu.execute(current_process, execution_time, current_time)
            current_time += execution_time

            if current_process.remaining_time > 0:
                queue.append(current_process)
            else:
                completed_processes.append(current_process)
        else:
            cpu.idle(1, current_time)
            current_time += 1

    return completed_processes