def __create_snap_entry(marker, entry_no, l):
    # use parse_roll() to create search entry
    node = []
    x = []
    for i in range(len(l)-1):
        if len(l) == 2 and abs(l[i] - l[i+1]) == 2:
                # if only two balls on the row
                x += [[l[i], 1]]
        elif abs(l[i] - l[i+1]) > 1:
            # only those distance>1 can move
            x += [[l[i], 1]]
            x += [[l[i+1], -1]]  # record two directions
    for item in x:
        node.append([marker, entry_no, item[0], item[1]])
    return node


def __find_corner(t1, t2, incline=1):
    if incline == 1:
        start = 0
        end = len(t1)
    else:
        start = len(t1)-1
        end = -1
    for i1 in range(start, end, incline):
        if len(t1[i1]) > 0:
            if incline == 1:
                i2 = t1[i1][0]
            else:
                i2 = t1[i1][-1]
            # print(t1[i1])
            # print(t2[i2])
            # print(incline)
            if len(t1[i1]) == 1 and len(t2[i2]) == 1:  # single ball at the corner
                if incline == 1:
                    if i2 == 0:
                        # print('db1')
                        return False, None, None
                    flag = True  # True only ball [1, i2)
                    for k in range(0, i2):
                        if len(t2[k]) > 0:
                            flag = False
                            break
                else:
                    if i2 == len(t2) - 1:
                        # print('db2')
                        return False, None, None
                    flag = True
                    for k in range(i2+1, len(t2)):
                        if len(t2[k]) > 0:
                            flag = False
                            break
                if flag:
                    # print('db3')
                    return False, None, None
            if incline == 1:
                return True, i1, t1[i1][0]
            return True, i1, t1[i1][-1]


def snap(row, col):  # row and col and dicts
    # create [True/False (row/col), row_no., b1 (first ball to move), b2 (ball to be hit)]
    # to reduce possible solutions, all solutions with unmovable corner balls should be eliminated
    node = []
    n1 = []
    n2 = []

    n_row = len(row.keys())
    n_col = len(col.keys())

    for i in row.keys():
        n1 += __create_snap_entry(True, i, row[i])
    for j in col.keys():
        n2 += __create_snap_entry(False, j, col[j])
    node = n1 + n2

    # corner balls are those closest to the corners
    # [0, 0],       [0, n_col-1]
    # [n_row-1, 0], [n_row-1, n_col-1]
    corner = []
    c1, b1x, b1y = __find_corner(row, col, 1)
    c2, b2x, b2y = __find_corner(row, col, -1)
    c3, b3y, b3x = __find_corner(col, row, 1)
    c4, b4y, b4x = __find_corner(col, row, -1)
    if c1 and c2 and c3 and c4:
        l = [[b1x, b1y], [b2x, b2y], [b3y, b3x], [b4y, b4x]]
    else:
        return []

    corner.append(l[0])
    for i in l[1:]:
        if i not in corner:
            corner.append(i)
    # print(corner)
    for i in corner:
        # find corner balls and put them in front
        for j in range(len(node)):
            if node[j][0]:  # row content
                if node[j][1] == i[0]:  # same row as the corner
                    b = node.pop(j)  # take it out
                    node.insert(0, b)  # put it in the front
            else:
                if node[j][1] == i[1]:  # same col as the corner
                    b = node.pop(j)
                    node.insert(0, b)
    # print(node)
    return node


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


if __name__ == '__main__':
    row = dict()
    for i in range(9):
        row[i] = []
    row[0] = [2]
    row[1] = [5, 6]
    row[2] = [1]
    row[3] = [4, 5]
    row[4] = [5]
    row[5] = [3]
    row[6] = [4]
    col = __transpose(row, 7)

    node = snap(row, col)
    print(node)

