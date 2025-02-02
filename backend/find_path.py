import math
import copy

def to_elevation_grid(points):
    grid = []
    base = int(math.sqrt(len(points)))
    for i, point in enumerate(points):
        if i % base == 0:
            grid.append([])
        grid[-1].append(point[1])

    return grid

    
def find_path(points, scale, bodyweight, height):
    elevation_grid = to_elevation_grid(points)
    pending_list = [[[0,0],0]]
    base = len(elevation_grid)
    # print(len(elevation_grid[0]), len(elevation_grid), scale)

    grid = []
    for i in range(base):
        grid.append([])
        for j in range(base):
            grid[-1].append(0)

    bmi = bodyweight/(height ** 2)
    def cost_func(curr_features, move_features):
        gradient = (move_features[0] - curr_features[0])/scale
        pace = 0.6 * math.exp(gradient + 0.5) * bmi/20
        cost = pace * scale/1000
        return cost
    
    def find_moves(curr, pending_list):
        moves = []
        x, y = curr[0][0], curr[0][1]
        curr_cost = curr[1]
        curr_features = elevation_grid[x][y]

        if x - 1 >= 0 and grid[y][x - 1] == 0:
            moves.append([[x - 1, y], curr_cost + cost_func(curr_features, elevation_grid[y][x - 1])])
        if x + 1 != base and grid[y][x + 1] == 0:
            moves.append([[x + 1, y], curr_cost + cost_func(curr_features, elevation_grid[y][x + 1])])
        if y - 1 >= 0 and grid[y - 1][x] == 0:
            moves.append([[x, y - 1], curr_cost + cost_func(curr_features, elevation_grid[y - 1][x])])
        if y + 1 != base and grid[y + 1][x] == 0:
            moves.append([[x, y + 1], curr_cost + cost_func(curr_features, elevation_grid[y + 1][x])])
        
        moves.sort(key=lambda x: x[1])
        ref = copy.deepcopy(moves)

        for i, end in enumerate(pending_list):
            for j, move in enumerate(ref):
                if end[0] == move[0]:
                    if end[1] <= move[1]:
                        ref.remove(move)
                        if move in moves:
                            moves.remove(move)

                    else:
                        pending_list.remove(end)
                        grid[end[0][1]][end[0][0]] = 0

            if len(moves) != 0:
                for move in moves:
                    if end[1] >= move[1]:
                        pending_list.insert(i, move)
                        grid[move[0][1]][move[0][0]] = curr[0]
                        del moves[0]
                        i += 1

                    elif i == len(pending_list) - 1:
                        pending_list += moves
                        for move in moves:
                            grid[move[0][1]][move[0][0]] = curr[0]
                        break
                    else:
                        break

        pending_list.remove(curr)
    
    while True:
        end = pending_list[0]

        if end[0] == [base - 1, base - 1]:
            curr = end[0]
            path = []
            while curr != [0,0]:
                path.append(curr)
                curr = grid[curr[1]][curr[0]]
                
            path.append(curr)
            return path, end[1]

        find_moves(end, pending_list)
                    