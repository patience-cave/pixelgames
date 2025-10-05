

def spotlight_changes(n, m, step, cx=None, cy=None):
    # Center defaults to image center
    if cx is None: cx = (m - 1) / 2.0  # x = column index
    if cy is None: cy = (n - 1) / 2.0  # y = row index

    # Initial radius: distance to farthest corner
    corners = [(0,0), (0,m-1), (n-1,0), (n-1,m-1)]
    R0 = max(((x - cx)**2 + (y - cy)**2)**0.5 for y,x in corners)

    # Number of frames until fully black
    Kmax = int((R0 + step - 1e-12) // step)  # ceil(R0/step) without import

    # Prepare buckets of changed pixels for each frame
    changes = [[] for _ in range(Kmax + 1)]  # frames 0..Kmax

    for y in range(n):            # row
        for x in range(m):        # col
            d = ((x - cx)**2 + (y - cy)**2)**0.5
            k = int((R0 - d) // step)  # floor
            if k >= 0 and k <= Kmax:
                changes[k].append((y, x))  # (row, col)

    # Optional: If you want NO change at frame 0 and start changing at frame 1,
    # you can shift by one: return changes[1:], and treat frame index accordingly.
    return changes #, R0, (cx, cy)

