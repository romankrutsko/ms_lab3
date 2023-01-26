import numpy as np
import base.element as element


class Process(element.Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = [0] * self.channels
        self.t_next = [np.inf]*self.channels

    def in_act(self):
        channels = self.get_channels()
        if (len(channels)>0):
            for channel in channels:
                self.state[channel] = 1
                self.t_next[channel] = self.t_curr+self.get_delay()
                break
        else:           
            if (self.queue < self.max_queue):
                self.queue = self.queue + 1
            else:
                self.failure+=1
            
    def out_act(self):
        channels = self.get_current_channel()
        for channel in channels:
            super().out_act()
            self.t_next[channel] = float('inf')
            self.state[channel] = 0

            if self.queue > 0:
                self.queue -= 1
                self.state[channel] = 1
                self.t_next[channel] = self.t_curr + self.get_delay()
            if self.next_element is not None:
                choosen_el = np.random.choice(a=self.next_element)
                choosen_el.in_act()
                