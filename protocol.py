# design of the protocol - Bidirectional d-Gap Protocol
"""
- Parties 0 and 1 use pads from the left end (0, 1, 2, ...)
- Parties 2 and 3 use pads from the right end (n-1, n-2, ...)
- Party 1's range starts at last_used[0] + d + 1 
- Party 2's range ends at last_used[3] - d - 1
- Constraint: left and right "fronts" must not cross
- Wastes at most O(d) pads (better than ((m-1)/m)*n when d << n)
"""

from dataclasses import dataclass, field
from typing import Optional

# shared state for the protocol
@dataclass
class ProtocolState:
    n: int # Pad sequence length
    d: int # Gap size
    # last[i] = last used pad by party i     
    last_used: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.last_used:
            self.last_used = [-1, -1, self.n, self.n]
    
    def copy(self) -> 'ProtocolState':
        return ProtocolState(self.n, self.d, self.last_used.copy())
    