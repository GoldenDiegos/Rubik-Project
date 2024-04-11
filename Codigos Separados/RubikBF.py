import random
import heapq

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

if __name__ == '__main__':
    solver = RubikSolver()
    solver.shuffle_cube(10)  
    heuristics = [solver.heuristic1, solver.heuristic2, solver.heuristic3]
    for heuristic in heuristics:
        solution = solver.solve_best_first_search(heuristic)
        print(f"Solución con la heurística {heuristics.index(heuristic) + 1}:", solution)
        solver.cube.print_cube()
