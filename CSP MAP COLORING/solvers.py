import copy
import random
from collections import deque

def is_valid_coloring(variable : list, color : list, assignment : dict, neighbors : dict):
    for neighbor in neighbors.get(variable, []):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def count_conflicts(variable: str, color: str, assignment: dict, neighbors: dict):
    conflicts = 0
    for neighbor in neighbors.get(variable, []):
        if neighbor in assignment and assignment[neighbor] == color:
            conflicts += 1
    return conflicts

def backtrack_fc(variables : list, domains : dict, assignment : dict, neighbors : dict):
    if len(assignment) == len(variables):
        return assignment

    var = next(v for v in variables if v not in assignment)

    for color in domains[var]:
        if is_valid_coloring(var, color, assignment, neighbors):
            assignment[var] = color
            
            local_domains = copy.deepcopy(domains)
            
            failure_early = False
            
            for neighbor in neighbors.get(var, []):
                if neighbor not in assignment:
                    if color in local_domains[neighbor]:
                        local_domains[neighbor].remove(color)
                    
                    # domain == zero -> can't solve
                    if not local_domains[neighbor]:
                        failure_early = True
                        break
            
            # recursive
            if not failure_early:
                result = backtrack_fc(variables, local_domains, assignment, neighbors)
                if result is not None:
                    return result
            
            # backtracking
            del assignment[var]

    return None

def min_conflicts(variables: list, domains: dict, neighbors: dict, max_steps: int = 1000):
    assignment = {}
    for var in variables:
        assignment[var] = random.choice(domains[var])
        
    for step in range(max_steps):
        conflicted_vars = []
        for var in variables:
            if count_conflicts(var, assignment[var], assignment, neighbors) > 0:
                conflicted_vars.append(var)
                
        if not conflicted_vars:
            print(f"Min-Conflicts solved in {step} steps")
            return assignment
            
        var = random.choice(conflicted_vars)
        
        current_colors = domains[var]
        min_count = float('inf')
        best_colors = []
        
        for color in current_colors:
            num_conflicts = count_conflicts(var, color, assignment, neighbors)
            if num_conflicts < min_count:
                min_count = num_conflicts
                best_colors = [color]
            elif num_conflicts == min_count:
                best_colors.append(color)
                
        assignment[var] = random.choice(best_colors)
        
    return None

def ac3(domains: dict, neighbors: dict, initial_queue: list = None):
    queue = deque()
    if initial_queue is not None:
        queue.extend(initial_queue)
    else:
        for x in neighbors:
            for y in neighbors[x]:
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        
        if remove_inconsistent_values(x, y, domains):
            if len(domains[x]) == 0:
                return False
                
            for z in neighbors.get(x, []):
                if z != y:
                    queue.append((z, x))
    return True

def remove_inconsistent_values(x: str, y: str, domains: dict):
    removed = False
    for x_color in list(domains[x]):
        has_consistent_choice = any(y_color != x_color for y_color in domains[y])
        
        if not has_consistent_choice:
            domains[x].remove(x_color)
            removed = True
            
    return removed

def backtrack_ac3(variables: list, domains: dict, assignment: dict, neighbors: dict):
    if len(assignment) == len(variables):
        return assignment

    var = next(v for v in variables if v not in assignment)

    for color in domains[var]:
        if is_valid_coloring(var, color, assignment, neighbors):
            assignment[var] = color
            
            local_domains = copy.deepcopy(domains)
            local_domains[var] = [color]
            
            arcs = [(neighbor, var) for neighbor in neighbors.get(var, []) if neighbor not in assignment]
            
            if ac3(local_domains, neighbors, initial_queue=arcs):
                result = backtrack_ac3(variables, local_domains, assignment, neighbors)
                if result is not None:
                    return result
            
            del assignment[var]

    return None