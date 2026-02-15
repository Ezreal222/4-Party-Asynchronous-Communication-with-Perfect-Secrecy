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

def run_scenario(
    scenario_name: str,
    n: int,
    d: int,
    active_parties: list[int] | None,
    num_executions: int = 100,
    seed: int | None = None    
) -> dict:
    """
    Run a scenario multiple times and compute statistics.
    
    Args:
        scenario_name: S.1, S.2, S.4
        n: pad sequence length
        d: gap size
        active_parties: list of parties can send messages, or None for all parties
        num_executions: number of protocol to run
        seed: random seed for reproducibility
    """
    rng = random.Random(seed)
    wasted_pads_list = []
    sent_messages_list = []
    
    for _ in range(num_executions):
        if active_parties is None:
            if scenario_name == "S.1":
                parties = [rng.randint(0, 3)]
            elif scenario_name == "S.2":
                parties = rng.sample(range(4), 2)
            else:
                parties = [0, 1, 2, 3]
        else:
            parties = active_parties
        sent_messages, wasted_pads = run_single_execution(n, d, parties, rng)
        sent_messages_list.append(sent_messages)
        wasted_pads_list.append(wasted_pads)
        
        avg_wasted_pads = sum(wasted_pads_list) / len(wasted_pads_list)
        avg_sent_messages = sum(sent_messages_list) / len(sent_messages_list)
        max_wasted_pads = max(wasted_pads_list)
        min_wasted_pads = min(wasted_pads_list)
    
    return {
        "scenario": scenario_name,
        "n": n,
        "d": d,
        "active_parties": active_parties if active_parties is not None else "random",
        "num_executions": num_executions,
        "avg_wasted_pads": avg_wasted_pads,
        "avg_sent_messages": avg_sent_messages,
        "max_wasted_pads": max_wasted_pads,
        "min_wasted_pads": min_wasted_pads,
        "wasted_pads_list": wasted_pads_list,
    }