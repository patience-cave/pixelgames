

import math
from collections import deque


from collections import deque
from math import isinf


from collections import deque
import random
from typing import List, Tuple, Set, Dict, Optional

Pos = Tuple[int, int]

DIRS: List[Pos] = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, down, up


def is_floor(game, p: Pos) -> bool:
    """Return True if the position is a floor tile."""
    return game.get([p[0], p[1]]) == "floor"


def neighbors_4(p: Pos) -> List[Pos]:
    """4-directional neighbors."""
    x, y = p
    return [(x + dx, y + dy) for dx, dy in DIRS]


def bfs_reachable_floors(game, start: Pos, max_steps: int = 5) -> Set[Pos]:
    """
    Return all floor positions reachable from `start` in <= max_steps moves
    using only up/down/left/right on floor tiles. Includes `start` if it's floor.
    """
    # if not is_floor(game, start):
    #     return set()

    visited: Set[Pos] = {start}
    q = deque([(start, 0)])

    while q:
        pos, d = q.popleft()
        if d == max_steps:
            continue
        for n in neighbors_4(pos):
            if n not in visited and game.get(n) in ["floor", "chaser", "runner"]:
                visited.add(n)
                q.append((n, d + 1))
    return visited


def any_chaser_within(game, start: Pos, reachable: Set[Pos]) -> bool:
    """True if any reachable tile hosts a chaser."""
    for p in reachable:
        if game.get([p[0], p[1]]) == "chaser":
            return True
    return False


def multi_source_floor_distances(game, sources: List[Pos], max_depth: int) -> Dict[Pos, int]:
    """
    BFS distances from any 'source' over floor tiles, clipped at max_depth.
    Returns {pos: distance}, including sources with distance 0 (even if not floor).
    If a source isn't on a floor, we still start its neighbors that are floors at distance 1.
    """
    dist: Dict[Pos, int] = {}
    q = deque()

    # Seed queue: push floor sources at 0, and floor neighbors of non-floor sources at 1
    for s in sources:
        if is_floor(game, s):
            dist[s] = 0
            q.append(s)
        else:
            # Step to adjacent floors as distance 1
            for n in neighbors_4(s):
                if is_floor(game, n) and n not in dist:
                    dist[n] = 1
                    q.append(n)

    while q:
        p = q.popleft()
        d = dist[p]
        if d >= max_depth:
            continue
        for n in neighbors_4(p):
            if is_floor(game, n) and n not in dist:
                dist[n] = d + 1
                q.append(n)

    return dist

#safest_next_move(game, pos, threat_radius=5, allow_random_when_safe=False):
def safest_next_move(
    game,
    start: Pos,
    max_steps: int = 5,
    stay_if_safe: bool = True,
    rng: Optional[random.Random] = None,
) -> Pos:
    """
    If a 'chaser' exists within `max_steps` floor-steps of `start`, choose the adjacent floor
    move that maximizes the shortest path distance to any chaser (ties broken randomly).
    Otherwise:
      - if stay_if_safe=True (default), return `start`
      - else, move randomly to any adjacent floor (or stay if none)

    Returns the chosen position (which may equal `start`).
    """
    
    if rng is None:
        rng = random.Random()

    # 1) Floor-reachable region within max_steps
    reachable = bfs_reachable_floors(game, start, max_steps)
    
    # 2) Collect chasers in that region
    chasers: List[Pos] = [p for p in reachable if game.get([p[0], p[1]]) == "chaser"]

    if not chasers:
        return start

    return best_escape_move_from_positions(reachable, start, chasers[0])

    # Candidate next steps = adjacent floors (distance 1 from start)
    adj_floor: List[Pos] = [n for n in neighbors_4(start) if is_floor(game, n)]

    # Edge case: nowhere to go
    if not adj_floor:
        return start
    if len(adj_floor) == 1:
        return start

    # If no chasers within the reachable region
    if not chasers:
        if stay_if_safe:
            return start
        else:
            return rng.choice(adj_floor)

    # 3) Compute floor distances from any chaser (multi-source BFS), up to max_steps + 1
    #    (+1 so that immediate next moves also get meaningful separation values)
    dist_from_chaser = multi_source_floor_distances(game, chasers, max_depth=max_steps + 1)

    # 4) Score each adjacent floor: maximize distance to nearest chaser (unknown => treat as +inf)
    def score(p: Pos) -> int:
        return dist_from_chaser.get(p, max_steps + 2)  # higher is safer

    best_score = max(score(p) for p in adj_floor)
    best_moves = [p for p in adj_floor if score(p) == best_score]

    return rng.choice(best_moves)


from collections import deque
from math import isinf

