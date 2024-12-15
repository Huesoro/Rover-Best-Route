import numpy as np
import random
import math

class ViajeMarte:
    def __init__(self):
        self.mars_map = np.load('crater_map.npy')
        self.rows, self.cols = self.mars_map.shape
        self.escala = 10.045

    def get_possible_actions(self, state):
        x, y = state
        possible_actions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                    depth_difference = abs(self.mars_map[x, y] - self.mars_map[new_x, new_y])
                    if depth_difference <= 2.0:
                        possible_actions.append((new_x, new_y))
        return possible_actions

    def heuristic(self, state):
        x, y = state
        n_r, n_c = self.rows, self.cols
        r = n_r - round(y / self.escala)
        c = n_c - round(x / self.escala)
        return np.abs(self.mars_map[r, c] - np.min(self.mars_map))

    def Codiciosa(self, initial_position):
        current_state = initial_position
        path = [current_state]
        visited = []
        print("Búsqueda Codiciosa:")
        i = 0
        while i < 70:
            possible_actions = self.get_possible_actions(current_state)
            if not possible_actions:
                break

            best_action = None
            best_heuristic = float('inf')
            for action in possible_actions:
                heuristic_value = self.heuristic(action)
                if heuristic_value < best_heuristic:
                    best_heuristic = heuristic_value
                    best_action = action
            visited.append(current_state)

            if current_state in visited:
                break

            current_state = best_action
            path.append(current_state)
            print("Posición:", current_state)
            i = i+1

        return current_state, path



    def RecocidoSimulado(self, initial_position, t=1000, cooling_rate=0.99):
        current_state = initial_position
        path = [current_state]
        print("Recocido simulado: ")
        while t > 1:
            possible_actions = self.get_possible_actions(current_state)
            if not possible_actions:
                break
            next_state = random.choice(possible_actions)
            energy_delta = self.heuristic(next_state) - self.heuristic(current_state)

            if energy_delta < 0 or random.random() < np.exp(-energy_delta / t):
                current_state = next_state
                path.append(current_state)

            t *= cooling_rate
            print("Posición:", current_state)

        return current_state, path

# Ejemplo de uso:
if __name__ == "__main__":
    viaje_marte = ViajeMarte()
    initial_position = (round(3350 / viaje_marte.escala), round(5800 / viaje_marte.escala))

    goal_position_greedy, path_greedy = viaje_marte.Codiciosa(initial_position)
    print("Búsqueda Codiciosa:")
    print("Posición inicial:", initial_position)
    print("Posición final:", goal_position_greedy)
    print("Profundidad:", viaje_marte.mars_map[goal_position_greedy])
    print("\n")

    goal_position_sa, path_sa = viaje_marte.RecocidoSimulado(initial_position)
    print("Recocido Simulado:")
    print("Posición inicial:", initial_position)
    print("Posición final:", goal_position_sa)
    print("Profundidad:", viaje_marte.mars_map[goal_position_sa])
    print("\n")
    
for i in range(5):
    initial_position = (random.randint(300, 350), random.randint(550, 600))

    goal_position_greedy, path_greedy = viaje_marte.Codiciosa(initial_position)
    print("Búsqueda Codiciosa:")
    print("Posición inicial:", initial_position)
    print("Posición final:", goal_position_greedy)
    print("Profundidad:", viaje_marte.mars_map[goal_position_greedy])
    print("\n")

    goal_position_sa, path_sa = viaje_marte.RecocidoSimulado(initial_position)
    print("Recocido Simulado:")
    print("Posición inicial:", initial_position)
    print("Posición final:", goal_position_sa)
    print("Profundidad:", viaje_marte.mars_map[goal_position_sa])
    print("\n")
