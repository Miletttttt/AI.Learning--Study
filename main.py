import random
import time

width = 5
height = 5

# memória da IA
q_table = {}

actions = [0, 1, 2, 3]  # cima, baixo, esquerda, direita

# estado MELHOR (distância)
def get_state(agent, food):
    dx = food[0] - agent[0]
    dy = food[1] - agent[1]
    return (dx, dy)

def choose_action(state, epsilon=0.2):
    if state not in q_table:
        q_table[state] = [0, 0, 0, 0]

    # exploração
    if random.random() < epsilon:
        return random.choice(actions)

    # melhor ação (com desempate aleatório)
    max_value = max(q_table[state])
    best = [i for i, v in enumerate(q_table[state]) if v == max_value]
    return random.choice(best)

def move(agent, action):
    x, y = agent
    old = [x, y]

    if action == 0: y -= 1
    if action == 1: y += 1
    if action == 2: x -= 1
    if action == 3: x += 1

    x = max(0, min(width - 1, x))
    y = max(0, min(height - 1, y))

    new = [x, y]
    hit_wall = (new == old)

    return new, hit_wall

def print_map(agent, food):
    print("\n" * 3)
    for y in range(height):
        row = ""
        for x in range(width):
            if [x, y] == agent:
                row += "A "
            elif [x, y] == food:
                row += "F "
            else:
                row += ". "
        print(row)
    print("Agent:", agent, "Food:", food)

# =====================
# TREINO
# =====================

for episode in range(3000):

    agent = [random.randint(0, 4), random.randint(0, 4)]
    food = [random.randint(0, 4), random.randint(0, 4)]

    last_positions = []

    for step in range(50):

        state = get_state(agent, food)
        action = choose_action(state)

        new_agent, hit_wall = move(agent, action)

        # recompensa base
        if new_agent == food:
            reward = 10
        else:
            reward = -1

        # bateu na parede (ESSENCIAL)
        if hit_wall:
            reward -= 8

        # anti-loop
        last_positions.append(tuple(new_agent))
        if len(last_positions) > 10:
            last_positions.pop(0)

        if last_positions.count(tuple(new_agent)) > 3:
            reward -= 5

        new_state = get_state(new_agent, food)

        if new_state not in q_table:
            q_table[new_state] = [0, 0, 0, 0]

        # aprendizado
        lr = 0.1
        gamma = 0.9

        q_table[state][action] += lr * (
            reward + gamma * max(q_table[new_state]) - q_table[state][action]
        )

        agent = new_agent

        if reward >= 10:
            break

# =====================
# TESTE VISUAL
# =====================

agent = [random.randint(0, 4), random.randint(0, 4)]
food = [random.randint(0, 4), random.randint(0, 4)]

while True:
    state = get_state(agent, food)
    action = choose_action(state, epsilon=0)

    agent, _ = move(agent, action)

    print_map(agent, food)
    time.sleep(0.3)

    if agent == food:
        print("ACHOU!")
        break