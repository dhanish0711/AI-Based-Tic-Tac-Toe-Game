class TicTacToeEngine:
    """
    Core game engine for Tic-Tac-Toe.
    Handles board state, move validation, turn switching, and win/draw evaluation.
    """
    WINNING_COMBINATIONS = [
        # Rows
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        # Columns
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        # Diagonals
        (0, 4, 8), (2, 4, 6)
    ]

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        """Resets the board state and starts a new game with X as the first player."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.winner = None

    def get_available_moves(self) -> list[int]:
        """Returns a list of indices (0-8) representing empty cells."""
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    def is_valid_move(self, position: int) -> bool:
        """Checks if a move to the specified position (0-8) is valid."""
        return 0 <= position < 9 and self.board[position] == ' '

    def make_move(self, position: int) -> bool:
        """
        Attempts to place the current player's symbol at the specified position.
        If successful, updates the game state, checks for a win/draw, switches turns,
        and returns True. Otherwise, returns False.
        """
        if not self.is_valid_move(position):
            return False

        self.board[position] = self.current_player
        
        # Check if this move won or drew the game
        winner = self.check_winner_static(self.board)
        if winner:
            self.winner = winner
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
        return True

    @classmethod
    def check_winner_static(cls, board_state: list[str]) -> str | None:
        """
        Static helper to determine the state of a board.
        Returns 'X', 'O' for winners, 'Draw' if the board is full with no winner,
        or None if the game is still in progress.
        """
        # Check all winning combinations
        for combo in cls.WINNING_COMBINATIONS:
            a, b, c = combo
            if board_state[a] != ' ' and board_state[a] == board_state[b] == board_state[c]:
                return board_state[a]

        # Check if the board is full (Draw)
        if ' ' not in board_state:
            return 'Draw'

        # Game is still in progress
        return None

    def is_game_over(self) -> bool:
        """Returns True if the game has ended in a win or a draw."""
        return self.winner is not None or ' ' not in self.board

    def get_winning_line(self) -> tuple[int, int, int] | None:
        """
        If there is a winner, returns the combination (3 indices) that won.
        Otherwise returns None.
        """
        for combo in self.WINNING_COMBINATIONS:
            a, b, c = combo
            if self.board[a] != ' ' and self.board[a] == self.board[b] == self.board[c]:
                return combo
        return None
