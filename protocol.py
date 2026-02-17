# design of the protocol - Split-Half d-Gap Protocol
"""
Split the pad sequence into two equal halves:
- First half [0, n/2): Parties 0 and 1 (like Alice and Bob)
  - Party 0 uses pads from left: 0, 1, 2, ...
  - Party 1 uses pads from right: n/2-1, n/2-2, ...
  - They maintain a gap of at least d between them

- Second half [n/2, n): Parties 2 and 3 (like Alice and Bob)
  - Party 2 uses pads from left: n/2, n/2+1, ...
  - Party 3 uses pads from right: n-1, n-2, ...
  - They maintain a gap of at least d between them
"""

from dataclasses import dataclass, field
from typing import Optional

# shared state for the protocol
@dataclass
class ProtocolState:
    n: int  # Pad sequence length
    d: int  # Gap size
    # last[i] = last used pad by party i
    # Party 0: starts at -1, moves right
    # Party 1: starts at n/2, moves left
    # Party 2: starts at n/2-1, moves right
    # Party 3: starts at n, moves left
    last_used: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.last_used:
            mid = self.n // 2
            self.last_used = [-1, mid, mid - 1, self.n]

    def copy(self) -> 'ProtocolState':
        return ProtocolState(self.n, self.d, self.last_used.copy())


class FourPartyProtocol:
    def __init__(self, n: int, d: int):
        if d >= n // 4:
            raise ValueError("Gap size must be less than a quarter of the sequence length")
        self.n = n
        self.d = d
        self.mid = n // 2  # boundary between the two halves
        self.state = ProtocolState(n=n, d=d)

    # get the next pad for party to use, or None if cannot send securely
    def get_next_pad(self, party_id: int) -> Optional[int]:
        s = self.state

        if party_id == 0:
            # Party 0: uses first half from left (0, 1, 2, ...)
            # Must maintain gap d from Party 1's position
            next_pad = s.last_used[0] + 1
            # Cannot cross into Party 1's territory (need gap of d)
            if next_pad >= s.last_used[1] - self.d:
                return None
            return next_pad

        elif party_id == 1:
            # Party 1: uses first half from right (mid-1, mid-2, ...)
            # Must maintain gap d from Party 0's position
            next_pad = s.last_used[1] - 1
            # Cannot cross into Party 0's territory (need gap of d)
            if next_pad <= s.last_used[0] + self.d:
                return None
            return next_pad

        elif party_id == 2:
            # Party 2: uses second half from left (mid, mid+1, ...)
            # Must maintain gap d from Party 3's position
            next_pad = s.last_used[2] + 1
            # Cannot cross into Party 3's territory (need gap of d)
            if next_pad >= s.last_used[3] - self.d:
                return None
            if next_pad < 0:
                return None
            return next_pad

        elif party_id == 3:
            # Party 3: uses second half from right (n-1, n-2, ...)
            # Must maintain gap d from Party 2's position
            next_pad = s.last_used[3] - 1
            # Cannot cross into Party 2's territory (need gap of d)
            if next_pad <= s.last_used[2] + self.d:
                return None
            if next_pad < self.mid:
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
        s = self.state
        total = 0

        # First half: Party 0 uses [0, last_used[0]], Party 1 uses [last_used[1], mid-1]
        # Party 0's contribution
        if s.last_used[0] >= 0:
            total += s.last_used[0] + 1  # pads 0 to last_used[0]

        # Party 1's contribution
        if s.last_used[1] < self.mid:
            total += self.mid - s.last_used[1]  # pads last_used[1] to mid-1

        # Second half: Party 2 uses [mid, last_used[2]], Party 3 uses [last_used[3], n-1]
        # Party 2's contribution
        if s.last_used[2] >= self.mid:
            total += s.last_used[2] - self.mid + 1  # pads mid to last_used[2]

        # Party 3's contribution
        if s.last_used[3] < self.n:
            total += self.n - s.last_used[3]  # pads last_used[3] to n-1

        return total

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
    print(f"Total pads n: {p.n}, Gap d: {p.d}, Target Wasted pads: {((4-1)/4)*p.n}")
    print(f"Total used pads: {p.get_total_used()}, Wasted pads: {p.get_wasted_pads()}")