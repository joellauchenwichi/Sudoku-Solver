## How the Algorithm Works

The `sudoku_solver` uses a **constraint propagation approach** focusing on eliminating candidates and unit-based single placement (hidden singles). Instead of iterating cell-by-cell, it operates with a **digit-first strategy** prioritizing the most constrained digits.

---

### Core Data Structures

* **`sudogrid`**: A flat list of 81 sets representing the 9x9 board. Each set contains all valid remaining candidate digits for that specific cell.
* **`sudobyte_counts`**: A dictionary tracking how many remaining placements are required for each digit (1 through 9).
* **`sudobit`**: An integer index (0–80) representing a cell in the flattened 9x9 grid.
* **`sudobyte`**: The specific digit (1–9) currently being processed.

---

### Key Components & Helpers

1. **`get_peers(sudobit)`**
   Calculates all peer cell indices that share the same row, column, or $3 \times 3$ subgrid box with the target cell (`sudobit`).
2. **`get_units(sudobit)`**
   Returns the three units belonging to a cell: its row list, column list, and $3 \times 3$ box list.

---

### Solving Logic (Main Loop)

The algorithm loops continuously while candidates can still be eliminated or values placed:

1. **Digit-First Ordering**
   Sorts digits by `sudobyte_counts` in ascending order. Digits with the fewest remaining placements are checked first because they offer the tightest constraints and higher likelihood of immediate deductions.

2. **Peer Elimination**
   Iterates through candidate cells for a given digit. If any peer cell is already solved with `sudobyte`, `sudobyte` is removed from the candidate set of the current cell.

3. **Hidden Single Detection**
   Checks each unit (row, column, 3X3 box) associated with a cell. If `sudobyte` can only fit into **one** candidate cell within that unit, that cell is solved with `sudobyte`.

---

### Limitations

* **Deterministic Deductions Only**: This solver purely relies on logical elimination and hidden singles. 
* **No Backtracking**: If a puzzle requires guessing or deep depth-first search (e.g., hard/expert-level Sudokus), the function returns `None`.

---

### Example Usage

```python
# Unsolved board represented as a flat list of 81 integers (0 = empty cell)
board = [
    5, 3, 0, 0, 7, 0, 0, 0, 0,
    6, 0, 0, 1, 9, 5, 0, 0, 0,
    0, 9, 8, 0, 0, 0, 0, 6, 0,
    8, 0, 0, 0, 6, 0, 0, 0, 3,
    4, 0, 0, 8, 0, 3, 0, 0, 1,
    7, 0, 0, 0, 2, 0, 0, 0, 6,
    0, 6, 0, 0, 0, 0, 2, 8, 0,
    0, 0, 0, 4, 1, 9, 0, 0, 5,
    0, 0, 0, 0, 8, 0, 0, 7, 9
]

solution = sudoku_solver(board)
print(solution)
