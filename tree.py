# Return a search tree
# Calculate distance (search tree) between two balls
#   e.g. distance D=1 means the two balls are next to each other
# Couple distance with direction
#   horizontal=False (row direction, False), 0 move 'left', 1 move 'right'
#   vertical=True (col direction, True), 2 move 'up', 3 move 'down'
# Distance with direction is a dictionary
#   like ball#1: [ball#2, distance, direction]

from grid import Grid


def ball_name(x, y):
    return str(x)+str(y)


def sign(x):
    if x > 0:
        return 1
    return -1


def real_distance(x1, x2):
    return sign(x2-x1)*(abs(x2-x1)-1)


def tree(grid=Grid):
    dist = dict()
    for b in grid.balls:
        s_ball = ball_name(b[0], b[1])
        dist[s_ball] = []  # (l=None, r=None, u=None, d=None)
        # horizontal search
        row = grid.row[b[0]]
        b_col_index = row.index(b[1])
        if b_col_index > 0:
            # there is a ball on the left
            dist[s_ball].append(['row', b[1], row[b_col_index-1]])
        if b_col_index < len(row)-1:
            # there is a ball on the right
            dist[s_ball].append(['row', b[1], row[b_col_index+1]])
        # vertical search
        col = grid.col[b[1]]
        b_row_index = col.index(b[0])
        if b_row_index > 0:
            # there is a ball on the top
            dist[s_ball].append(['col', b[0], col[b_row_index-1]])
        if b_row_index < len(col)-1:
            # there is a ball on the top
            dist[s_ball].append(['col', b[0], col[b_row_index+1]])
    return dist


if __name__ == '__main__':
    game = Grid(6, 5)
    game.place(0, 1)
    game.place(0, 4)
    game.place(3, 3)
    game.place(5, 3)
    game.place(1, 3)
    search = tree(game)
    print(search)