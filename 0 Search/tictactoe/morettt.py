from myttt import TicTacToe

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    ttt = TicTacToe()
    if ttt.terminal(board):
        return None

    # Optimization by hardcoding the first move
    if board == [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]:
        return 0, 1

    current_player = ttt.next_player(board)
    best_value = float("-inf") if current_player == "X" else float("inf")

    for move in ttt.actions(board):
        new_value = minimax_value(ttt.result(board, move), best_value)

        if current_player == "X":
            new_value = max(best_value, new_value)

        if current_player == "O":
            new_value = min(best_value, new_value)

        if new_value != best_value:
            best_value = new_value
            best_action = move

    return best_action


def minimax_value(board, best_value):
    """
    Returns the best value for each recursive minimax iteration.
    Optimized using Alpha-Beta Pruning: If the new value found is better
    than the best value then return without checking the others.
    """
    ttt = TicTacToe()
    if ttt.terminal(board):
        return ttt.utility(board)

    current_player = ttt.next_player(board)
    value = float("-inf") if current_player == "X" else float("inf")

    for action in ttt.actions(board):
        new_value = minimax_value(ttt.result(board, action), value)

        if current_player == "X":
            if new_value > best_value:
                return new_value
            value = max(value, new_value)

        if current_player == "O":
            if new_value < best_value:
                return new_value
            value = min(value, new_value)

    return value
