from grid import Grid
from snap import *
from roll import Roll
import sys
sys.setrecursionlimit(1000)


class PointyTree:
    def __init__(self, n, mum=None, solution=False, children=None):
        self.n = n
        self.mum = mum

        self.point = Tree

        self.children = []
        if children is not None:
            for child in children:
                self.children.append(child)
        self.solution = solution

    def add_point(self, point):
        assert isinstance(point, Tree)
        self.point = point

    def add_child(self, child):
        assert isinstance(child, PointyTree)
        self.children.append(child)


class Tree:
    def __init__(self, node, n, row, col, coordinate, children=None):
        self.n = n

        assert isinstance(node, list)
        assert isinstance(row, dict)
        assert isinstance(col, dict)

        self.node = node[:]  # absolute coordinate
        self.row = row.copy()
        self.col = col.copy()
        self.coordinate = coordinate

        self.mum = None
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __str__(self):
        return 'ID{}: '.format(self.n)

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def get_child(self, n):
        return self.children[n]

    def print_children(self):
        print('Children')
        for i in self.children:
            print(' {0} '.format(i), end='')
        print('\n')


class Fling:
    def __init__(self, n_row=8, n_col=7):
        self.n_row = n_row
        self.n_col = n_col
        self.board = Grid(n_row, n_col)

        self.path = []
        self.balls = None

        self.n = 0
        self.root = Tree
        self.point = PointyTree
        self.path = []
        # self.path.append(0)

    def start(self):
        row_t = self.board.row
        col_t = self.board.col
        self.balls = len(self.board.balls)

        self.root = Tree(snap(row_t, col_t), self.n, row_t, col_t, [])
        self.point = PointyTree(self.n)

        self.build(self.root, self.point)
        a, self.path = self.search(self.point)
        # if self.find(self.root):
        #     print('!\n!\nSolution found!\n!\n!')
        # else:
        #     print('!\n!\nNo solution found!\n!\n!')

    def build(self, mum, pointy_mum):
        self.__find_child(mum, pointy_mum)
        if len(mum.children) > 0:
            for i in range(len(mum.children)):
                self.build(mum.children[i], pointy_mum.children[i])

    @staticmethod
    def __transpose(table, length):
        assert isinstance(table, dict)
        result = dict()
        for i in range(length):
            result[i] = []
        for k in table.keys():
            if len(table[k]) != 0:
                for j in table[k]:
                    result[j].append(k)
        return result

    def __find_child(self, mum, pointy_mum):
        # find all  children under a mum
        assert isinstance(mum, Tree)
        for item in mum.node:
            if item[0]:
                l = mum.row[item[1]]
            else:
                l = mum.col[item[1]]
            m = Roll(item[2], item[3], l)
            # print(item)
            # print(l)
            m.move()
            if item[0]:
                table = mum.row.copy()
                table[item[1]] = m.result
                # print(table)
                table_t = self.__transpose(table, self.n_col)
                # print(table_t)
                node_t = snap(table, table_t)
            else:
                table = mum.col.copy()
                table[item[1]] = m.result
                # print(table)
                table_t = self.__transpose(table, self.n_row)
                node_t = snap(table_t, table)
            if len(node_t) != 0:
                self.n += 1
                if item[0]:
                    child = Tree(node_t, self.n, table, table_t, item)
                else:
                    child = Tree(node_t, self.n, table_t, table, item)
                n_row = 0
                n_col = 0
                for i in mum.row.keys():
                    if len(mum.row[i]) > 0:  # not empty
                        n_row += 1
                for i in mum.col.keys():
                    if len(mum.col[i]) > 0:
                        n_col += 1
                if n_row == 1 or n_col == 1:
                    # solution found
                    solution = True
                else:
                    solution = False
                pointy_child = PointyTree(self.n, pointy_mum.mum, solution, children=None)
                pointy_child.add_point(child)
                mum.add_child(child)
                pointy_mum.add_child(pointy_child)

    def search(self, mum, path=[]):
        # print('======')
        # print(mum)
        # print(path)
        # print(mum.node)
        # self.print_board(mum.row)
        # mum.print_children()
        # print('\n')
        assert isinstance(mum, PointyTree)
        if mum.solution:
            return True, path
        if len(mum.children) == 0:
            # dead end
            return False, path[:-1]
        step = 0
        for child in mum.children:
            c, steps = self.search(child, path+[step])
            if c:
                return True, steps
            step += 1
        return False, path[:-1]

    def print_board(self, table=None):
        if table is None:
            table = self.board.row
        print_l = ['-'] * self.n_col
        for i in range(self.n_row):
            temp_print_l = print_l[:]
            if i in table.keys():
                for j in table[i]:
                    temp_print_l[j] = 'O'
            print('{0}.  {1}'.format(i, temp_print_l))

    @staticmethod
    def __print_path_element(l):
        if l[0]:
            print('[{0}, {1}] >> '.format(l[1], l[2]), end="")
            if l[3] == 1:
                print('right')
            else:
                print('left')
        else:
            print('[{0}, {1}] >> '.format(l[2], l[1]), end="")
            if l[3] == 1:
                print('down')
            else:
                print('up')

    def print_path(self, path=None):
        if path is None:
            path = self.path
        print(path)
        mum = self.root
        for i in range(len(path)):
            # print('====')
            child = mum.get_child(path[i])
            self.__print_path_element(child.coordinate)
            # self.print_board(mum.row)
            mum = child


if __name__ == '__main__':
    game = Fling()
    l = [0,5,1,3,2,5,3,4,3,5,3,6,4,1,4,5,5,0,5,1,6,0,6,2,7,2,7,5]
    for i in range(int(len(l)/2)):
        game.board.place(l[2*i], l[2*i+1])
    # for i in l:
    #     game.board.place(i[0], i[1])
    game.print_board()
    game.start()
    game.print_path()