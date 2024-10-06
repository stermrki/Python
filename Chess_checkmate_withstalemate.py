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

# Mapping piece types to their abbreviations for display
chess_pieces = {
    'king': 'K',
    'queen': 'Q',
    'rook': 'R',
    'bishop': 'B',
    'knight': 'N',
    'pawn': 'P'
}

# Step 2: Print game instructions for the user
def print_instructions():
    """
    Prints the game instructions to guide the user on how to play.
    """
    instructions = """
Welcome to the Chess Checkmate Detection Game!

Here's how to play:
1. You will place a white king on the board by entering its position.
   - Format: "king position" (e.g., "king e4").
2. After placing the white king, you will add black pieces one by one.
   - You can add up to 8 pawns, 2 bishops, 2 rooks, 2 knights, and only one queen or king.
   - Format: "piece position" (e.g., "queen h5" or "rook a3").
3. Once you have added all black pieces, type "done" to finish.
4. The game will then determine if the black pieces can checkmate the white king based on their positions.

Remember:
- Coordinates use letters a-h (columns) and numbers 1-8 (rows).
- Ensure positions are valid and no two pieces occupy the same square.

Good luck!
"""
    print(instructions)

# Helper function to parse and validate position
def parse_position(position):
    """
    Parses the position string and converts it to numerical coordinates.

    Args:
        position (str): The position string (e.g., 'e4').

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
def get_piece_and_position(prompt, allowed_pieces, board, existing_piece_counts=None, max_counts=None):
    """
    Prompts the user to input a piece and its position, validating the input.

    Args:
        prompt (str): The input prompt message.
        allowed_pieces (list): List of allowed piece types.
        board (dict): Current state of the chessboard.
        existing_piece_counts (dict, optional): Current counts of each piece type.
        max_counts (dict, optional): Maximum allowed counts for each piece type.

    Returns:
        tuple: (piece, position) if valid, else ('done', 'done').
    """
    while True:
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
    Handles user input for placing white and black pieces on the board.

    Args:
        board (dict): The current state of the chessboard.

    Returns:
        tuple: (white_piece_type, white_piece_position, black_pieces)
    """
    # Place white king
    white_piece_type, white_piece_position = place_white_piece(board)

    # Place black pieces
    black_pieces = place_black_pieces(board)

    return white_piece_type, white_piece_position, black_pieces

def place_white_piece(board):
    """
    Prompts the user to place the white king on the board.

    Args:
        board (dict): The current state of the chessboard.

    Returns:
        tuple: (piece_type, position)
    """
    while True:
        piece, position = get_piece_and_position(
            "Enter your white piece (king) and its position (e.g., 'king e4'): ",
            allowed_pieces=['king'],
            board=board
        )
        if piece == 'done':
            print("You must place a white king before proceeding.")
            continue
        board[position] = f'White {chess_pieces[piece]}'
        print(f"You placed a White {piece} at {position}.")
        return piece, position

