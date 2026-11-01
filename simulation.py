"""
========================================================================================
Petri Net Simulation Engine
========================================================================================
Implements formal Petri Net operational semantics:
  1. Enabling Rule: Transition t is enabled in marking M iff every input place holds >= 1 token.
  2. Firing Rule: Firing an enabled transition t consumes 1 token from each input place
     and produces 1 token in each output place (supporting AND-splits and AND-joins).
========================================================================================
"""

def is_transition_enabled(transition_info: dict, marking: dict) -> bool:
    """
    Returns True iff every input place of the transition contains at least 1 token.

    Parameters:
        transition_info (dict): Transition definition with 'inputs' list of place IDs.
        marking (dict): Current token distribution mapping place IDs to token counts.

    Returns:
        bool: True if transition is enabled, False otherwise.
    """
    return all(marking.get(p, 0) >= 1 for p in transition_info["inputs"])


def fire_transition(transition_info: dict, marking: dict) -> dict:
    """
    Fires the transition, atomically consuming 1 token from each input place
    and depositing 1 token into each output place.

    Parameters:
        transition_info (dict): Transition definition containing 'inputs' and 'outputs'.
        marking (dict): Current token distribution.

    Returns:
        dict: New marking representing the updated token distribution.
    """
    new_marking = dict(marking)
    for p in transition_info["inputs"]:
        new_marking[p] -= 1
    for p in transition_info["outputs"]:
        new_marking[p] = new_marking.get(p, 0) + 1
    return new_marking


if __name__ == "__main__":
    print("Testing Petri Net Simulation Engine...")
    t_test = {"inputs": ["p1", "p2"], "outputs": ["p3"]}
    m_disabled = {"p1": 1, "p2": 0, "p3": 0}
    m_enabled = {"p1": 1, "p2": 1, "p3": 0}

    assert not is_transition_enabled(t_test, m_disabled), "Should not be enabled when p2 lacks tokens"
    assert is_transition_enabled(t_test, m_enabled), "Should be enabled when all inputs have tokens"

    m_fired = fire_transition(t_test, m_enabled)
    assert m_fired == {"p1": 0, "p2": 0, "p3": 1}, f"Unexpected marking after firing: {m_fired}"
    print("✅ Simulation unit test passed successfully.")

