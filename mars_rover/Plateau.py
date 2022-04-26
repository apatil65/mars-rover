from .Utils import Try


@Try.catch
class Plateau:
    MIN_WIDTH = 0
    MIN_HEIGHT = 0

    def __init__(self, width, height, min_width=0, min_height=0):
        self.width = width
        self.height = height
        self.MIN_WIDTH = min_width
        self.MIN_HEIGHT = min_height
        self.col = set()
        
    def move_available(self, position):
        """
        :param Position position:
        :return:
        """
        print(position.x, position.y, self.width, self.height)
        return self.MIN_WIDTH <= position.x < self.width and self.MIN_HEIGHT <= position.y < self.height
    
    def reserve_position(self, x, y):
        return "{}:{}".format(x, y)
    
    def create_obstace(self, x, y):
        key = self.reserve_position(x, y)
        self.col.add(key)
        
    def check_if_position_reserved(self, x, y):
        key = self.reserve_position(x, y)
        #print(x, y, self.col, key)
        #print(key in self.col)
        return key in self.col
