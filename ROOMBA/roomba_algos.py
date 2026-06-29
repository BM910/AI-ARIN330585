import math
import random
import heapq
from collections import deque
from roomba_node import Node


def bfs1(initial_state):
    if not initial_state:
        return
    node = Node(initial_state)

    frontier = deque()
    reached = set()
    frontier.append(node)
    frontier_set = set()
    frontier_set.add(initial_state)

    while frontier:
        node = frontier.popleft()
        frontier_set.discard(node.state)
        reached.add(node.state)

        if node.is_clean():
            message = f"Reached {len(reached)} states"
            return (node, message)
        
        moves = node.get_moves()
        
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, node.depth+1)

            if child_node.state not in frontier_set and child_node.state not in reached:
                frontier.append(child_node)
                frontier_set.add(child_node.state)

    return None


def bfs2(initial_state):
    if not initial_state:
        return
    node = Node(initial_state)

    frontier = deque()
    reached = set()
    frontier.append(node)
    frontier_set = set()
    frontier_set.add(initial_state)

    while frontier:
        node = frontier.popleft()
        frontier_set.discard(node.state)
        reached.add(node.state)
        
        moves = node.get_moves()
        
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, node.depth+1)
            if child_node.is_clean():
                message = f"Reached {len(reached)} states"
                return (child_node, message)

            if child_node.state not in frontier_set and child_node.state not in reached:
                frontier.append(child_node)
                frontier_set.add(child_node.state)

    return None


def dfs1(initial_state):
    if not initial_state:
        return
    node = Node(initial_state)

    frontier = []
    reached = set()
    frontier.append(node)
    frontier_set = set()
    frontier_set.add(initial_state)

    while frontier:
        node = frontier.pop()
        frontier_set.discard(node.state)
        reached.add(node.state)

        if node.is_clean():
            message = f"Reached {len(reached)} states"
            return (node, message)
        
        moves = node.get_moves()
        
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, node.depth+1)

            if child_node.state not in frontier_set and child_node.state not in reached:
                frontier.append(child_node)
                frontier_set.add(child_node.state)

    return None


def dfs2(initial_state):
    if not initial_state:
        return
    node = Node(initial_state)

    frontier = []
    reached = set()
    frontier.append(node)
    frontier_set = set()
    frontier_set.add(initial_state)

    while frontier:
        node = frontier.pop()
        frontier_set.discard(node.state)
        reached.add(node.state)
        
        moves = node.get_moves()
        
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, node.depth+1)
            if child_node.is_clean():
                message = f"Reached {len(reached)} states"
                return (child_node, message)

            if child_node.state not in frontier_set and child_node.state not in reached:
                frontier.append(child_node)
                frontier_set.add(child_node.state)

    return None


def ids(initial_state, max_depth=100):
    if not initial_state:
        return None
    
    for depth in range(max_depth):
        reached = set() 
        result = dls(initial_state, depth, reached)
        if result != "cutoff":
            return result
    return None


def dls(initial_state, limit, reached):
    node = Node(initial_state)
    return recursive_dls(node, limit, reached)


def recursive_dls(node: Node, limit, reached):
    if node.is_clean():
        return node
    if limit == 0:
        return "cutoff"
    
    reached.add(node.state)
    
    cutoff_occurred = False
    moves = node.get_moves()
    
    for dx, dy, action in moves:
        new_state = node.generate_new_state(dx, dy)
        
        if new_state in reached:
            continue
            
        child_node = Node(new_state, node, action, node.depth + 1)
        result = recursive_dls(child_node, limit - 1, reached)
        
        if result == "cutoff":
            cutoff_occurred = True
        elif result is not None:
            return result
            
    reached.remove(node.state)
    
    if cutoff_occurred:
        return "cutoff"
    return None

