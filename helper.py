

import math


def iterate_over_2D(string_list):

    height = len(string_list)

    y = height

    for i in string_list:
        y -= 1
        x = 0
        for j in i:
            yield (x, y, j)
            x += 1



def chunk_list_avg_size(lst, target):
    """
    Split `lst` into chunks whose sizes average ~ `target` (float).
    Sizes alternate between floor(target) and ceil(target) to match the average.
    The final chunk may be smaller, but never larger than ceil(target).
    """
    if target <= 1:
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