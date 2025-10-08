

def _get(bits, at): return (bits >> at) & 1

def _get_group(bits, ats):
    return [(bits >> at) & 1 for at in ats]

def _paint(bits, at): 
    bits |= 1 << at
    return bits
def _erase(bits, at, valid=False):
    if valid or _get(bits, at):
        bits -= 1 << at
    return bits
# set can only be 0 or 1
def _set(bits, at, to):
    if _get(bits, at):
        if not to:
            return _erase(bits, at, True)
    else:
        if to:
            return _paint(bits, at)
    return bits

def _valid_position(size, position):
    dimensions = len(size)
    if not dimensions: return False
    for i, value in enumerate(position):
        if i > 0 and i >= dimensions: return False
        if value < 0: return False
        if value >= size[i]: return False
    return True


from functools import reduce
import operator

def _position_to_at(size, position):
    return sum(
        reduce(operator.mul, size[:i], 1) * pos
        for i, pos in enumerate(position)
    )

def _positions_to_ats(size, positions):
    return [_position_to_at(size, position) for position in positions]

class bitgrid:
    def __init__(self, dimension, rep=0):
        self.size = dimension
        self.bits = rep

    def paint(self, at):
        self.bits = _paint(self.bits, at)

    def erase(self, at):
        self.bits = _erase(self.bits, at)

    def get(self, at):
        return _get(self.bits, at)

    def group_get(self, ats):
        return _get_group(self.bits, ats)

    # returns true if modified
    def set(self, at, to):
        oldbits = self.bits
        self.bits = _set(self.bits, at, to)
        return self.bits != oldbits

    def __str__(self): return f"{self.bits}"
    def __repr__(self): return f"bitgrid({self.bits})"

class grid:
    def __init__(self, dimension, symbols):
        """
        dimension : the dimension of the grid (i.e. 8x8)
        symbols : the number of different states a pixel can be
        """

        self.size = dimension

        self.bitgrids = []
        self.symbols = symbols

        while symbols:
            symbols >>= 1
            self.bitgrids.append(bitgrid(dimension))

    def location_exists(self, position):
        return _valid_position(self.size, position)

    def group_get(self, positions):
        size = self.size
        ats = _positions_to_ats(size, positions)

        bitgrids = self.bitgrids  # local
        n = len(ats)
        symbols = [0] * n

        for i, grid in enumerate(bitgrids):
            bits = grid.group_get(ats)     # list/iter of 0/1 for each position
            w = 1 << i                     # precompute shift once
            # in-place accumulation (no new list each round)
            for idx in range(n):
                symbols[idx] += bits[idx] * w
                # or: symbols[idx] |= (bits[idx] << i)  # if bits are strictly {0,1}
        return symbols

    def group_set(self, positions, to):
        for position in positions:
            self.set(position, to)

    # assuming position exists
    def get(self, position):
        at = _position_to_at(self.size, position)
        symbol = 0
        
        for i, bitgrid in enumerate(self.bitgrids):
            symbol += bitgrid.get(at) << i
        
        assert(symbol < self.symbols)

        return symbol

    # return True means modifications were made
    def set(self, position, to):
        if to >= self.symbols: return False
        if not self.location_exists(position): return False

        at = _position_to_at(self.size, position)

        bits = []
        for i in range(len(self.bitgrids)):
            bits.append(to & 1)
            to >>= 1

        modified = False
        for bit, bitgrid in zip(bits, self.bitgrids):
            o = bitgrid.set(at, bit)
            modified = o or modified

        return modified

    def __str__(self):
        return f"{[i.bits for i in self.bitgrids]}"

    def __repr__(self):
        return f"{[i.bits for i in self.bitgrids]}"
