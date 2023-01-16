import random

def move_random(start_gate, end_gate, board):
    while start_gate.x != end_gate.x and start_gate.y != end_gate.y and start_gate.z != end_gate.z:
        # board aantal lijnen die kruisen bijhouden i.p.v. boolean
        change = random.choice([start_gate.x, start_gate.y, start_gate.z])
        # check voor out of bounds?
        change += random.choice([-1, 1])

        node_name = width * start_gate.x + start_gate.y + (length * width) * start_gate.z
        board[node_name].crossings += 1



