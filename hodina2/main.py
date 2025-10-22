START_STATE = [" ", "B", "B", " ", "W", "W", " "]
GOAL_STATE = [" ", "W", "W", " ", "B", "B", " "]


def mozne_tahy(current_state):
    next_states = []
    n = len(current_state)

    for i in range(n):
        token = current_state[i]
        if token == " ":
            continue

        for delta in [-1, 1]:
            target = i + delta
            if 0 <= target < n and current_state[target] == " ":
                new_state = current_state[:]
                new_state[target] = token
                new_state[i] = " "
                next_states.append(new_state)

        for delta in [-1, 1]:
            jumped_over = i + delta
            target = i + 2 * delta

            if (
                0 <= jumped_over < n
                and current_state[jumped_over] != " "
                and 0 <= target < n
                and current_state[target] == " "
            ):
                new_state = current_state[:]
                new_state[target] = token
                new_state[i] = " "
                next_states.append(new_state)

    return next_states


def solve():
    fronta = [(START_STATE, [])]

    visited = {tuple(START_STATE)}
    GOAL_TUPLE = tuple(GOAL_STATE)

    while fronta:
        current_list_state, path = fronta.pop(0)
        current_tuple_state = tuple(current_list_state)

        if current_tuple_state == GOAL_TUPLE:
            return path + [current_list_state]

        for next_list_state in mozne_tahy(current_list_state):
            next_tuple_state = tuple(next_list_state)

            if next_tuple_state not in visited:
                visited.add(next_tuple_state)
                fronta.append((next_list_state, path + [current_list_state]))

    return "Řešení nenalezeno!"


solution_path = solve()

print(f"Počáteční stav: {START_STATE}")
print(f"Cílový stav: {GOAL_STATE}")

if isinstance(solution_path, list):
    for i, state in enumerate(solution_path):
        readable_state = "".join(state)
        print(f"Krok {i}:  {readable_state}")
else:
    print(solution_path)
