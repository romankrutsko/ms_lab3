from bank.Bank_Process import Bank_Process
from base.model import Model
import numpy as np

class Bank_model(Model):

    def __init__(self, elements: list, balancing=None):
        super().__init__(elements)
        self.queue_move = 0
        self.time = 0
        self.balancing = balancing
        self.all_clients, self.out_clients = 0, 0
        self.average_cnt_client_in_bank = 0

    def calc_average_cnt_client_in_bank(self, delta):
        self.average_cnt_client_in_bank += delta * (
                    self.balancing[0].queue + self.balancing[1].queue + self.balancing[0].state[0] +
                    self.balancing[1].state[0])


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

            self.calc_average_cnt_client_in_bank(self.t_next - self.t_curr)

            self.t_curr = self.t_next

            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if self.t_curr in e.t_next:
                    e.out_act()

            self.print_info()
            self.change_queue()
        return self.print_result()


    def change_queue(self):
        queue_list = list()
        for element in self.list:
            if isinstance(element, Bank_Process):
                queue_list.append(element.queue)
        q_1 = queue_list[0] - queue_list[1]
        q_2 = queue_list[1] - queue_list[0]
        if q_1 >= 2:
            self.list[1].queue -= 1
            self.list[2].queue += 1
            print("From CASHIER_1's queue one car left to CASHIER_2 queue.")
            self.queue_move += 1
        elif q_2 >= 2:
            self.list[2].queue -= 1
            self.list[1].queue += 1
            print("From CASHIER_2's queue one car left to CASHIER_1 queue.")
            self.queue_move += 1

    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self):
        super().print_result()
        global_mean_time_of_departure_accumulator = 0
        global_mean_time_in_bank_accumulator = 0
        num_of_processors = 0

        for e in self.list:
            e.result()
            if isinstance(e, Bank_Process):
                num_of_processors += 1

                global_mean_time_of_departure_accumulator += e.delta_t_departure / e.quantity
                global_mean_time_in_bank_accumulator += e.delta_t_in_bank / e.quantity

                print(f'Mean time of departure = {e.delta_t_departure / e.quantity}')

        average_cnt_client_in_bank = self.average_cnt_client_in_bank / self.t_curr
        global_mean_time_of_departure = global_mean_time_of_departure_accumulator / num_of_processors
        global_mean_time_in_bank = global_mean_time_in_bank_accumulator / num_of_processors

        print(f"Global mean client cnt in bank: {average_cnt_client_in_bank}")
        print(f"Global mean time of departure: {global_mean_time_of_departure}")
        print(f"Global mean time in bank: {global_mean_time_in_bank}")
        print(f"Global change queue cnt: {self.queue_move}")
        print()
