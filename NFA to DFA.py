def epsilon_closure(state_set, transitions, epsilon):
    closure = list(state_set)
    stack = list(state_set)
    while stack:
        state = stack.pop()
        key = (state, epsilon)
        if key in transitions:
            for next_state in transitions[key]:
                if next_state not in closure:
                    closure.append(next_state)
                    stack.append(next_state)
    return closure


def nfa_to_dfa(states, alphabet, transitions, start, accept, epsilon='ε'):
    initial = frozenset(epsilon_closure([start], transitions, epsilon))
    dfa_states = []
    dfa_transitions = {}
    dfa_accept = []
    queue = [initial]
    visited = []

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.append(current)
        dfa_states.append(current)

        for s in current:
            if s in accept:
                dfa_accept.append(current)
                break

        for symbol in alphabet:
            if symbol == epsilon:
                continue
            next_states = []
            for state in current:
                key = (state, symbol)
                if key in transitions:
                    for target in transitions[key]:
                        closure = epsilon_closure([target], transitions, epsilon)
                        next_states.extend(closure)

            next_states_set = frozenset(next_states)
            if next_states_set:
                dfa_transitions[(current, symbol)] = next_states_set
                if next_states_set not in visited and next_states_set not in queue:
                    queue.append(next_states_set)

    return dfa_states, dfa_transitions, initial, dfa_accept


def print_dfa(states, transitions, start, accept):
    print("=== DFA States ===")
    for i, s in enumerate(states):
        print(f"State {i}: {list(s)}")

    print("\n=== DFA Transitions ===")
    for key in transitions:
        from_state, symbol = key
        to_state = transitions[key]
        print(f"{list(from_state)} --{symbol}--> {list(to_state)}")

    print("\n=== Start State ===")
    print(list(start))

    print("\n=== Accepting States ===")
    for s in accept:
        print(list(s))


def run_example_1():
    states = {'1', '2'}
    alphabet = {'a', 'b'}
    transitions = {
        ('1', 'a'): {'1'},
        ('1', 'b'): {'2'},
        ('2', 'a'): {'2'},
        ('2', 'b'): {'2'}
    }
    start = '1'
    accept = {'1'}

    dfa_states, dfa_transitions, dfa_start, dfa_accept = nfa_to_dfa(
        states, alphabet, transitions, start, accept
    )
    print("=== DFA from NFA 1 ===")
    print_dfa(dfa_states, dfa_transitions, dfa_start, dfa_accept)


def run_example_2():
    states = {'1', '2', '3'}
    alphabet = {'a', 'b'}
    transitions = {
        ('1', 'ε'): {'2'},
        ('1', 'a'): {'3'},
        ('2', 'a'): {'3'},
        ('2', 'b'): {'3'},
        ('3', 'b'): {'3'}
    }
    start = '1'
    accept = {'2'}

    dfa_states, dfa_transitions, dfa_start, dfa_accept = nfa_to_dfa(
        states, alphabet, transitions, start, accept
    )
    print("=== DFA from NFA 2 (with ε-transitions) ===")
    print_dfa(dfa_states, dfa_transitions, dfa_start, dfa_accept)



run_example_1()
print("\n---------------------------------\n")
run_example_2()