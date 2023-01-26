from gettext import npgettext
import numpy as np
from bank.Bank_Process import Bank_Process

from base.process import Process
from hospital.process_hospital import Process_hospital

class Model:
    def __init__(self, elements: list):
        self.list = elements
        self.event = 0
        self.t_next = 0.0
        self.t_curr = self.t_next

    def event1(self):
        pass

    def printStatistic(self):
       print(f"numCreate = {self.numCreate} numProcess = {self.numProcess} failure = {self.failure}")
   
    def print_info(self):
        for item in self.list:
         item.print_info()
   
    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')

            for e in self.list:
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next:
                    self.t_next = t_next_val
                    self.event = e.id

            for e in self.list:
                e.do_Statistics(self.t_next - self.t_curr)

            self.t_curr = self.t_next

            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if self.t_curr in e.t_next:
                    e.out_act()

            self.print_info()

        return self.print_result()

    def print_result(self):
        print('-----RESULT-----')

        global_max_observed_queue_length = 0
        global_mean_queue_length_accumulator = 0
        global_failure_probability_accumulator = 0
        global_mean_load_accumulator = 0
        num_of_processors = 0

        for e in self.list:
            e.result()
            if isinstance(e, Process) or isinstance(e, Bank_Process) or isinstance(e,Process_hospital) :
                num_of_processors += 1
                mean_queue_length = e.mean_queue / self.t_curr

                failure_probability = e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0

                mean_load = e.mean_load / self.t_curr

                global_mean_queue_length_accumulator += mean_queue_length
                global_failure_probability_accumulator += failure_probability
                global_mean_load_accumulator += mean_load

                if e.max_observed_queue > global_max_observed_queue_length:
                    global_max_observed_queue_length = e.max_observed_queue

                print(f"avg queue size: {mean_queue_length}")
                print(f"probability to fail: {failure_probability}")
                print(f"avg load: {mean_load}")
                print()

        global_mean_queue_length = global_mean_queue_length_accumulator / num_of_processors
        global_failure_probability = global_failure_probability_accumulator / num_of_processors
        global_mean_load = global_mean_load_accumulator / num_of_processors

        print(f"global max queue size: {global_max_observed_queue_length}")
        print(f"global mean queue size: {global_mean_queue_length}")
        print(f"global probability to fail: {global_failure_probability}")
        print(f"global mean load: {global_mean_load}")
        print()
