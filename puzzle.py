import tkinter as tk
import random
import numpy as np
import heapq


# Game board setup
class Game2048:

    def __init__(self, size=4):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.size)
                       for j in range(self.size) if self.grid[i, j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i, j] = 4 if random.random() > 0.9 else 2

    def slide_left(self):
        moved = False
        for row in range(self.size):
            original_row = self.grid[row]
            non_zero = original_row[original_row != 0]
            new_row = np.zeros_like(original_row)
            if len(non_zero) > 0:
                merged = False
                j = 0
                for i in range(len(non_zero)):
                    if not merged and j > 0 and new_row[j - 1] == non_zero[i]:
                        new_row[j - 1] *= 2
                        self.score += new_row[j - 1]
                        merged = True
                    else:
                        new_row[j] = non_zero[i]
                        j += 1
                        merged = False
            if not np.array_equal(original_row, new_row):
                moved = True
            self.grid[row] = new_row
        return moved

    def rotate_board(self):
        self.grid = np.rot90(self.grid)

    def move(self, direction):
        moved = False
        if direction == 'left':
            moved = self.slide_left()
        elif direction == 'right':
            self.rotate_board()
            self.rotate_board()
            moved = self.slide_left()
            self.rotate_board()
            self.rotate_board()
        elif direction == 'up':
            self.rotate_board()
            self.rotate_board()
            self.rotate_board()
            moved = self.slide_left()
            self.rotate_board()
        elif direction == 'down':
            self.rotate_board()
            moved = self.slide_left()
            self.rotate_board()
            self.rotate_board()
            self.rotate_board()

        if moved:
            self.add_new_tile()
        return moved

    def is_game_over(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == 0:
                    return False
                if i < self.size - 1 and self.grid[i, j] == self.grid[i + 1,
                                                                      j]:
                    return False
                if j < self.size - 1 and self.grid[i, j] == self.grid[i,
                                                                      j + 1]:
                    return False
        return True


# A* Algorithm for 2048 Solver
class AStar2048:

    def __init__(self, game):
        self.game = game

    def heuristic(self, grid):
        # A heuristic function to guide A* search (minimize empty tiles)
        empty_cells = np.count_nonzero(grid == 0)
        return empty_cells

    def get_best_move(self):
        best_move = None
        best_heuristic = float('-inf')
        for move in ['left', 'right', 'up', 'down']:
            new_game = Game2048()
            new_game.grid = np.copy(self.game.grid)
            if new_game.move(move):
                h_value = self.heuristic(new_game.grid)
                if h_value > best_heuristic:
                    best_heuristic = h_value
                    best_move = move
        return best_move


# Tkinter GUI for 2048 Game
class Game2048GUI:

    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("2048 Game")
        self.grid_labels = [[None for _ in range(self.game.size)]
                            for _ in range(self.game.size)]
        self.build_grid()
        self.update_grid()

        self.ai_playing = True  # Automatically start AI mode
        self.run_ai()

    def build_grid(self):
        for i in range(self.game.size):
            for j in range(self.game.size):
                label = tk.Label(self.root,
                                 text="",
                                 font=('Arial', 24),
                                 width=4,
                                 height=2)
                label.grid(row=i, column=j, padx=5, pady=5)
                self.grid_labels[i][j] = label

    def update_grid(self):
        for i in range(self.game.size):
            for j in range(self.game.size):
                value = self.game.grid[i, j]
                self.grid_labels[i][j].config(
                    text=str(value) if value != 0 else "",
                    bg=self.get_color(value))
        self.root.update_idletasks()

    def get_color(self, value):
        colors = {
            0: "#CCC0B3",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E"
        }
        return colors.get(value, "#3C3A32")

    def run_ai(self):
        if self.game.is_game_over():
            self.root.title("Game Over!")
            return
        solver = AStar2048(self.game)
        best_move = solver.get_best_move()
        if best_move:
            self.game.move(best_move)  # Apply AI move
            self.update_grid()

        # Continue AI playing if not over, run every 500 milliseconds
        self.root.after(500, self.run_ai)

    def run(self):
        self.root.mainloop()


# Run the Game
game = Game2048()
gui = Game2048GUI(game)
gui.run()