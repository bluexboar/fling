class Grid:
    def __init__(self, n_row, n_col):
        self.n_col = n_col
        self.n_row = n_row
        # Create a nested boolean list, False: no ball; True: ball
        self.row = dict()  # a dict uses row as keys
        self.col = dict()  # a dict uses col as keys
        for i in range(self.n_row):
            self.row[i] = []
        for i in range(self.n_col):
            self.col[i] = []
        self.balls = []

    def place(self, x=int, y=int):
        if x < 0 or x > self.n_row - 1:
            print('Row position out of range [0, {0}]'.format(self.n_row - 1))
        elif y < 0 or y > self.n_col - 1:
            print('Column position out of range [0, {0}]'.format(self.n_col - 1))
        elif y in self.row[x]:
            print('Ball exists')
        else:
            self.row[x].append(y)
            self.row[x].sort()
            self.col[y].append(x)
            self.col[y].sort()
            self.balls.append([x, y])
            # print('Ball placed successfully')

    def take(self, x=int, y=int):
        if x < 0 or x > self.n_row - 1:
            print('Row position out of range [0, {0}]'.format(self.n_row - 1))
        elif y < 0 or y > self.n_col - 1:
            print('Column position out of range [0, {0}]'.format(self.n_col - 1))
        elif y in self.row[x]:
            self.row[x].remove(y)
            self.col[y].remove(x)
            self.balls.remove([x, y])
            print('Ball taken off successfully')
        else:
            print('Ball not exists')
