from classes import Node


class Binary(Node.Node):

    def __init__(self, left=None, right=None):
        super().__init__()
        self.left: Node.Node = left
        self.right: Node.Node = right

    def set_left(self, child):
        self.left: Node.Node = child
        return self

    def set_right(self, child):
        self.right: Node.Node = child
        return self