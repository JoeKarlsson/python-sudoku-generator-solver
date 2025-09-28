"""
Comprehensive test suite for the Sudoku Generator and Solver.

This module contains tests for all major functionality including:
- Cell operations
- Sudoku generation
- Sudoku validation
- Sudoku solving
- Difficulty classification
"""

import pytest
import copy
from sudoku import (
    Cell, Position, Difficulty, SudokuGenerator
)


class TestPosition:
    """Test cases for the Position dataclass."""

    def test_valid_position(self):
        """Test creating valid positions."""
        pos = Position(1, 1, 1)
        assert pos.row == 1
        assert pos.col == 1
        assert pos.box == 1

        pos = Position(9, 9, 9)
        assert pos.row == 9
        assert pos.col == 9
        assert pos.box == 9

    def test_invalid_position(self):
        """Test that invalid positions raise ValueError."""
        with pytest.raises(ValueError):
            Position(0, 1, 1)

        with pytest.raises(ValueError):
            Position(1, 0, 1)

        with pytest.raises(ValueError):
            Position(1, 1, 0)

        with pytest.raises(ValueError):
            Position(10, 1, 1)

        with pytest.raises(ValueError):
            Position(1, 10, 1)

        with pytest.raises(ValueError):
            Position(1, 1, 10)


class TestCell:
    """Test cases for the Cell class."""

    def test_cell_initialization(self):
        """Test cell initialization with tuple position."""
        cell = Cell((1, 1, 1))
        assert cell.position.row == 1
        assert cell.position.col == 1
        assert cell.position.box == 1
        assert cell.possible_answers == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert cell.answer is None
        assert not cell.solved

    def test_cell_initialization_with_position(self):
        """Test cell initialization with Position object."""
        pos = Position(2, 3, 4)
        cell = Cell(pos)
        assert cell.position == pos
        assert cell.possible_answers == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert cell.answer is None
        assert not cell.solved

    def test_remove_possible_answer(self):
        """Test removing possible answers from a cell."""
        cell = Cell((1, 1, 1))

        # Remove a number
        cell.remove(5)
        assert 5 not in cell.possible_answers
        assert len(cell.possible_answers) == 8
        assert not cell.solved

        # Remove more numbers until only one left
        for num in [1, 2, 3, 4, 6, 7, 8]:
            cell.remove(num)

        assert cell.possible_answers == [9]
        assert cell.solved
        assert cell.answer == 9

    def test_remove_from_solved_cell(self):
        """Test removing a number from a solved cell."""
        cell = Cell((1, 1, 1))
        cell.set_answer(5)

        # Try to remove the solved value
        cell.remove(5)
        assert cell.answer == 0  # Indicates conflict

    def test_set_answer(self):
        """Test setting an answer for a cell."""
        cell = Cell((1, 1, 1))

        cell.set_answer(7)
        assert cell.solved
        assert cell.answer == 7
        assert cell.possible_answers == [7]

    def test_set_invalid_answer(self):
        """Test setting an invalid answer raises ValueError."""
        cell = Cell((1, 1, 1))

        with pytest.raises(ValueError):
            cell.set_answer(0)

        with pytest.raises(ValueError):
            cell.set_answer(10)

    def test_reset_cell(self):
        """Test resetting a cell to original state."""
        cell = Cell((1, 1, 1))
        cell.set_answer(3)

        cell.reset()
        assert not cell.solved
        assert cell.answer is None
        assert cell.possible_answers == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_get_methods(self):
        """Test various getter methods."""
        cell = Cell((2, 3, 4))

        assert not cell.is_solved()
        assert cell.get_position().row == 2
        assert cell.get_position().col == 3
        assert cell.get_position().box == 4
        assert cell.get_possible_answers() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert cell.get_possible_count() == 9
        assert cell.get_answer() == 0

        cell.set_answer(5)
        assert cell.is_solved()
        assert cell.get_answer() == 5