def ucs(initial_state):
    if not initial_state:
        return
    node = Node(initial_state)

    counter = 0
    frontier = [(node.g_value, counter, node)]
    reached = {str(node.state) : 0}

    while frontier:
        current_g_value, _, node = heapq.heappop(frontier)
        if node.is_clean():
            return node

        if current_g_value > reached[str(node.state)]:
            continue

        moves = node.get_moves()
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, depth=node.depth+1, g_value=node.g_value+1)
            
            x, y = child_node.x, child_node.y
            if node.state[x][y] == 1:
                child_node.g_value -= 1

            child_str = str(child_node.state)
            child_cost = child_node.g_value
            if child_str not in reached or child_cost < reached[child_str]:
                reached[child_str] = child_cost
                counter += 1
                heapq.heappush(frontier, (child_cost, counter, child_node))

    return None


def greedy(initial_state):
    if not initial_state:
        return
    node = Node(initial_state, use_heuristic=True)
    
    counter = 0
    frontier = [(node.h_value, counter, node)]
    reached = set()

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if node.is_clean():
            return node
        reached.add(node.state)

        moves = node.get_moves()
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, depth=node.depth+1, use_heuristic=True)
            if child_node.state not in reached:
                counter += 1
                heapq.heappush(frontier, (child_node.h_value, counter, child_node))

    return None


def a_star(initial_state):
    if not initial_state:
        return
    node = Node(initial_state, g_value=0, use_heuristic=True)
    
    counter = 0
    frontier = [(node.f_value, counter, node)]
    reached = {str(node.state) : node.g_value}

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if node.is_clean():
            message = f"Reached {len(reached)} states"
            return (node, message)
        


        if node.g_value > reached[str(node.state)]:
            continue

        moves = node.get_moves()
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, depth=node.depth+1 ,g_value=node.g_value+1, use_heuristic=True)
            if "cleaned" in child_node.action:
                child_node.g_value -= 0.5

            child_node_str = str(child_node.state)
            if child_node_str not in reached or child_node.g_value < reached[child_node_str]:
                    reached[child_node_str] = child_node.g_value
                    counter += 1
                    heapq.heappush(frontier, (child_node.f_value, counter, child_node))

    return None


def ida_star(initial_state, max_f=1000):
    if not initial_state:
        return
    limit = 0
    node = None
    total_reached = 0
    max_reached = float(0)
    while limit <= max_f:
        node, new_limit, len_reached = a_star_limited(initial_state, limit)
        total_reached += len_reached
        max_reached = max(max_reached, len_reached)
        if node != "cutoff":
            message = f"Reached total {total_reached} states\nReached max {max_reached} states"
            return (node, message)
        limit = max(limit +1, new_limit)
    return node


def a_star_limited(initial_state, limit):
    node = Node(initial_state, g_value=0, use_heuristic=True)

    counter = 0
    frontier = [(node.f_value, counter, node)]
    reached = {str(node.state) : node.g_value}
    min_new_limit = -1

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if node.is_clean():
            return (node, min_new_limit, len(reached))

        if node.g_value > reached[str(node.state)]:
            continue

        moves = node.get_moves()
        for dx, dy, action in moves:
            if "cleaned" in action:
                child_node = Node(node.generate_new_state(dx, dy), node, action, depth=node.depth+1 ,g_value=node.g_value+0.5, use_heuristic=True)
            else:
                child_node = Node(node.generate_new_state(dx, dy), node, action, depth=node.depth+1 ,g_value=node.g_value+1, use_heuristic=True)

            if child_node.f_value >= limit:
                min_new_limit = child_node.f_value if min_new_limit == -1 else min(min_new_limit, child_node.f_value)
                continue

            child_node_str = str(child_node.state)
            if child_node_str not in reached or child_node_str in reached and child_node.g_value < reached[child_node_str]:
                    reached[child_node_str] = child_node.g_value
                    counter += 1
                    heapq.heappush(frontier, (child_node.f_value, counter, child_node))

    if min_new_limit == -1:
        return (None, float('inf'), len(reached))
    return ("cutoff", min_new_limit, len(reached))


def simple_hc(initial_state):
    if not initial_state:
        return
    node = Node(initial_state, use_heuristic=True)

    while True:
        moves = node.get_moves()
        next_node = None
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, use_heuristic=True)
            if child_node.h_value < node.h_value:
                next_node = child_node
                break
        
        if next_node is None:
            break
        node = next_node
    
    return node


