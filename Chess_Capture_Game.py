# Step 1: Define the chessboard and pieces
def create_chessboard():
    """
    Creates an 8x8 chessboard with positions labeled from 'a1' to 'h8'.
    
    Returns:
        dict: A dictionary representing the chessboard with all positions initialized to None.
    """
    rows = ['1', '2', '3', '4', '5', '6', '7', '8']
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    board = {}
    for col in cols:
        for row in rows:
            board[col + row] = None  # No piece at the start
    return board

# Define chess pieces and their movements
chess_pieces = {
    'king': 'King',      # King moves one square in any direction
    'queen': 'Queen',    # Queen moves diagonally, horizontally, or vertically
    'rook': 'Rook',      # Rook moves horizontally or vertically
    'bishop': 'Bishop',  # Bishop moves diagonally
    'knight': 'Knight',  # Knight moves in an L-shape
    'pawn': 'Pawn'       # Pawn moves one square forward (with exceptions)
}

# Step 2: Print game instructions for the user
def print_instructions():
    """
    Shows the instructions to help the user play the game.
    """
    instructions = """
Welcome to the Chess Capture Game!

Here's how to play:
1. First, you will choose a white piece (either a king or a pawn) and enter its position on the board.
   - The format should be: "piece position" (e.g., "king e4" or "pawn b2").
   - Example: "king e1" places a White King at position e1.
   - Note: White pawns move upwards (from row 2 to row 8).

2. After placing the white piece, you will add black pieces one by one.
   - You can add up to 16 black pieces with no limitations on specific piece types.
   - The format for adding a black piece is the same: "piece position" (e.g., "queen h5" or "rook a3").
   - Example: "pawn d7" places a Black Pawn at position d7.

3. Once you have added all black pieces, you can type "done" to finish.

4. The game will then calculate and show which black pieces the white piece can overtake based on their positions.

Remember:
- Coordinates are entered using letters a-h (columns) and numbers 1-8 (rows).
- Please make sure to follow the format and ensure positions are valid.

Good luck!
"""
    print(instructions)

# Helper function to check and convert position
def parse_position(position):
    """
    Checks the position string and converts it to numerical coordinates.
    
    Returns:
        tuple: (x, y) coordinates if valid, else (None, None).
    """
    if len(position) != 2:
        return None, None
    col, row = position[0], position[1]
    if col not in 'abcdefgh' or row not in '12345678':
        return None, None
    x = ord(col) - ord('a')
    y = int(row) - 1
    return x, y

# Helper function for user input
def get_piece_and_position(prompt, allowed_pieces, board, existing_piece_counts=None, max_counts=None, total_pieces=None, max_total=16):
    """
    Asks the user to input a piece and its position, checking if the input is valid.
    
    Returns:
        tuple: (piece, position) if valid, else ('done', 'done').
    """
    while True:
        if total_pieces is not None and total_pieces >= max_total:
            print(f"You have reached the maximum number of black pieces ({max_total}).")
            return 'done', 'done'
        
        user_input = input(prompt).strip().lower()
        if user_input == 'done':
            return 'done', 'done'
        parts = user_input.split()
        if len(parts) != 2:
            print("Please enter exactly two values: 'piece position' (e.g., 'queen h5').")
            continue
        piece, position = parts
        if piece not in allowed_pieces:
            print(f"Invalid piece. Allowed pieces: {', '.join(allowed_pieces)}.")
            continue
        if position not in board:
            print("Invalid position. Please enter a position like 'e4'.")
            continue
        if board[position] is not None:
            print("Position already taken. Choose a different position.")
            continue
        if existing_piece_counts and max_counts:
            if existing_piece_counts.get(piece, 0) >= max_counts.get(piece, 1):
                print(f"You cannot place more than {max_counts[piece]} {piece}(s).")
                continue
        return piece, position

# Step 3: Get user input for white and black pieces
def get_user_input(board):
    """
    Manages user input for placing white and black pieces on the board.
    
    Returns:
        tuple: (white_piece_type, white_piece_position, black_pieces)
    """
    # Place white piece
    white_piece_type, white_piece_position = place_white_piece(board)
    
    # Place black pieces
    black_pieces = place_black_pieces(board)
    
    return white_piece_type, white_piece_position, black_pieces

