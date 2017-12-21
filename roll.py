# Move a ball to hit another ball (or several balls on the line)
# Move only when the distance is larger than 1 (not next to each other)
# A basic move is, 1-->5: 4; or 5-->1: 2
# When multiple balls on the line, it is more complicated:
#   1-->3,4,5:  2,3,4
#   1-->3,4,6:  2,3,5
# The first ball always moves, while the ball being hit moves depending on the next one


class Roll:
    def __init__(self, b1, direction, l):
        self.b1_fix = b1
        self.b1 = self.b1_fix
        self.b1_index = None
        self.b2 = None
        self.b2_index = None
        self.b3 = None
        self.b3_index = None
        self.direction = direction
        self.l = l
        self.result = []

    def update(self, b1, direction):
        self.b1 = b1
        self.direction = direction
        self.l = []
        self.l = self.result
        self.result = []

    def move(self):
        self.b1_index = self.l.index(self.b1)
        self.b2 = self.l[self.b1_index + self.direction]
        self.__kick()
        if self.direction == -1:
            self.result.reverse()
        if 0 < self.b1_index < len(self.l)-1:
            if self.direction == 1:
                self.result = self.l[:self.b1_index] + self.result
            elif self.direction == -1:
                self.result += self.l[self.b1_index+1:]

    def __kick(self):
        self.result.append(self.b1 + self.direction
                           * (abs(self.b2-self.b1)-1))
        self.__hit()

    def __hit(self):
        self.b2_index = self.l.index(self.b2)
        self.b3_index = self.b2_index + self.direction
        if 0 <= self.b3_index < len(self.l):
            self.b3 = self.l[self.b3_index]
            if abs(self.b3-self.b2) > 1:
                # spacing between b2 and b3
                self.b1 = self.b2
                self.b2 = self.b3
                self.__kick()
            else:
                # no spacing, b2 stays
                self.result.append(self.b2)
                self.b2 = self.b3
                self.__hit()

    def print(self):
        print(self.result)


if __name__ == '__main__':
    l = [0, 4, 6, 7, 10]
    m1 = Roll(0, 1, l)
    m1.move()
    print(m1.result)
    m1.update(9, -1)
    m1.move()
    print(m1.result)
    m1.update(6, -1)
    m1.move()
    print(m1.result)
    m1.update(5, 1)
    m1.move()
    print(m1.result)