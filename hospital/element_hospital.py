from base.element import Element

class Element_hospital(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_type_element = None

    def get_delay(self):
        if self.name == 'reception':
            if self.next_type_element == 1:
                self.delay_mean = 15
            elif self.next_type_element == 2:
                self.delay_mean = 40
            elif self.next_type_element == 3:
                self.delay_mean = 30
        return super().get_delay()