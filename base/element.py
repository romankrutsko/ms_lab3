import base.fun_rand as fun
from copy import deepcopy
import numpy as np


class Element:
    nextId = 0

    def __init__(self,  delay_mean=None, name=None, distribution='',delay_dev=0., probability=1, max_queue=float('inf'), n_channel=1):
        self.t_next = [0]
        self.delay_mean = delay_mean
        self.delay_dev = delay_dev
        self.distribution = distribution
        self.quantity = 0
        self.t_curr = self.t_next
        self.state = [0]
        self.next_element = None
        self.id = Element.nextId
        self.name = f'id:{self.id}' if name is None else name
        Element.nextId += 1

        self.queue = 0
        self.channels = n_channel
        self.max_queue = max_queue
        self.probability = [probability]
        self.priority = [1] 
        self.failure = 0
        self.mean_load = 0
        self.mean_queue = 0.0
        self.max_observed_queue = 0


    def choose_next_element(self):
        if self.probability != [1] and self.priority != [1]:
            raise Exception('Route selection is ambiguous: probability and priority are set simultaneously')
        elif self.probability != [1]:
            next_element = np.random.choice(a=self.next_element, p=self.probability)
            return next_element
        elif self.priority != [1]:
            next_element = self.choose_by_priority()
            return next_element
        elif self.probability == [1] and self.priority == [1]:
            return self.next_element

    def choose_by_priority(self):
        priorities = deepcopy(self.priority)
        min_queue = float('inf')
        min_queue_index = 0

        for p in range(len(priorities)):
            if min(priorities) == 100000:
                break

            max_pr_index = priorities.index(min(priorities))
            if 0 in self.next_element[max_pr_index].state:
                return self.next_element[max_pr_index]
            else:
                if self.next_element[max_pr_index].queue < min_queue:
                    min_queue = self.next_element[max_pr_index].queue
                    min_queue_index = self.next_element.index(self.next_element[max_pr_index])

            priorities[max_pr_index] = 100000

        return self.next_element[min_queue_index]
    

    def get_delay(self):
        if 'exp' == self.distribution:
            return fun.exp(self.delay_mean)
        elif 'norm' == self.distribution:
            return fun.norm(self.delay_mean, self.delay_dev)
        elif 'uniform' == self.distribution:
            return fun.uniform(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean

    def in_act(self):
        pass

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def set_t_next(self, t_next_new):
        self.t_next = t_next_new

    def get_t_curr(self):
        return self.t_curr

    def out_act(self):
        self.quantity += 1

    def result(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def print_info(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} t_next = {self.t_next}')

    def do_Statistics(self, delta):
        self.mean_queue += self.queue * delta

        if self.queue > self.max_observed_queue:
            self.max_observed_queue = self.queue

        for i in range(self.channels):
            self.mean_load += self.state[0] * delta

        self.mean_load = self.mean_load / self.channels

    def get_channels(self):
        channels = []
        for i in range(self.channels):
            if self.state[0] == 0:
                channels.append(i)
        return channels

    def get_current_channel(self):
        channels = []
        for i in range(self.channels):
            if self.t_next[0] == self.t_curr:
                channels.append(i)
        return channels