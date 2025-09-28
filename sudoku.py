"""
Python Sudoku Generator and Solver

A comprehensive Sudoku puzzle generator and solver with multiple difficulty levels.
Supports generating puzzles of varying difficulty and solving them using constraint propagation
and backtracking algorithms.

Author: Joe Carlson (2015)
Updated: 2024
"""

from __future__ import annotations
import time
import copy
import random
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    """Difficulty levels for Sudoku puzzles."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    INSANE = "Insane"


@dataclass
class Position:
    """Represents a position in a Sudoku grid."""
    row: int
    col: int
    box: int

    def __post_init__(self):
        """Validate position coordinates."""
        if not (1 <= self.row <= 9 and 1 <= self.col <= 9 and 1 <= self.box <= 9):
            raise ValueError("Position coordinates must be between 1 and 9")


class Cell:
    """
    Represents a single cell in a Sudoku puzzle.

    A cell can contain a number from 1-9 or be empty. Each cell tracks its possible
    values and whether it has been solved.
    """

    def __init__(self, position: Union[Tuple[int, int, int], Position]) -> None:
        """Initialize a cell with all possible values (1-9)."""
        if isinstance(position, tuple):
            self.position = Position(position[0], position[1], position[2])
        else:
            self.position = position

        self.possible_answers: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.answer: Optional[int] = None
        self.solved: bool = False

    def remove(self, num: int) -> None:
        """Remove a number from the list of possible answers."""
        if num in self.possible_answers and not self.solved:
            self.possible_answers.remove(num)
            if len(self.possible_answers) == 1:
                self.answer = self.possible_answers[0]
                self.solved = True
        elif num in self.possible_answers and self.solved:
            # This indicates a conflict - the cell is solved but we're trying to remove its value
            self.answer = 0

    def is_solved(self) -> bool:
        """Return whether the cell has been solved."""
        return self.solved

    def get_position(self) -> Position:
        """Return the position of the cell in the Sudoku puzzle."""
        return self.position

    def get_possible_answers(self) -> List[int]:
        """Return a list of possible answers for this cell."""
        return self.possible_answers.copy()

    def get_possible_count(self) -> int:
        """Return the number of possible answers for this cell."""
        return len(self.possible_answers)

    def get_answer(self) -> int:
        """Return the solved value if the cell is solved, otherwise return 0."""
        if self.solved:
            return self.possible_answers[0]
        return 0

    def set_answer(self, num: int) -> None:
        """Set the answer for this cell and mark it as solved."""
        if num not in range(1, 10):
            raise ValueError(f"Answer must be between 1 and 9, got {num}")

        self.solved = True
        self.answer = num
        self.possible_answers = [num]

    def reset(self) -> None:
        """Reset the cell to its original state with all possible values."""
        self.possible_answers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.answer = None
        self.solved = False


class SudokuGenerator:
    """Main class for generating and solving Sudoku puzzles."""

    @staticmethod
    def create_empty_sudoku() -> List[Cell]:
        """
        Create an empty Sudoku grid with all cells initialized.

        Returns:
            List of 81 Cell objects representing an empty Sudoku puzzle.
        """
        cells = []
        for row in range(1, 10):
            # Calculate base box number for this row
            if row in [7, 8, 9]:
                base_box = 7
            elif row in [4, 5, 6]:
                base_box = 4
            else:  # row in [1, 2, 3]
                base_box = 1

            for col in range(1, 10):
                # Calculate box number for this column
                if col in [7, 8, 9]:
                    box = base_box + 2
                elif col in [4, 5, 6]:
                    box = base_box + 1
                else:  # col in [1, 2, 3]
                    box = base_box

                cell = Cell((row, col, box))
                cells.append(cell)

        return cells

    @staticmethod
    def print_sudoku(sudoku: List[Cell]) -> None:
        """
        Print a Sudoku puzzle in a human-readable format.

        Args:
            sudoku: List of 81 Cell objects representing the Sudoku puzzle.
        """
        # Convert cells to a 9x9 grid
        grid = [[0 for _ in range(9)] for _ in range(9)]

        for i, cell in enumerate(sudoku):
            row = i // 9
            col = i % 9
            grid[row][col] = cell.get_answer()

        # Print the grid with proper formatting
        for i, row in enumerate(grid):
            if i % 3 == 0 and i != 0:
                print("")

            # Print each group of 3 numbers
            for j in range(0, 9, 3):
                group = row[j:j+3]
                print(" ".join(str(num) if num !=
                      0 else "." for num in group), end="  ")
            print()

    @staticmethod
    def generate_sudoku() -> List[Cell]:
        """
        Generate a completed Sudoku puzzle using constraint propagation.

        Returns:
            List of 81 Cell objects representing a completed Sudoku puzzle.
        """
        cells = list(range(81))  # Indices of cells not yet set
        sudoku = SudokuGenerator.create_empty_sudoku()

        while cells:
            # Find cells with the minimum number of possible values
            min_possibilities = min(
                sudoku[i].get_possible_count() for i in cells)
            cells_with_min = [
                i for i in cells if sudoku[i].get_possible_count() == min_possibilities]

            # Randomly choose one of the cells with minimum possibilities
            chosen_index = random.choice(cells_with_min)
            chosen_cell = sudoku[chosen_index]
            cells.remove(chosen_index)

            position = chosen_cell.get_position()

            if not chosen_cell.is_solved():
                # Set a random possible value
                possible_values = chosen_cell.get_possible_answers()
                final_value = random.choice(possible_values)
                chosen_cell.set_answer(final_value)
            else:
                final_value = chosen_cell.get_answer()

            # Remove this value from all cells in the same row, column, or box
            for i in cells:
                other_cell = sudoku[i]
                other_position = other_cell.get_position()

                if (position.row == other_position.row or
                    position.col == other_position.col or
                        position.box == other_position.box):
                    other_cell.remove(final_value)

        return sudoku

    @staticmethod
    def is_valid_sudoku(sudoku: List[Cell]) -> bool:
        """
        Check if a Sudoku puzzle is valid (follows all Sudoku rules).

        Args:
            sudoku: List of 81 Cell objects representing the Sudoku puzzle.

        Returns:
            True if the puzzle is valid, False otherwise.
        """
        # Check each cell against all other cells
        for i in range(len(sudoku)):
            for j in range(len(sudoku)):
                if i != j:
                    pos1 = sudoku[i].get_position()
                    pos2 = sudoku[j].get_position()

                    # Check if cells are in the same row, column, or box
                    if (pos1.row == pos2.row or
                        pos1.col == pos2.col or
                            pos1.box == pos2.box):

                        num1 = sudoku[i].get_answer()
                        num2 = sudoku[j].get_answer()

                        # If both cells have the same non-zero value, it's invalid
                        if num1 != 0 and num2 != 0 and num1 == num2:
                            return False

        return True

    @staticmethod
    def generate_perfect_sudoku() -> List[Cell]:
        """
        Generate a completed and valid Sudoku puzzle.

        Returns:
            List of 81 Cell objects representing a valid completed Sudoku puzzle.
        """
        while True:
            sudoku = SudokuGenerator.generate_sudoku()
            if SudokuGenerator.is_valid_sudoku(sudoku):
                return sudoku

    @staticmethod
    def solve_sudoku(sudoku: List[Cell], max_guesses: int = 900) -> Tuple[Optional[List[Cell]], int, str]:
        """
        Solve a Sudoku puzzle using constraint propagation and backtracking.

        Args:
            sudoku: List of 81 Cell objects representing the Sudoku puzzle to solve.
            max_guesses: Maximum number of guesses allowed before giving up.

        Returns:
            Tuple of (solved_sudoku, guess_count, difficulty_level) or (None, 0, "Unsolvable")
        """
        if max_guesses <= 0:
            return None, 0, "Unsolvable"

        guesses = 0
        working_sudoku = copy.deepcopy(sudoku)
        cells = list(range(81))
        solved_cells = []

        # Find cells that are already solved
        for i in cells:
            if working_sudoku[i].get_possible_count() == 1:
                solved_cells.append(i)

        # Process solved cells
        while solved_cells:
            for cell_index in solved_cells:
                cell = working_sudoku[cell_index]
                position = cell.get_position()
                final_value = cell.get_answer()

                # Remove this value from all cells in the same row, column, or box
                for i in cells:
                    other_cell = working_sudoku[i]
                    other_position = other_cell.get_position()

                    if (position.row == other_position.row or
                        position.col == other_position.col or
                            position.box == other_position.box):
                        other_cell.remove(final_value)

                        # If this creates a new solved cell, add it to the list
                        if (other_cell.get_possible_count() == 1 and
                                i not in solved_cells and i in cells):
                            solved_cells.append(i)

                solved_cells.remove(cell_index)
                cells.remove(cell_index)

            # If no more cells can be solved by constraint propagation, make a guess
            if cells and not solved_cells:
                # Find cells with minimum possibilities
                min_possibilities = min(
                    working_sudoku[i].get_possible_count() for i in cells)
                cells_with_min = [
                    i for i in cells if working_sudoku[i].get_possible_count() == min_possibilities]

                # Randomly choose a cell and a value
                chosen_index = random.choice(cells_with_min)
                chosen_cell = working_sudoku[chosen_index]
                possible_values = chosen_cell.get_possible_answers()
                chosen_value = random.choice(possible_values)

                chosen_cell.set_answer(chosen_value)
                solved_cells.append(chosen_index)
                guesses += 1

        # Check if the puzzle is solved and valid
        if SudokuGenerator.is_valid_sudoku(working_sudoku):
            # Determine difficulty based on number of guesses
            if guesses == 0:
                difficulty = "Easy"
            elif guesses <= 2:
                difficulty = "Medium"
            elif guesses <= 7:
                difficulty = "Hard"
            else:
                difficulty = "Insane"

            return working_sudoku, guesses, difficulty
        else:
            # Try again with fewer guesses allowed
            return SudokuGenerator.solve_sudoku(sudoku, max_guesses - 1)

    @staticmethod
    def generate_puzzle_with_difficulty(difficulty: Difficulty) -> Tuple[List[Cell], int, str]:
        """
        Generate a Sudoku puzzle of the specified difficulty level.

        Args:
            difficulty: The desired difficulty level.

        Returns:
            Tuple of (puzzle, guess_count, difficulty_level).
        """
        # Generate a perfect Sudoku
        perfect_sudoku = SudokuGenerator.generate_perfect_sudoku()

        # Create a puzzle by removing cells based on difficulty
        puzzle = copy.deepcopy(perfect_sudoku)

        # Define how many cells to remove based on difficulty
        cells_to_remove = {
            Difficulty.EASY: 40,      # Remove 40 cells for easy
            Difficulty.MEDIUM: 50,    # Remove 50 cells for medium
            Difficulty.HARD: 60,      # Remove 60 cells for hard
            Difficulty.INSANE: 70     # Remove 70 cells for insane
        }

        num_to_remove = cells_to_remove[difficulty]
        cells_indices = list(range(81))
        random.shuffle(cells_indices)

        # Remove cells one by one
        for i in range(num_to_remove):
            if i < len(cells_indices):
                puzzle[cells_indices[i]].reset()

        # Solve the puzzle to determine actual difficulty
        solution, guesses, actual_difficulty = SudokuGenerator.solve_sudoku(
            puzzle)

        if solution is None:
            # If unsolvable, return a simpler puzzle
            puzzle = copy.deepcopy(perfect_sudoku)
            for i in range(30):  # Remove only 30 cells
                if i < len(cells_indices):
                    puzzle[cells_indices[i]].reset()
            solution, guesses, actual_difficulty = SudokuGenerator.solve_sudoku(
                puzzle)

        return puzzle, guesses, actual_difficulty


def main():
    """Main function to generate and display a Sudoku puzzle."""
    print("Python Sudoku Generator and Solver")
    print("=" * 40)

    # Generate a medium difficulty puzzle
    generator = SudokuGenerator()
    puzzle, guesses, difficulty = generator.generate_puzzle_with_difficulty(
        Difficulty.MEDIUM)

    print(f"Generated {difficulty} difficulty puzzle")
    print(f"Required {guesses} guesses to solve")
    print("\nPuzzle:")
    generator.print_sudoku(puzzle)

    print("\nSolution:")
    solution, _, _ = generator.solve_sudoku(puzzle)
    if solution:
        generator.print_sudoku(solution)
    else:
        print("Could not solve the puzzle!")


if __name__ == "__main__":
    main()