def place_black_pieces(board):
    """
    Prompts the user to place black pieces on the board.

    Args:
        board (dict): The current state of the chessboard.

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
    max_piece_counts = {
        'pawn': 8,
        'bishop': 2,
        'rook': 2,
        'knight': 2,
        'queen': 1,
        'king': 1
    }
    allowed_pieces = ['pawn', 'bishop', 'rook', 'knight', 'queen', 'king']

    while True:
        piece, position = get_piece_and_position(
            "Enter a black piece and its position (e.g., 'queen h5') or type 'done' to finish: ",
            allowed_pieces=allowed_pieces,
            board=board,
            existing_piece_counts=black_piece_counts,
            max_counts=max_piece_counts
        )
        if piece == 'done':
            if black_pieces:
                break
            else:
                print("You must add at least one black piece before typing 'done'.")
                continue

        # Check for the black king proximity rule
        if piece == 'king':
            if black_piece_counts['king'] >= 1:
                print("Maximum number of kings (1) reached. Cannot add more kings.")
                continue
            # Find the white king's position
            white_king_pos = next((pos for pos, val in board.items() if val and val.startswith('White K')), None)
            if white_king_pos and is_king_adjacent(position, white_king_pos):
                print("Invalid placement. The black king cannot be placed next to the white king.")
                continue

        # Place the piece
        board[position] = f'Black {chess_pieces[piece]}'
        black_pieces.append((piece, position))
        black_piece_counts[piece] += 1
        print(f"You placed a Black {piece} at {position}.")

    return black_pieces

# Helper function to check if kings are adjacent
def is_king_adjacent(black_king_position, white_king_position):
    """
    Checks if the black king is adjacent to the white king.

    Args:
        black_king_position (str): Position of the black king (e.g., 'e5').
        white_king_position (str): Position of the white king (e.g., 'e4').

    Returns:
        bool: True if adjacent, False otherwise.
    """
    x_w, y_w = parse_position(white_king_position)
    x_b, y_b = parse_position(black_king_position)
    if x_w is None or y_w is None or x_b is None or y_b is None:
        return False
    return abs(x_w - x_b) <= 1 and abs(y_w - y_b) <= 1

# Step 4: Determine if the black pieces can checkmate the white king
def determine_checkmate(board, white_piece_position, black_pieces):
    """
    Determines if the black pieces can checkmate the white king based on their positions.

    Args:
        board (dict): The current state of the chessboard.
        white_piece_position (str): The position of the white king (e.g., 'e4').
        black_pieces (list): A list of tuples representing black pieces and their positions.

    Returns:
        tuple: (status, escape_positions)
               status: 'checkmate', 'check', 'stalemate', or 'safe'
               escape_positions: List of positions the king can escape to (if any)
    """
    white_king_pos = white_piece_position
    x_w, y_w = parse_position(white_king_pos)

    if x_w is None or y_w is None:
        print("Invalid white king position.")
        return 'error', []

    def attacks(piece, pos, target_x, target_y):
        """
        Determines if a black piece attacks a given square.

        Args:
            piece (str): The type of the black piece (e.g., 'queen').
            pos (str): The position of the black piece (e.g., 'h5').
            target_x (int): X-coordinate of the target square.
            target_y (int): Y-coordinate of the target square.

        Returns:
            bool: True if the piece attacks the target square, False otherwise.
        """
        x, y = parse_position(pos)
        if x is None or y is None:
            return False

        dx = target_x - x
        dy = target_y - y

        if piece == 'queen':
            if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                return is_path_clear(x, y, target_x, target_y)
        elif piece == 'rook':
            if dx == 0 or dy == 0:
                return is_path_clear(x, y, target_x, target_y)
        elif piece == 'bishop':
            if abs(dx) == abs(dy):
                return is_path_clear(x, y, target_x, target_y)
        elif piece == 'knight':
            if (abs(dx), abs(dy)) in [(1, 2), (2, 1)]:
                return True
        elif piece == 'pawn':
            # Black pawns move downward (from y to y-1)
            if dy == -1 and abs(dx) == 1:
                return True
        elif piece == 'king':
            if abs(dx) <= 1 and abs(dy) <= 1:
                return True
        return False

    def is_path_clear(x_start, y_start, x_end, y_end):
        """
        Checks if the path between two squares is clear of other pieces.

        Args:
            x_start (int): X-coordinate of the starting square.
            y_start (int): Y-coordinate of the starting square.
            x_end (int): X-coordinate of the ending square.
            y_end (int): Y-coordinate of the ending square.

        Returns:
            bool: True if the path is clear, False otherwise.
        """
        step_x = 0
        step_y = 0
        if x_end > x_start:
            step_x = 1
        elif x_end < x_start:
            step_x = -1
        if y_end > y_start:
            step_y = 1
        elif y_end < y_start:
            step_y = -1

        current_x = x_start + step_x
        current_y = y_start + step_y

        while (current_x != x_end or current_y != y_end):
            pos = f"{chr(current_x + ord('a'))}{current_y + 1}"
            if board.get(pos) is not None:
                return False  # Path is blocked
            current_x += step_x
            current_y += step_y

        return True  # Path is clear

    def is_in_check():
        """
        Checks if the white king is currently in check.

        Returns:
            bool: True if in check, False otherwise.
        """
        for piece, pos in black_pieces:
            if attacks(piece, pos, x_w, y_w):
                return True
        return False

    def can_escape():
        """
        Determines if the white king can escape to any adjacent square.

        Returns:
            list: List of positions the king can safely move to.
        """
        escape_positions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Current position
                new_x = x_w + dx
                new_y = y_w + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    escape_pos = f"{chr(new_x + ord('a'))}{new_y + 1}"
                    # Check if the square is occupied by a white piece (only white king exists)
                    if board[escape_pos] is not None and board[escape_pos].startswith('White'):
                        continue
                    if board[escape_pos] is None:
                        # Square is empty, check if it's under attack
                        under_attack = False
                        for piece, pos in black_pieces:
                            if attacks(piece, pos, new_x, new_y):
                                under_attack = True
                                break
                        if not under_attack:
                            escape_positions.append(escape_pos)
                    elif 'Black' in board[escape_pos]:
                        # Square is occupied by a black piece, simulate capturing
                        # Find the corresponding black piece tuple
                        captured_piece_tuple = next((bp for bp in black_pieces if bp[1] == escape_pos), None)
                        if captured_piece_tuple:
                            temp_black_pieces = black_pieces.copy()
                            temp_black_pieces.remove(captured_piece_tuple)

                            # Simulate capturing the piece
                            original_piece = board[escape_pos]
                            board[escape_pos] = 'White K'
                            board[white_piece_position] = None

                            # Check if the king is still in check after capturing
                            in_check_after_capture = False
                            for piece_b, pos_b in temp_black_pieces:
                                if attacks(piece_b, pos_b, new_x, new_y):
                                    in_check_after_capture = True
                                    break

                            # Restore the board
                            board[escape_pos] = original_piece
                            board[white_piece_position] = 'White K'

                            if not in_check_after_capture:
                                escape_positions.append(escape_pos)
        return escape_positions

    def is_checkmate():
        """
        Determines if the white king is in checkmate.

        Returns:
            bool: True if checkmate, False otherwise.
        """
        if not is_in_check():
            return False
        escape_pos = can_escape()
        return len(escape_pos) == 0

    def is_stalemate():
        """
        Determines if the game is in stalemate.

        Returns:
            bool: True if stalemate, False otherwise.
        """
        if is_in_check():
            return False
        escape_pos = can_escape()
        return len(escape_pos) == 0

    if is_checkmate():
        return 'checkmate', []
    elif is_in_check():
        escape_pos = can_escape()
        return 'check', escape_pos
    elif is_stalemate():
        return 'stalemate', []
    else:
        return 'safe', []

# Step 5: Print the final board state
def print_board(board):
    """
    Prints the chess board with pieces in their respective positions.

    Args:
        board (dict): The current state of the chessboard.
    """
    # Dictionary to map piece types to their abbreviations for board display
    piece_abbr_map = {
        'king': 'K',
        'queen': 'Q',
        'rook': 'R',
        'bishop': 'B',
        'knight': 'N',
        'pawn': 'P'
    }

    print("\nFinal Board State:")
    # Iterate over the rows from 8 to 1
    for row in range(8, 0, -1):
        row_str = f"{row} "  # Add row numbers
        for col in 'abcdefgh':
            pos = f"{col}{row}"
            piece = board[pos]
            if piece is None:
                row_str += ". "
            else:
                parts = piece.split()
                if len(parts) != 2:
                    # Invalid piece format; treat as empty
                    row_str += ". "
                    continue
                color, piece_code = parts
                piece_type = {
                    'K': 'king',
                    'Q': 'queen',
                    'R': 'rook',
                    'B': 'bishop',
                    'N': 'knight',
                    'P': 'pawn'
                }.get(piece_code.upper(), '')
                if not piece_type:
                    # Unknown piece type; treat as empty
                    row_str += ". "
                    continue
                # Get the abbreviation for the piece type
                piece_abbr = piece_abbr_map.get(piece_type, '?')
                if color.lower() == 'black':
                    # Print Black pieces in red, lowercase
                    row_str += f"\033[31m{piece_abbr.lower()}\033[0m "
                elif color.lower() == 'white':
                    # Print White pieces normally, uppercase
                    row_str += f"{piece_abbr} "
                else:
                    # Unknown color; treat as empty
                    row_str += ". "
        print(row_str)
    # Print column labels
    print("  a b c d e f g h\n")

# Step 6: Main game loop
def main():
    """
    Main function to execute the Chess Checkmate Detection Game.
    """
    board = create_chessboard()
    print_instructions()
    white_piece_type, white_piece_position, black_pieces = get_user_input(board)

    # Determine if black pieces can checkmate the white king
    status, escape_positions = determine_checkmate(board, white_piece_position, black_pieces)

    # Output the results
    if status == 'checkmate':
        print("\nCheckmate! The black pieces have successfully checkmated the white king.")
    elif status == 'check':
        print("\nThe white king is under check.")
        if escape_positions:
            print("Possible escape positions:", ', '.join(escape_positions))
        else:
            print("No escape positions available.")
    elif status == 'stalemate':
        print("\nStalemate! The game ends in a draw.")
    elif status == 'safe':
        print("\nThe white king is not under check and is safe.")
    else:
        print("\nAn error occurred during checkmate determination.")

    print_board(board)

# Start the game
if __name__ == "__main__":
    main()
