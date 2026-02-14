# design of the protocol - Bidirectional d-Gap Protocol
"""
- Parties 0 and 1 use pads from the left end (0, 1, 2, ...)
- Parties 2 and 3 use pads from the right end (n-1, n-2, ...)
- Party 1's range starts at last_used[0] + d + 1 
- Party 2's range ends at last_used[3] - d - 1
- Constraint: left and right must not cross (gap of at least d)
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

class FourPartyProtocol:
    def __init__(self, n: int, d: int):
        if d >= n:
            raise ValueError("Gap size must be less than sequence length")
        self.n = n
        self.d = d
        self.state = ProtocolState(n=n, d=d)

    # rightmost boundary for left-side usage (for right parties to check)
    def _get_left_boundary(self) -> int:
        return max(self.state.last_used[0], self.state.last_used[1])
    
    # leftmost boundary for right-side usage (for left parties to check)
    def _get_right_boundary(self) -> int:
        return min(self.state.last_used[2], self.state.last_used[3])
    
    # get the next pad for party to use, or None if cannot send securely
    def get_next_pad(self, party_id: int) -> Optional[int]:
        s = self.state
        if party_id == 0:
            next_pad = s.last_used[0] + 1
            right_boundary = self._get_right_boundary()
            if next_pad >= right_boundary - self.d:
                return None
            return next_pad
        elif party_id == 1:
            next_pad = max(s.last_used[0] + self.d + 1, s.last_used[1] + 1)
            right_boundary = self._get_right_boundary()
            if next_pad >= right_boundary - self.d:
                return None
            return next_pad
        elif party_id == 2:
            next_pad = min(s.last_used[2] -1, s.last_used[3] - self.d - 1)
            left_boundary = self._get_left_boundary()
            if next_pad <= left_boundary + self.d:
                return None
            if next_pad < 0:
                return None
            return next_pad
        elif party_id == 3:
            next_pad = s.last_used[3] - 1
            left_boundary = self._get_left_boundary()
            if next_pad <= left_boundary + self.d:
                return None
            if next_pad < 0:
                return None
            return next_pad
        else:
            raise ValueError("Invalid party ID")
        
    # party sends a message, return pad index used, or None if cannot send
    def send(self, party_id: int) -> Optional[int]:
        pad = self.get_next_pad(party_id)
        if pad is None:
            return None
        self.state.last_used[party_id] = pad
        return pad
    
    # count total pads used by all parties
    def get_total_used(self) -> int:
        used = set()
        s = self.state
        if s.last_used[0] >= 0:
            for p in range(0, s.last_used[0] + 1):
                used.add(p)
        if s.last_used[1] >= 0:
            start = s.last_used[0] + self.d + 1
            for p in range(start, s.last_used[1] + 1):
                used.add(p)
        if s.last_used[2] < self.n:
            end = s.last_used[3] - self.d 
            for p in range(s.last_used[2], end):
                used.add(p)
        if s.last_used[3] < self.n:
            for p in range(s.last_used[3], self.n):
                used.add(p)
        return len(used)
    def get_wasted_pads(self) -> int:
        return self.n - self.get_total_used()
    
# Test: only party 0 sends until protocol ends
if __name__ == "__main__":
    p = FourPartyProtocol(n=100, d=5)
    count = 0
    while (pad := p.send(0)) is not None:
        count += 1
        if count <= 5:
            print(f"Party 0 sent with pad {pad}")
    print(f"... (party 0 sent {count} messages total)")
    print(f"Total used: {p.get_total_used()}, Wasted: {p.get_wasted_pads()}")