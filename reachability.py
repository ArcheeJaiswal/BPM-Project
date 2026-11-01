"""
========================================================================================
State-Space Reachability & Path Discovery Engine
========================================================================================
Implements state-space exploration via Depth-First Search (DFS) over the
Petri Net's Reachability Graph:
  - Explores all complete firing sequences from initial marking M0 to terminal sink place.
  - Handles concurrent branch interleavings (A -> B vs B -> A).
  - Handles bounded cyclic rework loops with configurable visit depth (max_visits=2).
  - Guarantees termination and unique trace deduplication.
========================================================================================
"""

from typing import List, Tuple, Dict, Any
from simulation import is_transition_enabled, fire_transition


def discover_all_execution_paths(petri_net: Dict[str, Any], max_visits: int = 2) -> List[List[Tuple[str, str, str]]]:
    """
    Discovers all complete execution paths from initial marking M0
    to the final sink place p_end.

    Parameters:
        petri_net (dict): Petri net specification containing:
            - 'transitions': Dict of transition ID to info
            - 'initial_marking': Initial token distribution dict
            - 'final_place': ID of the terminal sink place
        max_visits (int): Maximum times any specific marking state can be visited
            along a single exploration path branch (allows bounded loop exploration).

    Returns:
        List[List[Tuple[str, str, str]]]: A list of paths, where each path is an ordered
        list of transition tuples: (transition_id, label, transition_type).
    """
    paths = []
    final_place = petri_net["final_place"]

    def dfs(current_marking: Dict[str, int], current_sequence: List[Tuple[str, str, str]], visited_counts: Dict[Tuple, int]):
        # Termination condition: Token has arrived in the terminal sink place
        if current_marking.get(final_place, 0) >= 1:
            paths.append(list(current_sequence))
            return

        state_key = tuple(sorted(current_marking.items()))
        count = visited_counts.get(state_key, 0)
        if count >= max_visits:
            return

        new_counts = dict(visited_counts)
        new_counts[state_key] = count + 1

        # Explore all enabled transitions from the current marking
        for t_id, t_info in petri_net["transitions"].items():
            if is_transition_enabled(t_info, current_marking):
                next_marking = fire_transition(t_info, current_marking)
                dfs(
                    next_marking,
                    current_sequence + [(t_id, t_info["label"], t_info.get("type", "standard"))],
                    new_counts
                )

    initial_marking = dict(petri_net["initial_marking"])
    dfs(initial_marking, [], {})

    # Deduplicate unique transition sequences
    unique_paths = []
    seen = set()
    for p in paths:
        k = tuple(x[0] for x in p)
        if k not in seen:
            seen.add(k)
            unique_paths.append(p)

    return unique_paths


if __name__ == "__main__":
    print("Testing Reachability Engine...")
    test_net = {
        "final_place": "p_end",
        "initial_marking": {"p_start": 1, "p_mid": 0, "p_end": 0},
        "transitions": {
            "t1": {"label": "Task 1", "inputs": ["p_start"], "outputs": ["p_mid"]},
            "t2": {"label": "Task 2", "inputs": ["p_mid"], "outputs": ["p_end"]}
        }
    }
    found = discover_all_execution_paths(test_net)
    assert len(found) == 1, f"Expected 1 path, got {len(found)}"
    assert found[0][0][0] == "t1" and found[0][1][0] == "t2"
    print("✅ Reachability engine unit test passed successfully.")

