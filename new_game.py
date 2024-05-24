import tkinter as tk
import random


class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")

        # Header for the game
        self.header = tk.Label(master, text="2048", bg='azure3', font=("arial", 40, "bold"))
        self.header.pack(side=tk.TOP, pady=10)

        # Subtitle for the game
        self.subtitle = tk.Label(master, text="GAME GUIDE", bg='azure3', font=("arial", 20))
        self.subtitle.pack(side=tk.TOP, pady=5)

        self.game_area = tk.Frame(master, bg='azure3')
        self.grid()
        self.master.bind("<Key>", self.link_keys)
        self.commands = {
            'w': self.move_up, 's': self.move_down, 'a': self.move_left, 'd': self.move_right
        }
        self.reset_game()

    def reset_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid_cells()

    def grid(self):
        self.grid_cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(self.game_area, bg='azure4', width=100, height=100)
                cell.grid(row=i, column=j, padx=7, pady=7)
                t = tk.Label(master=cell, text='', bg='azure4', justify=tk.CENTER, font=("arial", 22, "bold"), width=4,
                             height=2)
                t.grid()
                row.append(t)
            self.grid_cells.append(row)
        self.game_area.pack(pady=10)

    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    self.grid_cells[i][j].configure(text='', bg='azure4')
                else:
                    self.grid_cells[i][j].configure(text=str(self.matrix[i][j]), bg=self.get_color(self.matrix[i][j]),
                                                    fg='white')
        self.master.update_idletasks()

    def get_color(self, value):
        colors = {
            2: '#eee4da', 4: '#ede0c8', 8: '#f2b179', 16: '#f59563',
            32: '#f67c5f', 64: '#f65e3b', 128: '#edcf72', 256: '#edcc61',
            512: '#edc850', 1024: '#edc53f', 2048: '#edc22e'
        }
        return colors.get(value, 'black')

    def link_keys(self, event):
        key = event.char
        if key in self.commands:
            self.commands[key]()
            self.add_new_tile()
            self.update_grid_cells()
            if self.game_over():
                self.grid_cells[1][1].configure(text="Game", bg='red')
                self.grid_cells[1][2].configure(text="Over", bg='red')

    def move_left(self):
        new_matrix = []
        for row in self.matrix:
            new_row = [i for i in row if i != 0]
            new_row += [0] * (4 - len(new_row))
            for i in range(3):
                if new_row[i] == new_row[i + 1] and new_row[i] != 0:
                    new_row[i] *= 2
                    new_row.pop(i + 1)
                    new_row.append(0)
            new_matrix.append(new_row)
        self.matrix = new_matrix

    def move_right(self):
        self.matrix = [list(reversed(row)) for row in self.matrix]
        self.move_left()
        self.matrix = [list(reversed(row)) for row in self.matrix]

    def move_up(self):
        self.matrix = [list(row) for row in zip(*self.matrix)]
        self.move_left()
        self.matrix = [list(row) for row in zip(*self.matrix)]

    def move_down(self):
        self.matrix = [list(row) for row in zip(*self.matrix)]
        self.move_right()
        self.matrix = [list(row) for row in zip(*self.matrix)]

    def game_over(self):
        for row in self.matrix:
            if 0 in row:
                return False
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False
        return True


root = tk.Tk()
game = Game2048(root)
root.mainloop()