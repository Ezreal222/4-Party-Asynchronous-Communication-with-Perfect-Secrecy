"""
Testing program for 4-Party Asynchronous Communication Protocol
- (Scenario (S.x)): only x, randomly chosen, parties repeatedly send L-length messages
- x = {1,2,4}
- Report average wasted pads 
"""

import random
from protocol import FourPartyProtocol

def run_single_execution(
    n: int,
    d: int,
    active_parties: list[int],
    rng: random.Random
) -> tuple[int, int]:
    """
    Run one protocol execution until at least one party cannot send.
    
    Returns:
        (total_messages_sent, wasted_pads)
    """
    protocol = FourPartyProtocol(n=n, d=d)
    total_messages_sent = 0
    
    while True:
        # randomly choose a party to send
        party_id = rng.choice(active_parties)
        if protocol.send(party_id) is None:
            break
        total_messages_sent += 1
        
    wasted_pads = protocol.get_wasted_pads()
    return total_messages_sent, wasted_pads