def steepest_ahc(initial_state):
    if not initial_state:
        return
    node = Node(initial_state, use_heuristic=True)

    while True:
        moves = node.get_moves()
        next_node = None
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, use_heuristic=True)
            if child_node.h_value < node.h_value:
                next_node = child_node
        
        if next_node is None:
            break
        node = next_node
    
    return node


def stochastic_hc(initial_state):
    if not initial_state:
        return
    node = Node(initial_state, use_heuristic=True)

    while True:
        moves = node.get_moves()
        better_child_nodes = []
        for dx, dy, action in moves:
            child_node = Node(node.generate_new_state(dx, dy), node, action, use_heuristic=True)
            if child_node.h_value < node.h_value:
                better_child_nodes.append(child_node)
        next_node = better_child_nodes[random.randint(0, len(better_child_nodes) - 1)] if len(better_child_nodes) > 0 else None
        
        if next_node is None:
            break
        node = next_node
    
    return node


def random_restart_hc(initial_state, max_restart=10):
    if not initial_state:
        return

    best_overall_node = None
    for i in range(max_restart):
        node = Node(initial_state, use_heuristic=True)

        while True:
            if node.is_clean():
                return node
            
            moves = node.get_moves()
            better_child_nodes = []

            for dx, dy, action in moves:
                child_node = Node(node.generate_new_state(dx, dy), node, action, use_heuristic=True)
                if child_node.h_value < node.h_value:
                    better_child_nodes.append(child_node)

            if not better_child_nodes:
                break

            better_child_nodes.sort(key=lambda x: x.h_value)
            best_h = better_child_nodes[0].h_value

            best_choices = [n for n in better_child_nodes if n.h_value == best_h]
            node = random.choice(best_choices)

            if best_overall_node is None or node.h_value < best_overall_node.h_value:
                best_overall_node = node
            
    return best_overall_node


def local_beam_search(initial_state, k=2):
    if not initial_state or k <= 0:
        return None
    
    node = Node(initial_state, use_heuristic=True)
    if node.is_clean():
        return node
    
    best_overall_node = node

    current_nodes = []
    for dx, dy, action in node.get_moves():
        child_node = Node(node.generate_new_state(dx, dy), node, action, use_heuristic=True)
        if child_node.is_clean():
            return child_node
        current_nodes.append(child_node)
    
    if child_node.h_value < best_overall_node.h_value:
        best_overall_node = child_node

    current_nodes.sort(key=lambda x: x.h_value)
    current_nodes = current_nodes[:k]

    visited_states = set(initial_state) 

    while current_nodes:
        neighbor_nodes = []
        
        for node in current_nodes:
            for dx, dy, action in node.get_moves():
                next_state = node.generate_new_state(dx, dy)
                
                if next_state in visited_states:
                    continue
                visited_states.add(next_state)

                child_node = Node(next_state, node, action, use_heuristic=True)
                
                if child_node.is_clean():
                    return child_node
                
                if child_node.h_value < best_overall_node.h_value:
                    best_overall_node = child_node

                neighbor_nodes.append(child_node)

        if not neighbor_nodes:
            break

        neighbor_nodes.sort(key=lambda x: x.h_value)
        
        current_nodes = neighbor_nodes[:k]

    return best_overall_node


def simulated_annealing(initial_state, temp=2, temp_min=0.01, cooling=0.95):
    if not initial_state:
        return
    
    current_node = Node(initial_state, use_heuristic=True)

    best_overall_node = current_node

    temperature = temp
    while temperature > temp_min:
        if current_node.is_clean():
            return current_node
        
        moves = current_node.get_moves()
        if not moves:
            break

        dx, dy, action = random.choice(moves)
        next_node = Node(current_node.generate_new_state(dx, dy), current_node, action + str(f" temp: {temperature:.4f}"), use_heuristic=True)
        delta = next_node.h_value - current_node.h_value

        if delta < 0:
            current_node = next_node
        else:
            p = math.exp(- delta / temperature)
            if random.random() < p:
                current_node = next_node

        if current_node.h_value < best_overall_node.h_value:
            best_overall_node = current_node
        temperature = cooling * temperature

    if current_node.is_clean():
        return current_node
    else:
        return best_overall_node
    