def best_escape_move_from_positions(floors, me, chasers, width=None, height=None, allow_stay=False):
    """
    Given:
      - floors: set of (x, y) tiles that are walkable.
      - me: (x, y) for your current position.
      - chasers: list of (x, y) positions (or a single (x, y)).
      - width, height: optional, for bounds checking.
    
    Returns:
      The best next position [x, y] to move to, or None if trapped.
    """
    me = tuple(me)
    if isinstance(chasers[0], (int, float)):
        chasers = [tuple(chasers)]
    else:
        chasers = [tuple(c) for c in chasers]

    # Helpers
    def in_bounds(x, y):
        if width is None or height is None:
            return True
        return 0 <= x < width and 0 <= y < height

    def is_floor(x, y):
        return (x, y) in floors and in_bounds(x, y)

    def neighbors(x, y):
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if is_floor(nx, ny):
                yield nx, ny

    # 1) BFS from all chasers to compute distance map
    dist = {}
    q = deque()

    for cx, cy in chasers:
        if is_floor(cx, cy) and (cx, cy) not in dist:
            dist[(cx, cy)] = 0
            q.append((cx, cy))

    while q:
        x, y = q.popleft()
        d = dist[(x, y)]
        for nx, ny in neighbors(x, y):
            if (nx, ny) not in dist:
                dist[(nx, ny)] = d + 1
                q.append((nx, ny))

    # 2) Candidate moves
    candidates = []
    if allow_stay and is_floor(*me):
        candidates.append(me)
    for nx, ny in neighbors(*me):
        candidates.append((nx, ny))

    if not candidates:
        return None

    # Helper scores
    def openness(x, y):
        return sum(1 for _ in neighbors(x, y))

    def manhattan_to_chasers(x, y):
        return max(abs(x - cx) + abs(y - cy) for cx, cy in chasers)

    # 3) Score each move
    scored = []
    for x, y in candidates:
        d = dist.get((x, y), float('inf'))
        open_score = openness(x, y)
        manh = manhattan_to_chasers(x, y)
        d_sort = 10**9 if isinf(d) else d
        scored.append(((d_sort, open_score, manh), (x, y)))

    # Sort descending: safest first
    scored.sort(key=lambda s: (-s[0][0], -s[0][1], -s[0][2]))
    return scored[0][1]


# Impossibly Smark Bot
# def min_steps_to_chaser(game, me, chaser):
# #def best_escape_move(game, me, chaser, width, height, allow_stay=False):
#     """
#     Pick the next [x, y] tile (N/E/S/W step) that maximizes safety from a chaser.

#     - Only tiles where game.get([x, y]) == "floor" are walkable.
#     - Uses a BFS distance map from the chaser, then chooses among your legal moves:
#       1) maximize chaser distance (unreachable == safest),
#       2) then maximize openness (number of walkable neighbors),
#       3) then maximize Manhattan distance.
#     - If allow_stay is True, considers not moving as a candidate.
#     """

#     width = game.width+1
#     height = game.height+1
#     allow_stay = True

#     me = tuple(me)
#     # Accept a single chaser [x,y] or a list of them
#     if isinstance(chaser[0], (int, float)):
#         chasers = [tuple(chaser)]
#     else:
#         chasers = [tuple(c) for c in chaser]

#     def in_bounds(x, y):
#         return 0 <= x < width and 0 <= y < height

#     def is_floor(x, y):
#         return in_bounds(x, y) and game.get([x, y]) == "floor"

#     def neighbors(x, y):
#         for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
#             nx, ny = x + dx, y + dy
#             if is_floor(nx, ny):
#                 yield nx, ny

#     # --- 1) BFS from the chaser(s) to get shortest-path distance over floor tiles
#     dist = {}  # (x,y) -> int distance
#     q = deque()

#     for cx, cy in chasers:
#         if is_floor(cx, cy) and (cx, cy) not in dist:
#             dist[(cx, cy)] = 0
#             q.append((cx, cy))

#     while q:
#         x, y = q.popleft()
#         d = dist[(x, y)]
#         for nx, ny in neighbors(x, y):
#             if (nx, ny) not in dist:
#                 dist[(nx, ny)] = d + 1
#                 q.append((nx, ny))

#     # --- helper scores
#     def openness(x, y):
#         return sum(1 for _ in neighbors(x, y))

#     def manhattan(x, y, cx, cy):
#         return abs(x - cx) + abs(y - cy)

#     # Use a representative chaser for the Manhattan tiebreaker:
#     # (if multiple, the max over chasers is a reasonable choice)
#     def manhattan_to_any_chaser(x, y):
#         return max(manhattan(x, y, cx, cy) for cx, cy in chasers)

#     # --- 2) candidate moves (optionally include staying still)
#     candidates = set()
#     if allow_stay and is_floor(*me):
#         candidates.add(me)
#     for nx, ny in neighbors(*me):
#         candidates.add((nx, ny))

#     if not candidates:
#         return None  # nowhere to go

