def sudoku_solver(nine_array):
    """
    nine_array: list of 81 ints, 0 = unknown
    
    sudobyte     = a digit (1-9) being tracked
    sudobit      = a cell index (0-80) - since it is a 9x9 (81) grid, we can treat it as a flat array for easier indexing
    sudopeer     = a peer cell in same row/col/box
    sudobyte_counts = {digit: remaining placements needed}
    """

    # dictionary of remaining candidates for each cell: set of possible digits
    sudogrid = []
    for val in nine_array:
        if val == 0:
            sudogrid.append(set(range(1, 10)))   # all digits still candidates so far
        else:
            sudogrid.append({val})               # already solved sudobit so only one candidate

    # sudobyte_counts: how many more times each digit still needs to be placed (initially 9 minus how many times it already appears)
    sudobyte_counts = {d: 9 - sum(1 for s in sudogrid if s == {d}) for d in range(1, 10)}

    # a peer is any cell that shares a row, column, or 3x3 box with the sudobit of interest. This is important for elimination and hidden single strategies.
    def get_peers(sudobit):
        r, c = sudobit // 9, sudobit % 9 # using the whole number 0-80 as index, calculate row and column- this will help me repeat the same index to check the row and column and box
        box_r, box_c = (r // 3) * 3, (c // 3) * 3 # calculate the top-left corner of the 3x3 box
        peers = set() # collect all peers in the same row, column, and box- using set to avoid duplicates
        for i in range(81): #                  
            if i != sudobit: # skip the sudobit itself since it can't be its own peer
                ri, ci = i // 9, i % 9 # calculate row and column for the peer candidate- ri is the row index and ci is the column index for the peer candidate
                if ri == r or ci == c or (box_r <= ri < box_r+3 and box_c <= ci < box_c+3): # check if the peer candidate is in the same row, column, or box as the sudobit
                    peers.add(i) # so we are only adding the peer candidate to the peers set if it shares a row, column, or box with the sudobit. 
        return peers

    def get_units(sudobit): # a unit is a collection of 9 cells that must contain all digits 1-9 exactly once (a row, column, or box). This is important for the hidden single strategy, where we look for a digit that can only go in one cell within a unit.
        r, c = sudobit // 9, sudobit % 9 
        box_r, box_c = (r // 3) * 3, (c // 3) * 3
        row  = [r*9 + ci for ci in range(9)] # calculate the indices of the cells in the same row as the sudobit- we are using r*9 to get to the start of the row and then adding ci (0-8) to get each cell in that row
        col  = [ri*9 + c for ri in range(9)] # calculate the indices of the cells in the same column as the sudobit- we are using c to get to the start of the column and then adding ri (0-8) to get each cell in that column  
        box  = [
            (box_r + dr)*9 + (box_c + dc) 
            for dr in range(3) for dc in range(3)
        ] # calculate the indices of the cells in the same 3x3 box as the sudobit- we are using box_r and box_c to get to the top-left corner of the box and then adding dr (0-2) and dc (0-2) to get each cell in that box
        return [row, col, box]

    #Main loop: digit-first, most constrained sudobyte first
    changed = True 
    while changed: 
        changed = False 

        # Sort digits by how few placements remain (my strategy is to start with most placed items first, since they have fewer options and can lead to more eliminations)
        digit_order = sorted(range(1, 10), key=lambda d: sudobyte_counts[d])

        for sudobyte in digit_order:  
            if sudobyte_counts[sudobyte] == 0: 
                continue # already fully placed, skip - this is why keeping track of how many placements remain for each digit, so we can skip fully placed digits and focus on the ones that still need to be placed rather than mixing things up by trying to place already fully placed digits which would lead to contradictions and wasted effort

            for sudobit in range(81):
                if sudobyte not in sudogrid[sudobit]:
                    continue
                if len(sudogrid[sudobit]) == 1:
                    continue  # already solved

                # Peer elimination: if sudobyte is placed in any sudopeer, remove from sudobit
                for sudopeer in get_peers(sudobit):
                    if sudogrid[sudopeer] == {sudobyte}:
                        sudogrid[sudobit].discard(sudobyte) # if the sudopeer is already solved with sudobyte, then we can eliminate sudobyte from the candidates of sudobit. We use discard to remove sudobyte from the set of candidates for sudobit, and if it was not present, it does nothing.
                        changed = True # if we made any changes in this iteration, we will need to loop again to check for new deductions based on the updated grid. Note: a change must be made everytime. If not, then the whole board is solved.
                        break

                # Hidden single: sudobyte has only one candidate cell in this unit
                for unit in get_units(sudobit):
                    candidates = [idx for idx in unit if sudobyte in sudogrid[idx]]
                    if len(candidates) == 1 and len(sudogrid[candidates[0]]) > 1:
                        sudogrid[candidates[0]] = {sudobyte}
                        sudobyte_counts[sudobyte] -= 1
                        changed = True

    # Return result
    if all(len(s) == 1 for s in sudogrid):
        return [list(s)[0] for s in sudogrid]
    else:
        return None  # needs backtracking for very hard puzzles


print(sudoku_solver([5, 3, 0, 0, 7, 0, 0, 0, 0,
                    6, 0, 0, 1, 9, 5, 0, 0, 0,
                    0, 9, 8, 0, 0, 0, 0, 6, 0,
                    8, 0, 0, 0, 6, 0, 0, 0, 3,
                    4, 0, 0, 8, 0, 3, 0, 0, 1,
                    7, 0, 0, 0, 2, 0, 0, 0, 6,
                    0, 6, 0, 0, 0, 0, 2, 8, 0,
                    0, 0, 0, 4, 1, 9, 0, 0, 5,
                    0, 0, 0, 0, 8, 0, 0, 7, 9]))