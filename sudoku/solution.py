assignments = []
rows = "ABCDEFGHI"
cols = "123456789"

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

boxes = cross(rows, cols)
unitlist = ([cross(r, cols) for r in rows] + 
    [cross(rows, c) for c in cols] + 
    [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')] +
    [[rows[idx] + cols[idx] for idx in range(9)]] +
    [[rows[8 - idx] + cols[idx] for idx in range(9)]])
units = dict((s, [u for u in unitlist if s in u]) 
    for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s]))
    for s in boxes)

def is_valid_sudoku(values, verbose):
    """
    this function is used to validate that a set of values 
    is a valid solution
    """
    # first check for single digits
    for box, value in values.items():
        if len(value) > 1:
            if verbose: print("box " + box + " has more than one value: " + str(value))
            return False
        if value not in cols:
            if verbose: print("box " + box + " has a non-digit value: " + str(value))
            return False
        # check peer groups
        for peer in peers[box]:
            if values[peer] == value:
                if verbose: print("box " + box + " hassame value as peer: " + peer)
                return False
    return True

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # get every non-determined value
    possible_twins = [box for box in values.keys() if len(values[box]) == 2]
    # for those values, create a list of dictionaries with the twins and 
    # the peer group
    naked_twins = [{"twins": [twin1, twin2], "unit": unit, "value": values[twin1]} for twin1 in possible_twins  
                      for unit in units[twin1] 
                      for twin2 in unit if set(values[twin1]) == set(values[twin2]) 
                      and twin1 != twin2 ]
    for naked_twin in naked_twins:
        unit = naked_twin["unit"]
        peers = set(unit) - set(naked_twin["twins"])
        for peer in peers:
            for digit in naked_twin["value"]:
                values = assign_value(values, peer, values[peer].replace(digit, '')) 
    
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    if len(grid) != 81:
        raise Exception("input doesn't have 81 squares")
    lgrid = [d if (d != '.' and d != '0') else '123456789' for d in grid]
    values =  dict(zip(boxes, lgrid))
    for box, value in values.items():
        values = assign_value(values, box, value)
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
            for c in cols))
        if r in 'CF': print(line)

def eliminate(values):
    """ 
    eliminate any solved values from that box's
    peer group
    """
    for box, digits in values.items():
        if len(digits) == 1:
            for peer in peers[box]:
                values = assign_value(values, peer, values[peer].replace(digits, ''))
    return values

def only_choice(values):
    """
    if a digit is the only option within a 
    given unit, then assign it accordingly.
    if that digit is not the "only choice"
    break early
    """
    for unit in unitlist:
        # in which indexes can a digit appear
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """ 
    reduce_puzzle tries to iteratively apply eliminate and only 
    choice to a given puzzle. It operates on a copy in the event 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # First eliminate solved digits from that box's peer group
        values = eliminate(values)
        # Apply only choice
        values = only_choice(values)
        # Apply naked twins
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle
    reduced = reduce_puzzle(values)
    if not reduced :
        return False
    # Check if we've solved the puzzle
    n_solved = 0
    for v in reduced.values():
        if len(v) == 1:
            n_solved += 1
    if n_solved == 81:
        if is_valid_sudoku(reduced, False):
            return reduced
        return False
    values = reduced
    # Pick a minimum
    _, pick = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Recurse, breaking if we find a valid answer
    for digit in values[pick]:
        values_copy = values.copy()
        values_copy[pick] = digit
        result = search(values_copy)
        if result:
            if is_valid_sudoku(result, False):
                return result
            return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # first parse the grid to get the values
    values = grid_values(grid)
    # next call search
    result = search(values)
    if not result:
        raise Exception("grid wasn't solvable")
    return result
    
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
