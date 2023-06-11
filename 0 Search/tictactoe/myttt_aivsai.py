#!/usr/bin/env python3
import copy
import morettt_aivsai as mttt

class TicTacToe:
    def __init__(self):
        self.board = []
        self.user = None
        self.player = "X"
        self.ai_move = False
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

    def start(self):
        self.create_board()
        continue_game = True
        while continue_game:
            self.player = self.next_player(self.board)
            if not self.terminal(self.board):
                print(f"Player {self.player} turn")
                self.show_board()
                move = mttt.minimax(self.board)
                self.board = self.result(self.board, move)
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

