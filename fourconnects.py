class ConnectFour:
    ROWS = 6
    COLS = 7
    EMPTY = 0

    def __init__(self):
        self.board = [[self.EMPTY] * self.COLS for _ in range(self.ROWS)]
        self.current_player = 1

    def drop_piece(self, col):
        for row in reversed(range(self.ROWS)):
            if self.board[row][col] == self.EMPTY:
                self.board[row][col] = self.current_player
                return row, col
        return None

    def is_valid_move(self, col):
        return self.board[0][col] == self.EMPTY

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def check_winner(self, row, col):
        def count_consecutive_pieces(direction):
            dr, dc = direction
            count = 0
            r, c = row, col
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == self.current_player:
                count += 1
                r += dr
                c += dc
            return count

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = count_consecutive_pieces((dr, dc)) + count_consecutive_pieces((-dr, -dc)) - 1
            if count >= 4:
                return True
        return False

    def is_full(self):
        return all(self.board[0][col] != self.EMPTY for col in range(self.COLS))
import tkinter as tk
from tkinter import messagebox

class ConnectFourGUI:
    def __init__(self, root):
        self.game = ConnectFour()
        self.root = root
        self.root.title("Connect Four")

        self.player1_name = tk.StringVar()
        self.player2_name = tk.StringVar()

        self.setup_names_input()
        
    def setup_names_input(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack()

        tk.Label(input_frame, text="Player 1 Name:").grid(row=0, column=0)
        tk.Entry(input_frame, textvariable=self.player1_name).grid(row=0, column=1)

        tk.Label(input_frame, text="Player 2 Name:").grid(row=1, column=0)
        tk.Entry(input_frame, textvariable=self.player2_name).grid(row=1, column=1)

        tk.Button(input_frame, text="Start Game", command=self.start_game).grid(row=2, column=0, columnspan=2)

    def start_game(self):
        if not self.player1_name.get() or not self.player2_name.get():
            messagebox.showerror("Error", "Please enter names for both players.")
            return

        self.current_player_name = self.player1_name.get()
        
        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.root, width=700, height=600)
        self.canvas.pack()

        self.draw_board()

        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.game.ROWS):
            for col in range(self.game.COLS):
                x0 = col * 100
                y0 = row * 100
                x1 = x0 + 100
                y1 = y0 + 100
                color = "white"
                if self.game.board[row][col] == 1:
                    color = "red"
                elif self.game.board[row][col] == 2:
                    color = "yellow"
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color, outline="blue")

    def handle_click(self, event):
        col = event.x // 100
        if self.game.is_valid_move(col):
            row, col = self.game.drop_piece(col)
            if self.game.check_winner(row, col):
                self.draw_board()
                winner = self.player1_name.get() if self.game.current_player == 1 else self.player2_name.get()
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.reset_game()
                return
            elif self.game.is_full():
                self.draw_board()
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
                return
            self.game.switch_player()
            self.current_player_name = self.player1_name.get() if self.game.current_player == 1 else self.player2_name.get()
            self.draw_board()
        else:
            messagebox.showwarning("Invalid Move", "Column is full. Choose another one.")

    def reset_game(self):
        self.game = ConnectFour()
        self.setup_names_input()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ConnectFourGUI(root)
    root.mainloop()
