from random import randrange


def display_board(board):
    horizontal_border = "+-------+-------+-------+"
    empty_row = "|       |       |       |"

    for row in board:
        print(horizontal_border)
        print(empty_row)
        print("|   " + "   |   ".join(str(cell) for cell in row) + "   |")
        print(empty_row)
    print(horizontal_border)


def make_list_of_free_fields(board):
    free_fields = []
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell not in ("X", "O"):
                free_fields.append((row_idx, col_idx))
    return free_fields


def victory_for(board, sign):
    win_positions = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for positions in win_positions:
        if all(board[row][col] == sign for row, col in positions):
            return True
    return False


def enter_move(board):
    while True:
        move_input = input("Enter your move: ")
        try:
            move = int(move_input)
        except ValueError:
            print("Please enter a valid number between 1 and 9.")
            continue

        if move < 1 or move > 9:
            print("The move must be between 1 and 9.")
            continue

        row = (move - 1) // 3
        col = (move - 1) % 3

        if board[row][col] in ("X", "O"):
            print("That square is already occupied. Choose another one.")
            continue

        board[row][col] = "O"
        break


def draw_move(board):
    free_fields = make_list_of_free_fields(board)
    if not free_fields:
        return

    row, col = free_fields[randrange(len(free_fields))]
    board[row][col] = "X"


def main():
    board = [
        [1, 2, 3],
        [4, "X", 6],
        [7, 8, 9],
    ]

    while True:
        display_board(board)

        if victory_for(board, "X"):
            print("The computer won!")
            break
        if victory_for(board, "O"):
            print("You won!")
            break

        if not make_list_of_free_fields(board):
            print("It's a tie!")
            break

        enter_move(board)

        if victory_for(board, "O"):
            display_board(board)
            print("You won!")
            break

        if not make_list_of_free_fields(board):
            display_board(board)
            print("It's a tie!")
            break

        draw_move(board)

        if victory_for(board, "X"):
            display_board(board)
            print("The computer won!")
            break

        if not make_list_of_free_fields(board):
            display_board(board)
            print("It's a tie!")
            break


if __name__ == "__main__":
    main()
