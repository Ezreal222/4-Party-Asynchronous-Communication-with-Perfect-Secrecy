# design of the protocol - Bidirectional d-Gap Protocol
"""
- Parties 0 and 1 use pads from the left end (0, 1, 2, ...)
- Parties 2 and 3 use pads from the right end (n-1, n-2, ...)
- Party 1's range starts at last_used[0] + d + 1 
- Party 2's range ends at last_used[3] - d - 1
- Constraint: left and right "fronts" must not cross
- Wastes at most O(d) pads (better than ((m-1)/m)*n when d << n)
"""
