#!/usr/bin/env python3
import copy

class TicTacToe:
    def __init__(self):
        self.board = []
        self.user = None
        self.player = "X"
        self.ai_move = False
        self.sum = [0, None]
        self.currentD = 1
    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)
    def show_board(self):
        for row in self.board:
            for col in row:
                print(col, end=" ")
            print()
    def next_player(self, board):
        """
        Returns player who has the next turn on a board.
        """
        x_count = 0
        o_count = 0
        for row in board:
            for cell in row:
                if cell == "X":
                    x_count += 1
                if cell == "O":
                    o_count += 1
        if x_count <= o_count:
            return "X"
        else:
            return "O"

    def choose_player(self):
        choice = input("Do you want to make the first move? (y/n):  ")
        if choice.lower() == "y":
            self.user = "X"
            print("You are player X")
            self.ai_move = False
        elif choice.lower() =="n":
            self.user = "O"
            print("You are player O")
            self.ai_move = True

    def terminal(self, board):
        """
        Returns True if game is over, False otherwise.
        """
        if self.winner(board) is not None \
            or not self.actions(board):
            return True
        else:
            return False

    def utility(self, board):
        """
        Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
        """
        winner_player = self.winner(board)
        if winner_player == "X":
            return 1
        elif winner_player == "O":
            return -1
        else:
            return 0

    def actions(self, board):
        """
        Returns set of all possible actions (i, j) available on the board.
        """
        possible_moves = set()
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == "-":
                    possible_moves.add((i, j))
        return possible_moves

    def winner(self, board):
        """
        Returns the winner of the game, if there is one.
        """
        wins = [[(0, 0), (0, 1), (0, 2)],
                [(1, 0), (1, 1), (1, 2)],
                [(2, 0), (2, 1), (2, 2)],
                [(0, 0), (1, 0), (2, 0)],
                [(0, 1), (1, 1), (2, 1)],
                [(0, 2), (1, 2), (2, 2)],
                [(0, 0), (1, 1), (2, 2)],
                [(0, 2), (1, 1), (2, 0)]]
        for combination in wins:
            checks_x = 0
            checks_o = 0
            for i, j in combination:
                if board[i][j] == "X":
                    checks_x += 1
                if board[i][j] == "O":
                    checks_o += 1
            if checks_x == 3:
                return "X"
            if checks_o == 3:
                return "O"
        return None

    def result(self, board, move):
        """
        Returns the board that results from making move (i, j) on the board.
        """
        if move not in self.actions(board):
            raise ValueError
        new_board = copy.deepcopy(board)
        new_board[move[0]][move[1]] = self.next_player(board)
        return new_board

    def minimax(self, board):
        """
        Returns the optimal action for the current player on the board.
        """
        if self.terminal(board):
            return None
        self.sum = [0, None]
        # Optimization by hardcoding the first move
        # if board == [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]:
        #     return 0, 1

        current_player = self.next_player(board)
        best_value = float("-inf") if current_player == "X" else float("inf")

        for move in self.actions(board):
            new_value = self.calculate_value(
                self.result(board, move), best_value, move)

            if current_player == "X":
                new_value = max(best_value, new_value)

            if current_player == "O":
                new_value = min(best_value, new_value)

            if new_value != best_value:
                best_value = new_value
                best_action = move

        print(self.sum)
        return self.sum[1]


    def calculate_value(self, board, prev_value, move):
        """
        Returns the best value for each recursive minimax iteration.
        Optimized using Alpha-Beta Pruning: If the new value found is better
        than the best value then return without checking the others.
        """
        if self.terminal(board):
            return self.utility(board)

        current_player = self.next_player(board)
        value = float("-inf") if current_player == "X" else float("inf")
        sum = 0
        self.currentD += 1
        if self.currentD < 5:
            for action in self.actions(board):
                new_value = self.calculate_value(self.result(board, action), value, move)
                sum += new_value

                if current_player == "X":
                    if new_value > prev_value:
                        value = new_value
                    else:
                        value = max(value, new_value)
                if current_player == "O":
                    if new_value < prev_value:
                        value = new_value
                    else:
                        value = min(value, new_value)
        self.currentD -= 1
        if current_player == "X":
            if self.sum[0] < sum:
                self.sum = [sum, move]
                print(self.sum)
        if current_player == "O":
            if self.sum[0] > sum:
                self.sum = [sum, move]
                print(self.sum)
        return value

    def start(self):
        self.choose_player()
        self.create_board()
        continue_game = True
        while continue_game:
            self.player = self.next_player(self.board)
            if self.user == self.player and not self.terminal(self.board):
                print(f"Player {self.player} turn")
                self.show_board()
                wrong_input = True
                while wrong_input:
                    choice = input("Enter row, col of your move, Q to end game: ")
                    if choice.lower() == "q":
                        continue_game = False
                        break
                    else:
                        try:
                            row, col = list(map(int, choice.split()))
                        except:
                            print("row, col must contain values between 1 and 3")
                            continue
                        else:
                            if 1 <= row <= 3 and 1 <= col <= 3:
                                wrong_input = False
                            else:
                                print("row, col must be between 1 and 3")
                    possible_moves = self.actions(self.board)
                    # print(possible_moves)
                    if (row-1, col-1) not in possible_moves:
                        print("You must choose row, col of a blank '-' space")
                        wrong_input = True
                if continue_game:
                    print()
                    self.board[row-1][col-1] = self.player
                    self.show_board()
                    print()
            # Check for AI move
            if self.user != self.player and not self.terminal(self.board):
                if self.ai_move:
                    move = self.minimax(self.board)
                    self.board = self.result(self.board, move)
                    self.ai_move = False
                else:
                    self.ai_move = True
            if self.terminal(self.board):
                who = self.winner(self.board)
                if who == "X":
                    print("X wins!")
                    if self.user != self.player:
                        self.show_board()
                    break
                elif who == "O":
                    print("O wins!")
                    if self.user != self.player:
                        self.show_board()
                    break
                else:
                    print("It's a draw!")
                    if self.user != self.player:
                        self.show_board()
                    break


def main():
    tic_tac_toe = TicTacToe()
    tic_tac_toe.start()

if __name__ == "__main__":
    main()

