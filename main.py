import gradio as gr  # Import Gradio to build a friendly web interface for the game.
from random import randrange  # Import the randrange function to pick random numbers for the computer's move.


def make_list_of_free_fields(board):
    """Return a list of indices for open squares in a 1D board representation."""

    return [index for index, cell in enumerate(board) if cell not in ("X", "O")]


def victory_for(board, sign):
    """Check whether the provided sign ("X" or "O") has a winning line."""

    win_positions = [
        # Rows
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        # Columns
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        # Diagonals
        (0, 4, 8),
        (2, 4, 6),
    ]

    return any(all(board[pos] == sign for pos in pattern) for pattern in win_positions)


def computer_move(board):
    """Place an 'X' on a random free square."""

    free_fields = make_list_of_free_fields(board)
    if not free_fields:
        return board

    board[free_fields[randrange(len(free_fields))]] = "X"
    return board


def format_board(board):
    """Convert board state to display-friendly labels."""

    return [cell if cell in ("X", "O") else "" for cell in board]


def describe_state(board):
    """Create a user-facing message summarizing the current game state."""

    if victory_for(board, "O"):
        return "You won! 🎉"
    if victory_for(board, "X"):
        return "The computer won this round."
    if not make_list_of_free_fields(board):
        return "It's a tie!"
    return "Your move: tap any open square to place an O."


def initialize_board():
    """Start a new game with the computer taking center as X."""

    board = ["" for _ in range(9)]
    board[4] = "X"
    return board


def reset_game():
    """Return a fresh board and its accompanying status and labels."""

    board = initialize_board()
    return board, describe_state(board), *format_board(board)


def play_turn(selected_index, board):
    """Process a player's move, then let the computer respond if the game continues."""

    # Copy to avoid mutating Gradio's state in place before returning updates.
    board = list(board)

    # If the game is already over, keep the board unchanged.
    if victory_for(board, "O") or victory_for(board, "X") or not make_list_of_free_fields(board):
        return board, describe_state(board), *format_board(board)

    if board[selected_index] in ("X", "O"):
        return board, "That square is taken. Choose another spot!", *format_board(board)

    board[selected_index] = "O"

    if victory_for(board, "O") or not make_list_of_free_fields(board):
        return board, describe_state(board), *format_board(board)

    # Computer's response
    computer_move(board)
    return board, describe_state(board), *format_board(board)


def build_ui():
    """Create and return a Gradio Blocks interface for the game."""

    with gr.Blocks(title="Tic-Tac-Toe") as demo:
        gr.Markdown(
            """
            # Tic-Tac-Toe
            Play a quick round of Tic-Tac-Toe. You are **O** and the computer is **X**.
            The computer starts in the center—tap any empty square to respond.
            """
        )

        starting_board = initialize_board()
        board_state = gr.State(starting_board)
        status = gr.Markdown(describe_state(starting_board))

        buttons = []
        for row in range(3):
            with gr.Row():
                for col in range(3):
                    index = row * 3 + col
                    button = gr.Button(
                        value="X" if index == 4 else "",
                        size="lg",
                        variant="secondary",
                    )
                    buttons.append(button)

        for idx, button in enumerate(buttons):
            button.click(
                fn=lambda board, idx=idx: play_turn(idx, board),
                inputs=board_state,
                outputs=[board_state, status, *buttons],
            )

        gr.Button("Restart", variant="primary").click(
            fn=reset_game,
            inputs=None,
            outputs=[board_state, status, *buttons],
        )

    return demo


def main():
    """Launch the Gradio demo for playing Tic-Tac-Toe."""

    demo = build_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
