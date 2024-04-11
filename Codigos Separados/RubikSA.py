import random
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
    energy = solver.solve_simulated_annealing()
    print("Final energy (lower is better):", energy)
    solver.cube.print_cube()
