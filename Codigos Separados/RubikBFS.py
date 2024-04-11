import random
from collections import deque

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

if __name__ == '__main__':
    solver = RubikSolver()
    solver.shuffle_cube(10)  
    solution = solver.solve_bfs()
    print("Solution found:", solution)
    solver.cube.print_cube()
