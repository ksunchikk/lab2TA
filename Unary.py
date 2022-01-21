from classes import Node


class Unary(Node.Node):

    def __init__(self, child=None):
        super().__init__()
        self.child: Node.Node = child

    def set_child(self, child):
        self.child: Node.Node = child
        return self