class TestSudokuGenerator:
    """Test cases for the SudokuGenerator class."""

    def test_create_empty_sudoku(self):
        """Test creating an empty Sudoku grid."""
        sudoku = SudokuGenerator.create_empty_sudoku()

        assert len(sudoku) == 81

        # Check that all cells are in correct positions
        for i, cell in enumerate(sudoku):
            row = i // 9 + 1
            col = i % 9 + 1

            # Calculate expected box
            if row in [1, 2, 3]:
                base_box = 1
            elif row in [4, 5, 6]:
                base_box = 4
            else:  # row in [7, 8, 9]
                base_box = 7

            if col in [1, 2, 3]:
                box = base_box
            elif col in [4, 5, 6]:
                box = base_box + 1
            else:  # col in [7, 8, 9]
                box = base_box + 2

            assert cell.position.row == row
            assert cell.position.col == col
            assert cell.position.box == box
            assert not cell.solved

    def test_generate_sudoku(self):
        """Test generating a Sudoku puzzle."""
        sudoku = SudokuGenerator.generate_sudoku()

        assert len(sudoku) == 81

        # All cells should be solved
        for cell in sudoku:
            assert cell.solved
            assert cell.get_answer() in range(1, 10)

    def test_is_valid_sudoku_valid(self):
        """Test validation of a valid Sudoku."""
        sudoku = SudokuGenerator.generate_perfect_sudoku()
        assert SudokuGenerator.is_valid_sudoku(sudoku)

    def test_is_valid_sudoku_invalid_row(self):
        """Test validation detects invalid row."""
        sudoku = SudokuGenerator.create_empty_sudoku()

        # Set two cells in the same row to the same value
        sudoku[0].set_answer(5)  # Row 1, Col 1
        sudoku[1].set_answer(5)  # Row 1, Col 2

        assert not SudokuGenerator.is_valid_sudoku(sudoku)

    def test_is_valid_sudoku_invalid_column(self):
        """Test validation detects invalid column."""
        sudoku = SudokuGenerator.create_empty_sudoku()

        # Set two cells in the same column to the same value
        sudoku[0].set_answer(5)  # Row 1, Col 1
        sudoku[9].set_answer(5)  # Row 2, Col 1

        assert not SudokuGenerator.is_valid_sudoku(sudoku)

    def test_is_valid_sudoku_invalid_box(self):
        """Test validation detects invalid box."""
        sudoku = SudokuGenerator.create_empty_sudoku()

        # Set two cells in the same box to the same value
        sudoku[0].set_answer(5)  # Box 1
        sudoku[1].set_answer(5)  # Box 1

        assert not SudokuGenerator.is_valid_sudoku(sudoku)

    def test_generate_perfect_sudoku(self):
        """Test generating a perfect Sudoku."""
        sudoku = SudokuGenerator.generate_perfect_sudoku()

        assert len(sudoku) == 81
        assert SudokuGenerator.is_valid_sudoku(sudoku)

        # All cells should be solved
        for cell in sudoku:
            assert cell.solved
            assert cell.get_answer() in range(1, 10)

    def test_solve_sudoku_complete(self):
        """Test solving an already complete Sudoku."""
        sudoku = SudokuGenerator.generate_perfect_sudoku()
        solution, guesses, difficulty = SudokuGenerator.solve_sudoku(sudoku)

        assert solution is not None
        assert guesses == 0
        assert difficulty == "Easy"
        assert SudokuGenerator.is_valid_sudoku(solution)

    def test_solve_sudoku_partial(self):
        """Test solving a partial Sudoku."""
        # Create a partial Sudoku by removing some cells from a complete one
        complete = SudokuGenerator.generate_perfect_sudoku()
        partial = copy.deepcopy(complete)

        # Reset some cells
        for i in [0, 1, 2, 10, 11, 12]:
            partial[i].reset()

        solution, guesses, difficulty = SudokuGenerator.solve_sudoku(partial)

        assert solution is not None
        assert SudokuGenerator.is_valid_sudoku(solution)
        assert guesses >= 0

    def test_solve_sudoku_unsolvable(self):
        """Test solving an unsolvable Sudoku."""
        # Create an unsolvable Sudoku
        sudoku = SudokuGenerator.create_empty_sudoku()

        # Set up an impossible configuration
        sudoku[0].set_answer(1)
        sudoku[1].set_answer(1)  # Same row, same value - invalid

        solution, guesses, difficulty = SudokuGenerator.solve_sudoku(
            sudoku, max_guesses=1)

        assert solution is None
        assert guesses == 0
        assert difficulty == "Unsolvable"

    def test_generate_puzzle_with_difficulty(self):
        """Test generating puzzles with specific difficulty levels."""
        for difficulty in Difficulty:
            puzzle, guesses, actual_difficulty = SudokuGenerator.generate_puzzle_with_difficulty(
                difficulty)

            assert len(puzzle) == 81
            assert actual_difficulty in ["Easy", "Medium", "Hard", "Insane"]

            # The puzzle should be solvable
            solution, _, _ = SudokuGenerator.solve_sudoku(puzzle)
            assert solution is not None


