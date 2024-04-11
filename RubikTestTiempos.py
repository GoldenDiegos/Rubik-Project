import random
import heapq
import math
import time

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
        queue = []
        seen = set()
        queue.append((self.copy_cube(self.cube), []))

        while queue:
            current_cube, moves = queue.pop(0)
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

def generate_algorithm_results(algorithm, solver, shuffle_max, heuristic=None):
    times = []
    for _ in range(20):
        start_time = time.time()
        solver.shuffle_cube(shuffle_max)

        if algorithm == "BFS":
            solver.solve_bfs()
        elif algorithm == "Best-First Search":
            solver.solve_best_first_search(heuristic)
        elif algorithm == "A*":
            solver.solve_a_star(heuristic)
        elif algorithm == "Simulated Annealing":
            solver.solve_simulated_annealing()
        end_time = time.time()
        times.append(end_time - start_time)

    average_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    return {'average_time': average_time, 'min_time': min_time, 'max_time': max_time}

if __name__ == '__main__':
    solver = RubikSolver()
    algorithms = ["BFS", "Best-First Search", "A*", "Simulated Annealing"]
    heuristics = [solver.heuristic1, solver.heuristic2, solver.heuristic3]
    shuffle_max_values = [5, 10, 15, 20]
    algorithm_results = {}

    for algorithm in algorithms:
        algorithm_results[algorithm] = {}
        for shuffle_max in shuffle_max_values:
            if algorithm == "Best-First Search" or algorithm == "A*":
                for heuristic in heuristics:
                    algorithm_results[algorithm][(shuffle_max, heuristic.__name__)] = generate_algorithm_results(algorithm, solver, shuffle_max, heuristic)
            else:
                algorithm_results[algorithm][shuffle_max] = generate_algorithm_results(algorithm, solver, shuffle_max)

    for algorithm in algorithms:
        print(f"Results for {algorithm}:")
        if algorithm == "Best-First Search" or algorithm == "A*":
            for shuffle_max, results in algorithm_results[algorithm].items():
                print(f"Shuffle max: {shuffle_max[0]}, Heuristic: {shuffle_max[1]}")
                print(f"Average time: {results['average_time']}")
                print(f"Min time: {results['min_time']}")
                print(f"Max time: {results['max_time']}")
                print()  
        else:
            for shuffle_max, results in algorithm_results[algorithm].items():
                print(f"Shuffle max: {shuffle_max}")
                print(f"Average time: {results['average_time']}")
                print(f"Min time: {results['min_time']}")
                print(f"Max time: {results['max_time']}")
                print()  
