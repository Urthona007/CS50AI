import itertools
import random
import copy

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

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
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
        print("Won? mf {self.mines_found} m {self.mines}")
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
        return 0
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.known_safes
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

        #raise NotImplementedError


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

    def adj_cells_set(self, cell):
        """
        Return all cells that adjacent to cell.
        """
        adj_cells = set()
        x = cell[0]
        y = cell[1]

        if x > 0 and y > 0:
            adj_cells.add((x-1, y-1))
        if y > 0:
            adj_cells.add((x, y-1))
        if x < (self.width - 1) and y > 0:
            adj_cells.add((x+1, y-1))
        if x < (self.width -1):
            adj_cells.add((x+1, y))
        if x < (self.width -1) and y < (self.height - 1):
            adj_cells.add((x+1, y+1))
        if y < (self.height - 1):
            adj_cells.add((x, y+1))
        if x > 0 and y < (self.height - 1):
            adj_cells.add((x-1, y+1))
        if x > 0:
            adj_cells.add((x-1, y))
        return adj_cells

    def check_rule1(self):
        """
        Return a sentence where the count is zero.
        """
        for s in self.knowledge:
            if s.count == 0:
                # print(f"Found RULE 1 sentence {s} with count 0.")
                return s
        return None

    def apply_rule1(self, s):
        """
        Apply the zero count inference rule.
        """
        cs = copy.copy(s.cells)
        for c in cs:
            # print(f"Marking {c} as safe.")
            self.mark_safe(c)

    def check_rule2(self):
        """
        Return a sentence where the count equals the number of cells.
        """
        for s in self.knowledge:
            # RULE 2 Check if number of cells are equal to count
            if s.count == len(s.cells) and s.count > 0:
                # print(f"Found RULE 2 sentence {s} with matching count.")
                return s
        return None

    def apply_rule2(self, s):
        """
        When cells are equal to the count, then the cells must be mines.
        """
        cs = copy.copy(s.cells)
        for c in cs:
            # print(f"Marking {c} as safe.")
            self.mark_mine(c)


    def solve_knowledge(self):
        """ Apply a few simple logic rules to reduce the sentences and mark squares as
            safe or or min.
         """
        # print("SOLVING...")

        while True:
            found = False
            sentence_to_delete = []

            s = self.check_rule1() # RULE 1 Check for and apply the zero count inference rule.
            if s is not None:
                self.apply_rule1(s)
                found = True
                sentence_to_delete.append(s)

            s = self.check_rule2() # RULE 2 Check if number of cells are equal to count
            if s is not None:
                self.apply_rule2(s)
                found = True
                sentence_to_delete.append(s)

            for s in sentence_to_delete:
                # print(f'Removing Resolved sentence {s} from knowledge base.')
                self.knowledge.remove(s)

            for s in self.knowledge: # Rule 3: Look for sentences where cells are subset of
                                     #         another sentence's cells and then reduce.
                for ss in self.knowledge:
                    if s != ss:
                        if s.cells.issubset(ss.cells):
                            # print(f"Found RULE 3 {s} is a subset of {ss}")
                            ss.cells -= s.cells
                            ss.count -= s.count
                            # print(f'New sentence is {ss}')
                            found = True
            if not found:
                break
        # print("END SOLVING")
        self.print_knowledge()

    def print_knowledge(self):
        # print(f"KNOWLEDGE: {len(self.knowledge)}")
        # for s in self.knowledge:
            # print(f"\t{s}")
        pass

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
        # print(f"\nadd_knowledge called. cell is {cell} and the count is {count}.")

        # 1) mark the cell as a move that has been made.
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`.
        new_s = Sentence(self.adj_cells_set(cell), count)
        for c in self.safes:
            new_s.mark_safe(c)
        for c in self.mines:
            new_s.mark_mine(c)
        self.knowledge.append(new_s)
        self.print_knowledge()

        # 4) mark any additional cells as safe or as mines if it can be concluded based on the
        #    AI's knowledge base.
        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing
        #    knowledge.
        self.solve_knowledge()

        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for c in self.safes:
            if c not in self.moves_made:
                # print(f"make_safe_move returning {0}", c)
                return c
        # print('make_safe_move returning None!')
        return None
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # return(0,0)
        # Pure random for now
        # random.seed(2023)

        if len(self.moves_made) + len(self.mines) == self.width * self.height:
            return None # We won!
        while True:
            randval = random.randint(0,self.width*self.height-1)
            candidate = (int(randval/self.width), randval%self.width)
            if candidate not in self.mines and candidate not in self.moves_made:
                break
        return candidate

        #raise NotImplementedError
