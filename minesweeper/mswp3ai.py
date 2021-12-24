#!/usr/bin/env python3
"""
This program has an AI that makes moves for each turn when ok by user.
User can also choose for AI to move to end.
"""
import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        # The actual values of the grid
        self.numbers = [[0 for y in range(self.width)] \
            for x in range(self.height)]
        # The apparent values of the grid
        self.mine_values = [[' ' for y in range(self.width)] \
            for x in range(self.height)]
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
                self.numbers[i][j] = 'M'

        # At first, player has found no mines
        self.mines_found = set()

    def print_mines(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def print_board(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                print("|" + str(self.mine_values[i][j]), end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

    def infer_from(self, other):
        """
        Returns inferred sentence from this and other sentence.
        If it can't make any inference returns None.
        """
        if other.cells.issubset(self.cells):
            return Sentence(self.cells - other.cells, self.count - other.count)
        elif self.cells.issubset(other.cells):
            return Sentence(other.cells - self.cells, other.count - self.count)
        else:
            return None

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Create new sentence and mark already known mines and safes in it
        new_sentence = Sentence(self.get_neighbors(cell), count)

        for mine in self.mines:
            new_sentence.mark_mine(mine)
        for safe in self.safes:
            new_sentence.mark_safe(safe)

        self.knowledge.append(new_sentence)

        # Mark additional mines and safes if their position can be concluded from the knowledge base
        new_mines = set()
        new_safes = set()

        for sentence in self.knowledge:
            for cell in sentence.known_mines():
                new_mines.add(cell)
            for cell in sentence.known_safes():
                new_safes.add(cell)

        for cell in new_mines:
            self.mark_mine(cell)
        for cell in new_safes:
            self.mark_safe(cell)

        # Add new sentences if they can be inferred from existing knowledge
        more_sentences = []

        for sentenceA, sentenceB in itertools.combinations(self.knowledge, 2):
            inference = sentenceA.infer_from(sentenceB)
            if inference is not None and inference not in self.knowledge:
                more_sentences.append(inference)

        self.knowledge.extend(more_sentences)

        # Remove empty sentences from the knowledge base
        for sentence in self.knowledge:
            if sentence == Sentence(set(), 0):
                self.knowledge.remove(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        moves_left = self.safes - self.moves_made

        if moves_left:
            return random.choice(tuple(moves_left))
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves_left = set(itertools.product(range(0, self.height), range(0, self.width)))
        moves_left = moves_left - self.mines - self.moves_made

        if moves_left:
            return random.choice(tuple(moves_left))
        else:
            return None

    def get_neighbors(self, cell):
        """
        Returns a set containing all neighbors of a given cell.
        """
        neighbors = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add as neighbour if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        return neighbors

if __name__ == "__main__":
    game = Minesweeper()
    ai = MinesweeperAI()
    revealed = set()
    flags = set()
    lost = False
    all_ai = False
    game.print_mines()
    print()
    while not lost:
        game.print_board()
        move = None
        try_ai = False
        if not all_ai:
            inp_ai = input("Do you want AI to move?  Type a for AI to move to the end. (y/n/a): ")
            if inp_ai.lower() == 'y':
                print("AI will move.")
                try_ai = True
            elif inp_ai.lower() == 'n':
                print("AI will not move.")
                try_ai = False
            elif inp_ai.lower() == 'a':
                print("AI will move to the end.")
                all_ai = True
            else:
                print("Wrong entry.  AI will not move.")
                try_ai = False
        if (try_ai or all_ai) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    game.mines_found = flags
                    print("No moves left to make.")
                    if game.won():
                        print("You win!")
                        break
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
        elif not try_ai and not lost:
            inp = input("Enter row number followed by space and column number = ").split()
                    # Standard input
            if len(inp) == 2:
                # Try block to handle errant input
                try:
                    (i, j) = tuple(map(int, inp))
                    move = (i-1, j-1)
                except ValueError:
                    print("Wrong input!")
                    continue
            else:
                print("Wrong input!")
                continue
        if move:
            if game.is_mine(move):
                lost = True
                print(f"({move[0]+1}, {move[1]+1}), lost={lost}")
            else:
                nearby = game.nearby_mines(move)
                revealed.add(move)
                ai.add_knowledge(move, nearby)
                # print(f"{move[0]+1}, {move[1]+1}")
                # print(nearby)
                print(revealed)
                (i, j) = move
                game.mine_values[i][j]=nearby
