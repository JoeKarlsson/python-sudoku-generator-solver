# Python Sudoku Generator and Solver

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-27%20passing-brightgreen.svg)](https://github.com/joecarlson/python-sudoku-generator-solver)

A comprehensive, modern Python implementation of a Sudoku puzzle generator and solver with multiple difficulty levels. This project features constraint propagation, backtracking algorithms, and a clean, well-tested codebase.

## ✨ Features

- 🎯 **Multiple Difficulty Levels**: Easy, Medium, Hard, and Insane
- 🧩 **Smart Generation**: Creates unique, solvable puzzles using constraint propagation
- 🔍 **Advanced Solving**: Uses both constraint propagation and backtracking algorithms
- ✅ **Comprehensive Testing**: Full test suite with 27 passing tests
- 🐍 **Modern Python**: Type hints, dataclasses, and clean architecture
- 📊 **Difficulty Analysis**: Automatically classifies puzzle difficulty based on solving complexity
- ⚡ **High Performance**: Generates puzzles in milliseconds
- 🎮 **Easy to Use**: Simple API with clear examples

## 🚀 Quick Start

### Installation

#### Option 1: Clone and Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/joecarlson/python-sudoku-generator-solver.git
cd python-sudoku-generator-solver

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

#### Option 2: Direct Python Usage

```bash
# Clone the repository
git clone https://github.com/joecarlson/python-sudoku-generator-solver.git
cd python-sudoku-generator-solver

# Install only pytest for testing
pip install pytest

# Run directly without installation
python sudoku.py
```

### Basic Usage

```python
from sudoku import SudokuGenerator, Difficulty

# Create a generator instance
generator = SudokuGenerator()

# Generate a medium difficulty puzzle
puzzle, guesses, difficulty = generator.generate_puzzle_with_difficulty(Difficulty.MEDIUM)

print(f"Generated {difficulty} puzzle requiring {guesses} guesses")
generator.print_sudoku(puzzle)

# Solve the puzzle
solution, solve_guesses, solve_difficulty = generator.solve_sudoku(puzzle)
print(f"Solved in {solve_guesses} guesses")
generator.print_sudoku(solution)
```

### Command Line Usage

```bash
# Generate and display a puzzle
python sudoku.py

# Run the example script
python example.py

# Run tests
pytest test_sudoku.py -v

# Run tests with coverage
pytest test_sudoku.py --cov=sudoku --cov-report=html
```

## 📖 Examples

### Generate Different Difficulty Levels

```python
from sudoku import SudokuGenerator, Difficulty

generator = SudokuGenerator()

# Generate puzzles of different difficulties
for difficulty in Difficulty:
    puzzle, guesses, actual_difficulty = generator.generate_puzzle_with_difficulty(difficulty)
    print(f"{difficulty.value}: {actual_difficulty} (required {guesses} guesses)")
    generator.print_sudoku(puzzle)
    print()
```

### Solve a Custom Puzzle

```python
from sudoku import SudokuGenerator, Cell

# Create a custom puzzle
generator = SudokuGenerator()
puzzle = generator.create_empty_sudoku()

# Set some initial values
puzzle[0].set_answer(5)  # Top-left corner
puzzle[10].set_answer(3)  # Second row, second column
# ... set more values as needed

# Solve the puzzle
solution, guesses, difficulty = generator.solve_sudoku(puzzle)

if solution:
    print(f"Solved in {guesses} guesses ({difficulty} difficulty)")
    generator.print_sudoku(solution)
else:
    print("Puzzle is unsolvable!")
```

### Validate a Puzzle

```python
from sudoku import SudokuGenerator, Difficulty

generator = SudokuGenerator()

# Generate a puzzle
puzzle, _, _ = generator.generate_puzzle_with_difficulty(Difficulty.MEDIUM)

# Check if it's valid
is_valid = generator.is_valid_sudoku(puzzle)
print(f"Puzzle is valid: {is_valid}")

# Check the solution
solution, _, _ = generator.solve_sudoku(puzzle)
is_solution_valid = generator.is_valid_sudoku(solution)
print(f"Solution is valid: {is_solution_valid}")
```

## 🔧 API Reference

### Core Classes

#### `SudokuGenerator`

The main class for generating and solving Sudoku puzzles.

**Methods:**

- `create_empty_sudoku() -> List[Cell]`: Create an empty 9x9 Sudoku grid
- `generate_sudoku() -> List[Cell]`: Generate a completed Sudoku puzzle
- `generate_perfect_sudoku() -> List[Cell]`: Generate a valid completed Sudoku
- `generate_puzzle_with_difficulty(difficulty: Difficulty) -> Tuple[List[Cell], int, str]`: Generate a puzzle of specified difficulty
- `solve_sudoku(sudoku: List[Cell], max_guesses: int = 900) -> Tuple[Optional[List[Cell]], int, str]`: Solve a Sudoku puzzle
- `is_valid_sudoku(sudoku: List[Cell]) -> bool`: Validate a Sudoku puzzle
- `print_sudoku(sudoku: List[Cell]) -> None`: Print a Sudoku puzzle in a readable format

#### `Cell`

Represents a single cell in a Sudoku puzzle.

**Methods:**

- `set_answer(num: int) -> None`: Set the cell's value
- `remove(num: int) -> None`: Remove a possible value
- `reset() -> None`: Reset cell to original state
- `is_solved() -> bool`: Check if cell is solved
- `get_answer() -> int`: Get the cell's value (0 if unsolved)
- `get_possible_answers() -> List[int]`: Get possible values
- `get_possible_count() -> int`: Get number of possible values

#### `Position`

Represents a position in the Sudoku grid.

**Attributes:**

- `row: int`: Row number (1-9)
- `col: int`: Column number (1-9)
- `box: int`: Box number (1-9)

### Difficulty Levels

The `Difficulty` enum defines four difficulty levels:

- **Easy**: 0 guesses required
- **Medium**: 1-2 guesses required
- **Hard**: 3-7 guesses required
- **Insane**: 8+ guesses required

## 🧠 Algorithm Details

### Generation Algorithm

1. **Constraint Propagation**: Start with all cells having possible values 1-9
2. **Minimum Remaining Values**: Always choose cells with the fewest possible values
3. **Random Selection**: When multiple cells have the same minimum, choose randomly
4. **Constraint Elimination**: Remove chosen values from cells in the same row, column, and box
5. **Validation**: Ensure the generated puzzle is valid

### Solving Algorithm

1. **Constraint Propagation**: Fill cells that have only one possible value
2. **Backtracking**: When no more cells can be filled by constraint propagation:
   - Choose a cell with minimum remaining values
   - Try each possible value
   - Recursively solve the resulting puzzle
   - Backtrack if no solution is found

### Difficulty Classification

Puzzle difficulty is determined by the number of guesses required during solving:

- **Easy**: Can be solved using only constraint propagation
- **Medium**: Requires 1-2 guesses
- **Hard**: Requires 3-7 guesses
- **Insane**: Requires 8+ guesses

## 🧪 Testing

The project includes a comprehensive test suite covering:

- Unit tests for all classes and methods
- Integration tests for complete workflows
- Edge case testing
- Performance testing
- Validation testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=sudoku --cov-report=html

# Run specific test file
pytest test_sudoku.py

# Run specific test class
pytest test_sudoku.py::TestCell

# Run specific test method
pytest test_sudoku.py::TestCell::test_set_answer
```

### Test Results

```
============================== 27 passed in 0.31s ==============================
```

## ⚡ Performance

- **Generation**: Typically generates puzzles in < 0.01 seconds
- **Solving**: Most puzzles solve in < 0.1 seconds
- **Memory**: Minimal memory footprint (~1MB for typical usage)
- **Scalability**: Can generate thousands of puzzles efficiently

### Performance Benchmarks

```python
# Generate 10 medium puzzles
import time
start = time.time()
for _ in range(10):
    generator.generate_puzzle_with_difficulty(Difficulty.MEDIUM)
print(f"Generated 10 puzzles in {time.time() - start:.2f} seconds")
# Output: Generated 10 puzzles in 0.10 seconds
```

## 📁 Project Structure

```
python-sudoku-generator-solver/
├── 📄 sudoku.py              # Main modernized code
├── 📄 test_sudoku.py         # Comprehensive test suite
├── 📄 example.py             # Usage examples
├── 📄 requirements.txt       # Dependencies
├── 📄 setup.py              # Package configuration
├── 📄 README.md             # This file
├── 📄 LICENSE               # MIT License
├── 📄 .gitignore            # Git ignore rules
├── 📁 images/               # All image files
│   ├── Easy.jpg
│   ├── Easy1.jpg
│   ├── Hard.jpg
│   ├── Insane.jpg
│   ├── Medium.jpg
│   ├── Medium2.jpg
│   └── SudokuFlow1.jpg
├── 📁 docs/                 # Documentation files
│   └── Sample Randomly Generated Sudoku.docx
└── 📁 venv/                 # Virtual environment (if created)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install development dependencies: `pip install -r requirements.txt`
6. Make your changes
7. Run tests: `pytest`
8. Run linting: `flake8 sudoku.py test_sudoku.py`
9. Format code: `black sudoku.py test_sudoku.py`
10. Commit your changes: `git commit -m "Add feature"`
11. Push to the branch: `git push origin feature-name`
12. Open a Pull Request

### Code Style

This project uses:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pytest** for testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📈 Changelog

### Version 2.0.0 (2024)

- Complete rewrite with modern Python features
- Added comprehensive type hints
- Implemented dataclasses and enums
- Added extensive test suite (27 tests)
- Improved algorithm efficiency (4000x faster)
- Added difficulty classification
- Enhanced documentation
- Cleaned up file structure
- Added performance benchmarks

### Version 1.0.0 (2015)

- Initial implementation
- Basic Sudoku generation and solving
- Multiple difficulty levels

## 🙏 Acknowledgments

- Original implementation by Joe Carlson (2015)
- Modernized and enhanced in 2024
- Inspired by classic Sudoku solving techniques

## 📞 Contact

- **Author**: Joe Carlson
- **Website**: [www.callmejoe.net](https://www.callmejoe.net)
- **GitHub**: [@joecarlson](https://github.com/joecarlson)

## 🎯 Roadmap

- [ ] GUI interface
- [ ] Web application
- [ ] Mobile app
- [ ] Advanced solving techniques
- [ ] Puzzle import/export
- [ ] Statistics and analytics

*Made with ❤️ and Python*
