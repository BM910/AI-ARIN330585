import random

class Node:
    def __init__(self, state, parent=None, action=None, depth=0, g_value=0, use_heuristic=False):
        self.state = tuple(tuple(row) for row in state) if isinstance(state, list) else state
        self.parent = parent
        self.action = action
        self.depth = depth

        self.x, self.y = self.find_roomba()

        self.g_value = g_value
        self.h_value = self.heu_min_manhattan() + self.heu_dirty_value() if use_heuristic else 0
        self.f_value = self.g_value + self.h_value

    def __str__(self):
        state = ""
        for row in self.state:
            state += str(row) + '\n'
        move_and_cost = f"Moved {self.action}"
        return state + move_and_cost

    def heu_dirty_value(self, weight=1.8):
        dirty_tile_count = 0
        for row in self.state:
            dirty_tile_count += (row.count(1))
        return dirty_tile_count * weight

    def heu_min_manhattan(self, weight=0.1):
        min_dist = -1
        x, y = self.x, self.y
        for i, row in enumerate(self.state):
            for j, tile in enumerate(row):
                if tile == 1:
                    dist = abs(x - i) + abs(y - j)
                    min_dist = dist if min_dist == -1 else min(min_dist, dist)
        return 0 if min_dist == -1 else min_dist * weight
    
    def heu_sum_manhattan(self, weight=0.6):
        sum_dist = 0
        x, y = self.x, self.y
        for i, row in enumerate(self.state):
            for j, tile in enumerate(row):
                if tile == 1:
                    sum_dist += abs(x - i) + abs(y - j)
        return sum_dist * weight

    def is_clean(self):
        for row in self.state:
            if 1 in row:
                return False
        return True

    def find_roomba(self):
        for i, row in enumerate(self.state):
            if 3 in row:
                return (i, row.index(3))
        return (-1, -1)

    def get_moves(self):
        x, y = self.x, self.y
        full_moves = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]
        # prioritized_moves = [] # prioritize
        valid_moves = []

        for dx, dy, action in full_moves:
            if self.check_valid_move(x, y, dx, dy):
                nx, ny = x + dx, y + dy
                if self.state[nx][ny] == 1:
                    action += f" and cleaned [{nx}][{ny}]"
                    # prioritized_moves.append((dx, dy, action)) # prioritize
                valid_moves.append((dx, dy, action))
        
        # random.shuffle(valid_moves) # randomize
        # valid_moves = prioritized_moves + valid_moves # prioritize
        return valid_moves
                    
    def check_valid_move(self, x, y, dx, dy):
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(self.state) and 0 <= ny < len(self.state[0]) and self.state[nx][ny] != 2:
            return True
        return False
    
    def generate_new_state(self, dx, dy, return_list=False):
        x, y = self.x, self.y
        nx, ny = x + dx, y + dy
        new_state = [list(row) for row in self.state]
        new_state[x][y] = 0
        new_state[nx][ny] = 3
        if return_list:
            return new_state
        else:
            return tuple(tuple(row) for row in new_state)
    
    def get_parent_list(self):
        path = [self]
        while self.parent:
            path.append(self.parent)
            self = self.parent
        return path[::-1]
    

def randomize_map(custom_size=None):
    global current_room

    rows = custom_size if custom_size else random.randint(4, 8)
    cols = rows

    choices = [0, 1, 2]
    weights = [0.60, 0.20, 0.20]

    current_room = []
    for r in range(rows):
        row_tiles = random.choices(choices, weights=weights, k=cols)
        current_room.append(row_tiles)
        
    roomba_placed = False
    while not roomba_placed:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        
        if current_room[random_row][random_col] in (0, 1):
            current_room[random_row][random_col] = 3
            roomba_placed = True

    return tuple(tuple(row) for row in current_room)


if __name__ == "__main__":
    def print_map(state, tile_set=None):
        for row in state:
            if tile_set:
                for tile in row:
                    print(tile_set[tile], end=" ")
                print()
            else:
                print(row)

    tile_set = {-1: "~", 0: " ", 1: "_", 2: "#", 3: "*"}

    map = randomize_map(6)
    print_map(map, tile_set)
    print()
    print_map(map)