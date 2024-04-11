import random
import heapq
from collections import deque
import math

class RubikCube:
    def __init__(self):
        self.faces = {
            'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'R': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']]
        }

    def rotate_face(self, face):
        face[:] = [list(row) for row in zip(*face[::-1])]

    def rotate(self, move):
        self.rotate_face(self.faces[move])

    def print_cube(self):
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            print(f"{face}:")
            for row in self.faces[face]:
                print(' '.join(row))
            print()

class RubikSolver:
    def __init__(self):
        self.cube = RubikCube()

    def shuffle_cube(self, num_moves=20):
        moves = ['F', 'B', 'U', 'D', 'L', 'R']
        for _ in range(num_moves):
            move = random.choice(moves)
            self.cube.rotate(move)

    def is_solved(self, cube):
        for face in cube.faces:
            if not all(color == cube.faces[face][0][0] for row in cube.faces[face] for color in row):
                return False
        return True

    def copy_cube(self, cube):
        new_cube = RubikCube()
        new_cube.faces = {face: [row[:] for row in cube.faces[face]] for face in cube.faces}
        return new_cube

    def heuristic1(self, cube):
        # Heurística 1: Cuenta el número de caras resueltas
        solved_faces = sum(1 for face in cube.faces if all(cube.faces[face][0][0] == cell for row in cube.faces[face] for cell in row))
        return -solved_faces

    def heuristic2(self, cube):
        # Heurística 2: Cuenta el número de colores únicos en las caras
        unique_colors = len(set(color for face in cube.faces for row in cube.faces[face] for color in row))
        return -unique_colors

    def heuristic3(self, cube):
        # Heurística 3: Cuenta el número de colores repetidos en las caras
        repeated_colors = sum(1 for face in cube.faces for row in cube.faces[face] for color in row if row.count(color) > 1)
        return -repeated_colors

    def solve_bfs(self):
        queue = deque([(self.copy_cube(self.cube), [])])
        seen = set()
        while queue:
            current_cube, moves = queue.popleft()
            if self.is_solved(current_cube):
                return moves
            for move in ['F', 'B', 'U', 'D', 'L', 'R']:
                new_cube = self.copy_cube(current_cube)
                new_cube.rotate(move)
                cube_state = str(new_cube.faces)
                if cube_state not in seen:
                    seen.add(cube_state)
                    queue.append((new_cube, moves + [move]))

    def solve_best_first_search(self, heuristic):
        priority_queue = []
        initial_state = (heuristic(self.cube), self.copy_cube(self.cube), [])
        heapq.heappush(priority_queue, initial_state)
        seen = set()

        while priority_queue:
            _, current_cube, moves = heapq.heappop(priority_queue)
            if self.is_solved(current_cube):
                return moves
            for move in ['F', 'B', 'U', 'D', 'L', 'R']:
                new_cube = self.copy_cube(current_cube)
                new_cube.rotate(move)
                cube_state = str(new_cube.faces)
                if cube_state not in seen:
                    seen.add(cube_state)
                    heapq.heappush(priority_queue, (heuristic(new_cube), new_cube, moves + [move]))

    def solve_a_star(self, heuristic):
        open_set = []
        initial_state = (heuristic(self.cube), 0, self.copy_cube(self.cube), [])
        heapq.heappush(open_set, initial_state)
        seen = set()

        while open_set:
            _, cost, current_cube, moves = heapq.heappop(open_set)
            if self.is_solved(current_cube):
                return moves
            for move in ['F', 'B', 'U', 'D', 'L', 'R']:
                new_cube = self.copy_cube(current_cube)
                new_cube.rotate(move)
                cube_state = str(new_cube.faces)
                if cube_state not in seen:
                    seen.add(cube_state)
                    new_cost = cost + 1
                    heapq.heappush(open_set, (heuristic(new_cube) + new_cost, new_cost, new_cube, moves + [move]))

    def solve_simulated_annealing(self, temp=30, cooling_rate=0.99, stop_temp=0.1):
        current_cube = self.copy_cube(self.cube)
        current_energy = self.calculate_energy(current_cube)
        best_cube = current_cube
        best_energy = current_energy
        
        while temp > stop_temp:
            next_cube = self.copy_cube(current_cube)
            self.make_random_move(next_cube)
            next_energy = self.calculate_energy(next_cube)
            
            if next_energy < current_energy:
                current_cube, current_energy = next_cube, next_energy
                if current_energy < best_energy:
                    best_cube, best_energy = current_cube, current_energy
            else:
                if random.random() < math.exp((current_energy - next_energy) / temp):
                    current_cube, current_energy = next_cube, next_energy
            
            temp *= cooling_rate
        
        self.cube = best_cube
        return best_energy

    def calculate_energy(self, cube):
        energy = 0
        for face in cube.faces:
            target_color = cube.faces[face][0][0]
            for row in cube.faces[face]:
                for color in row:
                    if color != target_color:
                        energy += 1
        return energy

    def make_random_move(self, cube):
        move = random.choice(['F', 'B', 'U', 'D', 'L', 'R'])
        cube.rotate(move)

if __name__ == '__main__':
    solver = RubikSolver()
    solver.shuffle_cube(10)

    print("Resuelto con BFS:")
    bfs_solution = solver.solve_bfs()
    print("Resuelto con:", bfs_solution)
    solver.cube.print_cube()

    print("\Resuelto con Best First Search y Heurística 1:")
    best_first_search_solution1 = solver.solve_best_first_search(solver.heuristic1)
    print("Resuelto con:", best_first_search_solution1)
    solver.cube.print_cube()

    print("\nResuelto con Best First Search y Heurística 2:")
    best_first_search_solution2 = solver.solve_best_first_search(solver.heuristic2)
    print("Resuelto con:", best_first_search_solution2)
    solver.cube.print_cube()

    print("\nResuelto con Best First Search y Heurística 3:")
    best_first_search_solution3 = solver.solve_best_first_search(solver.heuristic3)
    print("SResuelto con:", best_first_search_solution3)
    solver.cube.print_cube()

    print("\nResuelto con A* Search y Heurística1:")
    a_star_solution1 = solver.solve_a_star(solver.heuristic1)
    print("Resuelto con:", a_star_solution1)
    solver.cube.print_cube()

    print("\nResuelto con A* Search y Heurística 2:")
    a_star_solution2 = solver.solve_a_star(solver.heuristic2)
    print("Resuelto con:", a_star_solution2)
    solver.cube.print_cube()

    print("\nResuelto con A* Search y Heurística3:")
    a_star_solution3 = solver.solve_a_star(solver.heuristic3)
    print("Resuelto con:", a_star_solution3)
    solver.cube.print_cube()

    print("\nResuelto con Simulated Annealing:")
    simulated_annealing_energy = solver.solve_simulated_annealing()
    print("Final energy (lower is better):", simulated_annealing_energy)
    solver.cube.print_cube()
