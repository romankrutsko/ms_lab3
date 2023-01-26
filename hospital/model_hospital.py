import numpy as np
from base.model import Model
from hospital.dispose_hospital import Dispose_hospital
from hospital.process_hospital import Process_hospital

class Model_hospital(Model):
    def __init__(self, elements: list):
        super().__init__(elements)
        self.event = elements[0]

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')
            for e in self.list:
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next and not isinstance(e, Dispose_hospital):
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

    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self):
        super().print_result()
        global_mean_interval_between_arriving_to_the_lab = 0
        global_mean_time_finishing_accumulator = 0
        num_of_processors = 0
        num_of_finished = 0

        for e in self.list:
            e.result()
            if isinstance(e, Process_hospital):
                num_of_processors += 1

                if e.name == 'to lab reception':
                    global_mean_interval_between_arriving_to_the_lab = e.delta_t_following_to_the_lab_reception / e.quantity

                if e.name == 'to reception':
                    print(
                        f'Mean_time_finishing for type 2 = {e.delta_t_finished2_new / e.type2_cnt_new if e.type2_cnt_new != 0 else np.inf}')

            elif isinstance(e, Dispose_hospital):
                global_mean_time_finishing_accumulator += e.delta_t_finished1 + e.delta_t_finished2 + e.delta_t_finished3
                num_of_finished += e.quantity
                print(
                    f'Mean_time_finishing for type 1 = {e.delta_t_finished1 / e.type1_cnt if e.type1_cnt != 0 else np.inf}')
                print(
                    f'Mean_time_finishing for type 2 = {e.delta_t_finished2 / e.type2_cnt if e.type2_cnt != 0 else np.inf}')
                print(
                    f'Mean_time_finishing for type 3 = {e.delta_t_finished3 / e.type3_cnt if e.type3_cnt != 0 else np.inf}')
                print()

        global_mean_time_finishing = global_mean_time_finishing_accumulator / num_of_finished

        print(
            f'Global mean interval between arriving to the lab: {global_mean_interval_between_arriving_to_the_lab}')
        print(f'Global mean time of finishing: {global_mean_time_finishing}')
        print()
