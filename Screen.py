from classes import Unary


class Screen(Unary.Unary):
    def __init__(self, child=None, val=''):
        super().__init__(child)
        self.val = val
