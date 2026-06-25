"""
solvers.py

Three independent CSP-solving strategies for the Vietnam map-colouring
problem. Kept separate (rather than merged into one mega-function) so
each algorithm can be read, graded, and timed on its own:

  1. backtracking_search(...)   — backtracking + forward checking
  2. ac3(...)                   — arc-consistency preprocessing (AC-3),
                                   used here as a *preprocessing* step
                                   run once before backtracking starts
  3. min_conflicts(...)         — local search / hill-climbing repair

All three operate on the same representation:
  - colors    : list[str]              e.g. ["Red", "Teal", "Yellow", "Blue"]
  - neighbors : dict[str, set[str]]     adjacency graph
  - variables : list[str]               province names (the CSP variables)
"""

import random
from collections import deque


# ──────────────────────────────────────────────────────────────────────────
# 1. BACKTRACKING SEARCH + FORWARD CHECKING
# ──────────────────────────────────────────────────────────────────────────
def backtracking_search(
    variables: list[str],
    colors: list[str],
    neighbors: dict[str, set[str]],
    domains: dict[str, list[str]] | None = None,
) -> dict[str, str] | None:
    """
    Classic recursive backtracking with forward checking.

    domains: optional starting domains (e.g. already reduced by AC-3).
             If None, every variable starts with the full `colors` list.
    """
    if domains is None:
        domains = {v: list(colors) for v in variables}
    else:
        domains = {v: list(d) for v, d in domains.items()}  # deep-ish copy

    n = len(variables)

    def is_consistent(var: str, color: str, assignment: dict[str, str]) -> bool:
        for nb in neighbors.get(var, set()):
            if assignment.get(nb) == color:
                return False
        return True

    def forward_check(var: str, color: str, assignment: dict[str, str],
                       local_domains: dict[str, list[str]]) -> tuple[bool, dict]:
        """Temporarily remove `color` from unassigned neighbors' domains.
        Returns (ok, removed) where removed records what was pruned, so it
        can be restored on backtrack."""
        removed: dict[str, list[str]] = {}
        for nb in neighbors.get(var, set()):
            if nb in assignment:
                continue
            if color in local_domains[nb]:
                local_domains[nb] = [c for c in local_domains[nb] if c != color]
                removed[nb] = [color]
                if not local_domains[nb]:
                    return False, removed
        return True, removed

    def select_unassigned(assignment: dict[str, str]) -> str | None:
        # Minimum-Remaining-Values (MRV) heuristic: pick the variable with
        # the fewest legal values left — a small but real improvement over
        # plain first-unassigned ordering.
        unassigned = [v for v in variables if v not in assignment]
        if not unassigned:
            return None
        return min(unassigned, key=lambda v: len(domains[v]))

    def backtrack(assignment: dict[str, str]) -> dict[str, str] | None:
        if len(assignment) == n:
            return assignment

        var = select_unassigned(assignment)
        if var is None:
            return None

        for color in list(domains[var]):
            if is_consistent(var, color, assignment):
                assignment[var] = color
                ok, removed = forward_check(var, color, assignment, domains)
                if ok:
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                # restore pruned domain values
                for nb, vals in removed.items():
                    domains[nb].extend(vals)
                del assignment[var]

        return None

    return backtrack({})