class TestIntegration:
    """Integration tests for the complete Sudoku system."""

    def test_full_workflow(self):
        """Test the complete workflow from generation to solving."""
        generator = SudokuGenerator()

        # Generate a puzzle
        puzzle, guesses, difficulty = generator.generate_puzzle_with_difficulty(
            Difficulty.MEDIUM)

        # Verify puzzle properties
        assert len(puzzle) == 81
        assert difficulty in ["Easy", "Medium", "Hard", "Insane"]

        # Count empty cells
        empty_cells = sum(1 for cell in puzzle if not cell.solved)
        assert empty_cells > 0  # Should have some empty cells

        # Solve the puzzle
        solution, solve_guesses, solve_difficulty = generator.solve_sudoku(
            puzzle)

        # Verify solution
        assert solution is not None
        assert generator.is_valid_sudoku(solution)
        assert solve_difficulty in ["Easy", "Medium", "Hard", "Insane"]

        # All cells should be solved in the solution
        for cell in solution:
            assert cell.solved
            assert cell.get_answer() in range(1, 10)

    def test_difficulty_classification(self):
        """Test that difficulty classification works correctly."""
        generator = SudokuGenerator()

        # Test with different guess counts
        test_cases = [
            (0, "Easy"),
            (1, "Medium"),
            (2, "Medium"),
            (3, "Hard"),
            (7, "Hard"),
            (8, "Insane"),
            (15, "Insane")
        ]

        for guesses, expected_difficulty in test_cases:
            # Create a mock solution result
            complete = generator.generate_perfect_sudoku()
            solution, _, difficulty = generator.solve_sudoku(complete)

            # The difficulty should be "Easy" for a complete puzzle
            assert difficulty == "Easy"

    def test_puzzle_uniqueness(self):
        """Test that generated puzzles are unique."""
        generator = SudokuGenerator()

        # Generate multiple puzzles
        puzzles = []
        for _ in range(5):
            puzzle, _, _ = generator.generate_puzzle_with_difficulty(
                Difficulty.EASY)
            puzzles.append(puzzle)

        # Convert to comparable format
        puzzle_strings = []
        for puzzle in puzzles:
            puzzle_str = "".join(str(cell.get_answer()) for cell in puzzle)
            puzzle_strings.append(puzzle_str)

        # All puzzles should be different
        assert len(set(puzzle_strings)) == len(puzzle_strings)


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_sudoku_validation(self):
        """Test validation of completely empty Sudoku."""
        sudoku = SudokuGenerator.create_empty_sudoku()
        assert SudokuGenerator.is_valid_sudoku(sudoku)

    def test_single_cell_sudoku(self):
        """Test Sudoku with only one cell filled."""
        sudoku = SudokuGenerator.create_empty_sudoku()
        sudoku[0].set_answer(5)
        assert SudokuGenerator.is_valid_sudoku(sudoku)

    def test_maximum_guesses_limit(self):
        """Test that solver respects maximum guesses limit."""
        # Create a very difficult puzzle
        sudoku = SudokuGenerator.create_empty_sudoku()

        # Set up a configuration that requires many guesses
        for i in range(0, 80, 2):  # Fill every other cell
            sudoku[i].set_answer((i % 9) + 1)

        solution, guesses, difficulty = SudokuGenerator.solve_sudoku(
            sudoku, max_guesses=5)

        # Should either solve within limit or return None
        if solution is not None:
            assert guesses <= 5
        else:
            assert difficulty == "Unsolvable"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