#     # --- 3) score and select
#     scored = []
#     for x, y in candidates:
#         d = dist.get((x, y), float('inf'))             # chaser BFS distance (inf = unreachable)
#         open_score = openness(x, y)                    # more exits is safer
#         manh = manhattan_to_any_chaser(x, y)           # last tiebreaker

#         # Make a sortable distance where "inf" beats any finite distance
#         d_for_sort = 10**18 if isinf(d) else d

#         scored.append(((d_for_sort, open_score, manh), [x, y]))

#     # Sort by: distance desc, openness desc, manhattan desc
#     scored.sort(key=lambda s: (-s[0][0], -s[0][1], -s[0][2]))
#     return scored[0][1]


def frontier_positions(positions):
    """Return all orthogonal neighbors of positions that are not in the set."""
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    result = set()
    for x, y in positions:
        for dx, dy in deltas:
            neighbor = (x + dx, y + dy)
            if neighbor not in positions:
                result.add(neighbor)
    return result

def convert_tile_to_board(game, tile):
    tilex = tile[0] - game.origin[0]
    tiley = tile[1] - game.origin[1]
    return [tilex // game.resolution[0], tiley // game.resolution[1]]


def diagonals(size):
    """Generate diagonals (x, y) for a grid of size [width, height]."""
    width, height = size[0], size[1]
    diags = []
    for s in range(width + height - 1):
        diag = []
        for x in range(width):
            y = s - x
            if 0 <= y < height:
                diag.append([x, y])
        diags.append(diag)
    return diags

def lists_match(list1, list2):
    return set(i == j for i, j in zip(list1, list2)) == { True }

def position_in_bounds(game, position):
    return position[0] >= 0 and position[0] < game.board_size[0] and position[1] >= 0 and position[1] < game.board_size[1]

    
def iterate_over_2D(string_list):

    height = len(string_list)

    y = height

    for i in string_list:
        y -= 1
        x = 0
        for j in i:
            yield (x, y, j)
            x += 1

def sort_objects_by_positions(objects, positions, dx, dy):
    # Pair positions with objects
    paired = list(zip(positions, objects))
    
    # Sort by x-direction
    if dx != 0:
        paired.sort(key=lambda p: p[0][0], reverse=(dx > 0))
    
    # Sort by y-direction
    if dy != 0:
        paired.sort(key=lambda p: p[0][1], reverse=(dy > 0))
    
    # Return only the objects, in the new order
    return [obj for _, obj in paired]


def chunk_list_avg_size(lst, target):
    """
    Split `lst` into chunks whose sizes average ~ `target` (float).
    Sizes alternate between floor(target) and ceil(target) to match the average.
    The final chunk may be smaller, but never larger than ceil(target).
    """
    if target <= 1:
        return chunk_list_avg_size_1(lst, target)
        # Smallest sensible chunk is 1; clamp tiny/invalid targets
        step = 1
        frac = 0.0
    else:
        step = math.floor(target)
        frac = target - step  # fraction of times we should use ceil

    ceil_step = step if frac == 0 else step + 1

    chunks = []
    i = 0
    err = 0.0  # accumulates the fractional part

    while i < len(lst):
        # Decide chunk size: mostly `step`, sometimes `ceil_step`
        if frac == 0:
            k = step
        else:
            err += frac
            if err >= 1.0:
                k = ceil_step
                err -= 1.0
            else:
                k = step

        if k < 1:  # safety
            k = 1

        # Don't overrun the end
        remaining = len(lst) - i
        k = min(k, remaining)

        chunks.append(lst[i:i+k])
        i += k

    if len(chunks[-1]) < target - 1:

        final_chunk = chunks.pop()
        chunks[-1] += final_chunk

    return chunks


import math

def chunk_list_avg_size_1(lst, target):
    """
    Split `lst` into chunks whose sizes average ≈ `target` (float).

    Works for any target > 0, including target < 1.
    - Uses an accumulator so every step's chunk size is either floor(target) or ceil(target).
    - When target < 1, zero-length chunks are emitted to maintain the average (e.g., 1,0,1,0,...).
    - The final chunk will not overrun `lst` (it's clipped to remaining elements).

    Returns: list of slices from `lst`; some may be empty if target < 1.
    """
    if target <= 0:
        raise ValueError("target must be > 0")

    chunks = []
    i = 0                 # number of items already consumed from lst
    acc = 0.0             # accumulates the target rate

    # Keep stepping until we've consumed all elements.
    # Each step decides how many *new* items to consume this round.
    while i < len(lst):
        acc += target
        should_have_eaten = int(math.floor(acc))
        k = should_have_eaten - i            # how many items to take now (can be 0 or more)
        if k < 0:
            k = 0
        # Don't overrun the end
        remaining = len(lst) - i
        k = min(k, remaining)

        # Append the (possibly empty) chunk and advance by k
        chunks.append(lst[i:i+k])
        i += k

        # If k == 0, we still made progress in time (via acc) and will eventually take 1 on a future step.

    return chunks