# ──────────────────────────────────────────────────────────────────────────
# 2. AC-3 (ARC CONSISTENCY)
# ──────────────────────────────────────────────────────────────────────────
def ac3(
    variables: list[str],
    colors: list[str],
    neighbors: dict[str, set[str]],
) -> dict[str, list[str]] | None:
    """
    Standard AC-3 algorithm (Mackworth, 1977), matching the pseudocode:

        function AC-3(csp) returns the CSP, possibly with reduced domains
            queue <- all arcs (Xi, Xj) in csp
            while queue is not empty:
                (Xi, Xj) <- Remove-First(queue)
                if Remove-Inconsistent-Values(Xi, Xj):
                    for each Xk in Neighbors[Xi]:
                        add (Xk, Xi) to queue

    Returns the reduced domains dict, or None if any domain becomes empty
    (i.e. the CSP is shown to have no solution by arc consistency alone).

    Note: with no unary constraints and every province starting with all
    4 colours, AC-3 alone won't shrink any domain here (every value is
    still arc-consistent w.r.t. a "not equal" constraint when the
    neighbour's domain has 2+ values). It's included because it's the
    assigned algorithm, and it sets up the domains used to seed
    backtracking — in a less symmetric CSP (extra unary constraints, or
    if interleaved with assignment in MAC) it would prune much more.
    """
    domains: dict[str, list[str]] = {v: list(colors) for v in variables}

    # initial queue = all directed arcs (Xi, Xj) for every adjacency edge
    queue = deque()
    for xi in variables:
        for xj in neighbors.get(xi, set()):
            queue.append((xi, xj))

    def remove_inconsistent_values(xi: str, xj: str) -> bool:
        removed = False
        for x in list(domains[xi]):
            # "no value y in Domain[Xj] allows (x, y) to satisfy constraint(Xi, Xj)"
            # constraint here is simply x != y
            if not any(x != y for y in domains[xj]):
                domains[xi].remove(x)
                removed = True
        return removed

    while queue:
        xi, xj = queue.popleft()
        if remove_inconsistent_values(xi, xj):
            if not domains[xi]:
                return None  # CSP is inconsistent
            for xk in neighbors.get(xi, set()):
                if xk != xj:
                    queue.append((xk, xi))

    return domains


def ac3_then_backtracking(
    variables: list[str],
    colors: list[str],
    neighbors: dict[str, set[str]],
) -> tuple[dict[str, str] | None, dict[str, list[str]] | None]:
    """Run AC-3 as preprocessing, then backtracking+FC on the reduced domains.
    Returns (solution, domains_after_ac3) so callers can report how much
    AC-3 pruned."""
    reduced_domains = ac3(variables, colors, neighbors)
    if reduced_domains is None:
        return None, None
    solution = backtracking_search(variables, colors, neighbors, domains=reduced_domains)
    return solution, reduced_domains


# ──────────────────────────────────────────────────────────────────────────
# 3. MIN-CONFLICTS (LOCAL SEARCH)
# ──────────────────────────────────────────────────────────────────────────
def min_conflicts(
    variables: list[str],
    colors: list[str],
    neighbors: dict[str, set[str]],
    max_steps: int = 10_000,
    seed: int | None = None,
) -> dict[str, str] | None:
    """
    Min-conflicts local search, matching the pseudocode:

        function MIN-CONFLICTS(csp, max_steps) returns a solution or failure
            current <- an initial complete assignment for csp
            for i = 1 to max_steps:
                if current is a solution: return current
                var <- a randomly chosen conflicted variable
                value <- the value v for var that minimizes CONFLICTS(var, v, current, csp)
                set var = value in current
            return failure
    """
    rng = random.Random(seed)

    def conflicts(var: str, color: str, assignment: dict[str, str]) -> int:
        return sum(
            1 for nb in neighbors.get(var, set())
            if assignment.get(nb) == color
        )

    def conflicted_variables(assignment: dict[str, str]) -> list[str]:
        return [
            v for v in variables
            if conflicts(v, assignment[v], assignment) > 0
        ]

    # initial complete (likely-inconsistent) assignment — random colour for each province
    current: dict[str, str] = {v: rng.choice(colors) for v in variables}

    for _ in range(max_steps):
        conflicted = conflicted_variables(current)
        if not conflicted:
            return current  # solution found

        var = rng.choice(conflicted)
        # value that minimizes conflicts for `var`; ties broken randomly
        best_colors, best_count = [], None
        for c in colors:
            cnt = conflicts(var, c, current)
            if best_count is None or cnt < best_count:
                best_count, best_colors = cnt, [c]
            elif cnt == best_count:
                best_colors.append(c)
        current[var] = rng.choice(best_colors)

    return None  # failure — ran out of steps