def place_white_piece(board):
    """
    Asks the user to place the white piece on the board.
    
    Returns:
        tuple: (piece_type, position)
    """
    while True:
        piece, position = get_piece_and_position(
            "Enter your white piece (king or pawn) and its position (e.g., 'king e4'): ",
            allowed_pieces=['king', 'pawn'],
            board=board
        )
        if piece == 'done':
            print("You must place a white piece before proceeding.")
            continue
        board[position] = f'White {chess_pieces[piece]}'
        print(f"You placed a White {chess_pieces[piece]} at {position}.")
        return piece, position

def place_black_pieces(board):
    """
    Asks the user to place black pieces on the board.
    
    Returns:
        list: A list of tuples representing black pieces and their positions.
    """
    black_pieces = []
    black_piece_counts = {
        'pawn': 0,
        'bishop': 0,
        'rook': 0,
        'knight': 0,
        'queen': 0,
        'king': 0
    }
    allowed_pieces = ['pawn', 'bishop', 'rook', 'knight', 'queen', 'king']
    max_total_pieces = 16  # Maximum number of black pieces allowed
    
    while True:
        current_total = len(black_pieces)
        piece, position = get_piece_and_position(
            "Enter a black piece and its position (e.g., 'queen h5') or type 'done' to finish: ",
            allowed_pieces=allowed_pieces,
            board=board,
            existing_piece_counts=None,  # No per-piece count limits
            max_counts=None,
            total_pieces=current_total,
            max_total=max_total_pieces
        )
        if piece == 'done':
            if black_pieces:
                break
            else:
                print("You must add at least one black piece before typing 'done'.")
                continue
        board[position] = f'Black {chess_pieces[piece]}'
        black_pieces.append((piece, position))
        print(f"You placed a Black {chess_pieces[piece]} at {position}.")
    
    return black_pieces

# Step 4: Determine which black pieces can be overtaken by the white piece
def determine_overtakes(white_piece_type, white_piece_position, black_pieces):
    """
    Checks which black pieces can be overtaken by the white piece based on their positions.
    
    Returns:
        list: A list of black pieces that can be overtaken.
    """
    overtakes = []
    x_w, y_w = parse_position(white_piece_position)
    if x_w is None or y_w is None:
        print("Invalid white piece position.")
        return overtakes
    
    # Check for overtaking moves for each black piece
    for piece, position in black_pieces:
        x_b, y_b = parse_position(position)
        if x_b is None or y_b is None:
            print(f"Invalid position for black {piece} at {position}. Skipping.")
            continue

        # Determine overtaking ability based on white piece type
        if white_piece_type == 'king':
            if abs(x_b - x_w) <= 1 and abs(y_b - y_w) <= 1:  # King can move to any adjacent square
                overtakes.append(f'Black {chess_pieces[piece]} ({position})')
        elif white_piece_type == 'pawn':
            # White pawns move upwards: y_b - y_w should be 1
            if (abs(x_b - x_w) == 1 and y_b - y_w == 1):  # Pawn captures diagonally forward
                overtakes.append(f'Black {chess_pieces[piece]} ({position})')
    
    return overtakes  # Return the list of overtakes

# Main function to run the game
def main():
    """
    Main function to execute the Chess Capture Game.
    """
    # Step 1: Create the chessboard
    chessboard = create_chessboard()

    # Step 2: Print instructions
    print_instructions()

    # Step 3: Get user input for the white and black pieces
    white_piece_type, white_piece_position, black_pieces = get_user_input(chessboard)

    # Step 4: Determine which black pieces can be overtaken by the white piece
    overtakes = determine_overtakes(white_piece_type, white_piece_position, black_pieces)

    # Output the results
    if overtakes:
        print(f"\nThe following black pieces can be overtaken by the White {chess_pieces[white_piece_type]}:")
        for overtake in overtakes:
            print(overtake)
    else:
        print(f"\nNo black pieces can be overtaken by the White {chess_pieces[white_piece_type]}.")

# Run the main function
if __name__ == "__main__":
    main()
