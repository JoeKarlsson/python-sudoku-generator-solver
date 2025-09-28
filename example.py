#!/usr/bin/env python3
"""
Example script demonstrating the Python Sudoku Generator and Solver.

This script shows various ways to use the Sudoku generator and solver,
including generating puzzles of different difficulties and solving them.
"""

from sudoku import SudokuGenerator, Difficulty


def main():
    """Main example function."""
    print("Python Sudoku Generator and Solver - Example")
    print("=" * 50)

    generator = SudokuGenerator()

    # Example 1: Generate and solve a puzzle of each difficulty
    print("\n1. Generating puzzles of different difficulties:")
    print("-" * 45)

    for difficulty in Difficulty:
        print(f"\n{difficulty.value} Difficulty Puzzle:")
        puzzle, guesses, actual_difficulty = generator.generate_puzzle_with_difficulty(
            difficulty)
        print(
            f"Generated as: {actual_difficulty} (required {guesses} guesses)")
        generator.print_sudoku(puzzle)

        # Solve the puzzle
        solution, solve_guesses, solve_difficulty = generator.solve_sudoku(
            puzzle)
        if solution:
            print(f"\nSolution (solved in {solve_guesses} guesses):")
            generator.print_sudoku(solution)
        else:
            print("Could not solve the puzzle!")
        print()

    # Example 2: Create a custom puzzle
    print("\n2. Creating and solving a custom puzzle:")
    print("-" * 40)

    # Create an empty puzzle
    custom_puzzle = generator.create_empty_sudoku()

    # Set some initial values (this creates a solvable puzzle)
    initial_values = [
        (0, 5), (1, 3), (4, 7),
        (9, 6), (12, 1), (13, 9), (14, 5),
        (19, 9), (20, 8), (25, 6),
        (27, 8), (31, 6), (35, 3),
        (36, 4), (39, 8), (41, 3), (44, 1),
        (45, 7), (49, 2), (53, 6),
        (55, 6), (60, 2), (61, 8),
        (66, 4), (67, 1), (68, 9),
        (71, 5), (76, 8), (79, 7), (80, 9)
    ]

    for cell_index, value in initial_values:
        custom_puzzle[cell_index].set_answer(value)

    print("Custom puzzle:")
    generator.print_sudoku(custom_puzzle)

    # Solve the custom puzzle
    solution, guesses, difficulty = generator.solve_sudoku(custom_puzzle)
    if solution:
        print(
            f"\nSolution (solved in {guesses} guesses, {difficulty} difficulty):")
        generator.print_sudoku(solution)
    else:
        print("Could not solve the custom puzzle!")

    # Example 3: Validate puzzles
    print("\n3. Validating puzzles:")
    print("-" * 25)

    # Generate a valid puzzle
    valid_puzzle = generator.generate_perfect_sudoku()
    is_valid = generator.is_valid_sudoku(valid_puzzle)
    print(f"Generated puzzle is valid: {is_valid}")

    # Create an invalid puzzle
    invalid_puzzle = generator.create_empty_sudoku()
    invalid_puzzle[0].set_answer(5)  # Row 1, Col 1
    invalid_puzzle[1].set_answer(5)  # Row 1, Col 2 (same row, same value)
    is_invalid = generator.is_valid_sudoku(invalid_puzzle)
    print(f"Invalid puzzle is valid: {is_invalid}")

    # Example 4: Performance test
    print("\n4. Performance test:")
    print("-" * 20)

    import time

    # Time puzzle generation
    start_time = time.time()
    for _ in range(10):
        generator.generate_puzzle_with_difficulty(Difficulty.MEDIUM)
    generation_time = time.time() - start_time
    print(f"Generated 10 medium puzzles in {generation_time:.2f} seconds")
    print(f"Average time per puzzle: {generation_time/10:.3f} seconds")

    # Time puzzle solving
    puzzle, _, _ = generator.generate_puzzle_with_difficulty(Difficulty.HARD)
    start_time = time.time()
    for _ in range(10):
        generator.solve_sudoku(puzzle)
    solving_time = time.time() - start_time
    print(f"Solved the same puzzle 10 times in {solving_time:.2f} seconds")
    print(f"Average time per solve: {solving_time/10:.3f} seconds")


if __name__ == "__main__":
    main()
