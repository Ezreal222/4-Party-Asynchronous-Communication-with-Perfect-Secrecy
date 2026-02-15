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

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Test 4-party protocol")
    parser.add_argument("-n", type=int, default=1000, help="pad sequence length")
    parser.add_argument("-d", type=int, default=10, help="gap size")
    parser.add_argument("-e", "--executions", type=int, default=100, help="number of executions")
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    args = parser.parse_args()
    
    n = args.n
    d = args.d
    num_executions = args.executions
    seed = args.seed
    
    print("=" * 60)
    print("4-Party Protocol Testing")
    print("=" * 60)
    print(f"Parameters: n={n}, d={d}, num_executions={num_executions}")
    print()
    
    # Scenario S.1: one randomly chosen party sends
    s1 = run_scenario("S.1", n, d, None, num_executions, seed)
    print(f"Scenario S.1 - 1 randomly chosen party:")
    print(f"  Avg wasted pads: {s1['avg_wasted_pads']:.2f}")
    print(f"  Avg messages sent: {s1['avg_sent_messages']:.2f}")
    print(f"  Max wasted: {s1['max_wasted_pads']}, Min wasted: {s1['min_wasted_pads']}")
    print()    
    
    # Scenario S.2: two randomly chosen parties send
    s2 = run_scenario("S.2", n, d, None, num_executions, seed)
    print(f"Scenario S.2 - 2 randomly chosen parties:")
    print(f"  Avg wasted pads: {s2['avg_wasted_pads']:.2f}")
    print(f"  Avg messages sent: {s2['avg_sent_messages']:.2f}")
    print(f"  Max wasted: {s2['max_wasted_pads']}, Min wasted: {s2['min_wasted_pads']}")
    print()    
    
    # Scenario S.4: All 4 parties send
    s4 = run_scenario("S.4", n, d, [0,1,2,3], num_executions, seed)
    print(f"Scenario S.4 - All 4 parties:")
    print(f"  Avg wasted pads: {s4['avg_wasted_pads']:.2f}")
    print(f"  Avg messages sent: {s4['avg_sent_messages']:.2f}")
    print(f"  Max wasted: {s4['max_wasted_pads']}, Min wasted: {s4['min_wasted_pads']}")
    print()    
    
    # compare to the obvious protocol: (m-1)/m * n wasted pads
    wasted = (4 - 1) / 4 * n
    print("Compare to the obvious protocol:")    
    print(f" Obvious protocol wasted (3n/4): {wasted:.2f}")
    print(f" Our protocol average wasted S.1: {s1['avg_wasted_pads']:.2f}")
    print(f" Our protocol average wasted S.2: {s2['avg_wasted_pads']:.2f}")
    print(f" Our protocol average wasted S.4: {s4['avg_wasted_pads']:.2f}")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()