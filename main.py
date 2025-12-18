from random import randrange  # Import the randrange function to pick random numbers for the computer's move.


def display_board(board):
    """Print a human-readable version of the current board."""
    horizontal_border = "+-------+-------+-------+"  # A reusable border string that outlines each row.
    empty_row = "|       |       |       |"  # A spacer line to pad the cells for readability.

    for row in board:  # Iterate through each of the three board rows.
        print(horizontal_border)  # Draw the top border for the current row.
        print(empty_row)  # Add a blank padded line above the cell content.
        print("|   " + "   |   ".join(str(cell) for cell in row) + "   |")  # Show the row's values separated by vertical lines.
        print(empty_row)  # Add a blank padded line below the cell content.
    print(horizontal_border)  # Close the board with a final border line.


def make_list_of_free_fields(board):
    """Return a list of coordinates for all squares that are not yet taken."""
    free_fields = []  # Start with an empty list to collect available positions.
    for row_idx, row in enumerate(board):  # Loop over each row along with its index.
        for col_idx, cell in enumerate(row):  # Loop over each cell in the current row with its column index.
            if cell not in ("X", "O"):  # Check whether the square is still a number (meaning it's empty).
                free_fields.append((row_idx, col_idx))  # Record the row and column of this empty square.
    return free_fields  # Hand back every free coordinate so other functions can use them.


def victory_for(board, sign):
    """Check whether the provided sign ('X' or 'O') has a winning line."""
    win_positions = [  # Predefine every combination of coordinates that forms a win.
        # Rows
        [(0, 0), (0, 1), (0, 2)],  # Top row
        [(1, 0), (1, 1), (1, 2)],  # Middle row
        [(2, 0), (2, 1), (2, 2)],  # Bottom row
        # Columns
        [(0, 0), (1, 0), (2, 0)],  # Left column
        [(0, 1), (1, 1), (2, 1)],  # Middle column
        [(0, 2), (1, 2), (2, 2)],  # Right column
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],  # Top-left to bottom-right diagonal
        [(0, 2), (1, 1), (2, 0)],  # Top-right to bottom-left diagonal
    ]

    for positions in win_positions:  # Walk through each possible winning combination.
        if all(board[row][col] == sign for row, col in positions):  # Confirm every square in this combo matches the sign.
            return True  # Immediately report a win when a full line is found.
    return False  # If no combos match, the player has not won yet.


def enter_move(board):
    """Ask the human player for a move and place their 'O' on the board."""
    while True:  # Repeat until the player provides a valid input.
        move_input = input("Enter your move: ")  # Read raw input from the keyboard.
        try:
            move = int(move_input)  # Attempt to convert the text to an integer representing the chosen square.
        except ValueError:  # If conversion fails, the user didn't type a proper number.
            print("Please enter a valid number between 1 and 9.")  # Guide the user to provide correct input.
            continue  # Restart the loop to ask again.

        if move < 1 or move > 9:  # Ensure the chosen number maps to a board position.
            print("The move must be between 1 and 9.")  # Explain the allowed range.
            continue  # Restart the loop for another try.

        row = (move - 1) // 3  # Convert the 1-9 choice to a zero-based row index.
        col = (move - 1) % 3  # Convert the same choice to a zero-based column index.

        if board[row][col] in ("X", "O"):  # Check whether that square is already taken.
            print("That square is already occupied. Choose another one.")  # Alert the user and prompt again.
            continue  # Loop back for a new selection.

        board[row][col] = "O"  # Place the human player's marker on the chosen square.
        break  # Exit the loop because the move was successful.


def draw_move(board):
    """Let the computer choose a random free square and place an 'X'."""
    free_fields = make_list_of_free_fields(board)  # Collect all currently open squares.
    if not free_fields:  # If nothing is available, there is no move to make.
        return  # Exit without modifying the board.

    row, col = free_fields[randrange(len(free_fields))]  # Pick a random available square by index.
    board[row][col] = "X"  # Place the computer's marker on that square.


def main():
    """Run the main game loop that alternates between the player and the computer."""
    board = [  # Build the starting board layout with numbers for empty squares and an 'X' in the center.
        [1, 2, 3],
        [4, "X", 6],
        [7, 8, 9],
    ]

    while True:  # Continue playing until a win or tie ends the game.
        display_board(board)  # Show the current board to the player before each action.

        if victory_for(board, "X"):  # Check if the computer has already won.
            print("The computer won!")  # Announce the result to the player.
            break  # End the game loop.
        if victory_for(board, "O"):  # Check if the player has already won.
            print("You won!")  # Celebrate the player's victory.
            break  # End the game loop.

        if not make_list_of_free_fields(board):  # If there are no open squares, the game must be a tie.
            print("It's a tie!")  # Inform the player of the draw.
            break  # Exit the loop because the game is finished.

        enter_move(board)  # Ask the player for their move and update the board.

        if victory_for(board, "O"):  # After the player's move, check again for a win.
            display_board(board)  # Show the final board state.
            print("You won!")  # Confirm the player's victory.
            break  # Stop the game loop.

        if not make_list_of_free_fields(board):  # If the board filled up after the player's move, it's a tie.
            display_board(board)  # Display the filled board.
            print("It's a tie!")  # Report the tie.
            break  # End the game loop.

        draw_move(board)  # Let the computer make its move.

        if victory_for(board, "X"):  # Check if the computer's move created a winning line.
            display_board(board)  # Show the board with the winning move.
            print("The computer won!")  # Inform the player of the loss.
            break  # End the game loop.

        if not make_list_of_free_fields(board):  # If the board filled after the computer's move, it's a tie.
            display_board(board)  # Display the final board.
            print("It's a tie!")  # Announce the draw.
            break  # Stop the loop because the game is over.


if __name__ == "__main__":  # Ensure this block runs only when the script is executed directly.
    main()  # Start the game by calling the main function.
