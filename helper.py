

import math

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