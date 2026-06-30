from roomba_node import Node
import heapq

VISION_RADIUS = 1

def initialize_observed_map(full_map, x, y):
    # make fog full map outside VISION_RADIUS
    if not full_map:
        return []

    rows = len(full_map)
    cols = len(full_map[0])
    observed_map = []

    for i in range(rows):
        row = []
        for j in range(cols):
            if abs(i - x) <= VISION_RADIUS and abs(j - y) <= VISION_RADIUS:
                row.append(full_map[i][j])
            else:
                row.append(-1)
        observed_map.append(row)

    return tuple(tuple(row) for row in observed_map)


def update_observed_map(full_map, current_observed_map, x, y):
    # clear fog in VISION_RADIUS
    if not full_map or not current_observed_map:
        return current_observed_map

    updated_map = [list(row) for row in current_observed_map]
    rows = len(full_map)
    cols = len(full_map[0])

    for i in range(rows):
        for j in range(cols):
            if abs(i - x) <= VISION_RADIUS and abs(j - y) <= VISION_RADIUS:
                updated_map[i][j] = full_map[i][j]

    return tuple(tuple(row) for row in updated_map)


def partial_observation_search(full_map):
    if not full_map:
        return None
    
    initial_full_node = Node(full_map)
    if initial_full_node.is_clean():
        return initial_full_node
    fog_node = Node(initialize_observed_map(full_map, initial_full_node.x, initial_full_node.y))

    frontier = []
    frontier.append((fog_node, initial_full_node))
    reached = set()

    while frontier:
        fog_node, full_node = frontier.pop()

        reached.add(fog_node.state)

        moves = fog_node.get_moves()
        print(moves)

        for dx, dy, action in moves:
            fog_child_state = fog_node.generate_new_state(dx, dy)
            full_child_state = full_node.generate_new_state(dx, dy)
            x, y = fog_node.x + dx, fog_node.y + dy
            fog_child_state = update_observed_map(full_child_state, fog_child_state, x, y)

            if fog_child_state in reached:
                continue

            fog_child_node = Node(fog_child_state, fog_node, action)
            full_child_node = Node(full_child_state)
            
            if full_child_node.is_clean():
                return fog_child_node

            frontier.append((fog_child_node, full_child_node))

    return None


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

    full_map = (
        (0, 3, 1, 2, 0, 2),
        (0, 0, 0, 2, 0, 0),
        (0, 1, 0, 0, 1, 1),
        (0, 0, 0, 0, 0, 1),
        (2, 2, 0, 2, 0, 0),
        (0, 0, 0, 0, 1, 0)
    )

    fog_map = initialize_observed_map(full_map, 0, 1)
    print_map(full_map, tile_set)
    print_map(fog_map, tile_set)

    result_node = partial_observation_search(full_map)
    path = result_node.get_parent_list()

    for node in path:
        print_map(node.state, tile_set)
        print("-"*20)