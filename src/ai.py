import random
from src.engine import TicTacToeEngine

class TicTacToeAI:
    """
    AI player for Tic-Tac-Toe.
    Supports Easy (random), Medium (heuristic), and Hard (unbeatable minimax with alpha-beta pruning) modes.
    """

    def __init__(self, symbol: str):
        """
        Initializes the AI with its symbol ('X' or 'O').
        The opponent's symbol is automatically inferred.
        """
        self.symbol = symbol
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'

    def get_move(self, board: list[str], difficulty: str) -> int:
        """
        Returns the chosen board index (0-8) based on the specified difficulty:
        'easy', 'medium', or 'hard'.
        """
        available_moves = [i for i, cell in enumerate(board) if cell == ' ']
        if not available_moves:
            raise ValueError("No available moves on the board.")

        diff_lower = difficulty.lower()
        if diff_lower == 'easy':
            return self._get_easy_move(available_moves)
        elif diff_lower == 'medium':
            return self._get_medium_move(board, available_moves)
        elif diff_lower == 'hard':
            return self._get_hard_move(board, available_moves)
        else:
            raise ValueError(f"Unknown difficulty level: {difficulty}")

    def _get_easy_move(self, available_moves: list[int]) -> int:
        """Easy mode: picks a completely random valid move."""
        return random.choice(available_moves)

    def _get_medium_move(self, board: list[str], available_moves: list[int]) -> int:
        """
        Medium mode:
        1. Checks for immediate winning moves for AI.
        2. Checks for immediate blocking moves (preventing player wins).
        3. Prefers center if available.
        4. Prefers corners.
        5. Falls back to random edge.
        """
        # 1. Check if AI can win in this move
        for move in available_moves:
            temp_board = list(board)
            temp_board[move] = self.symbol
            if TicTacToeEngine.check_winner_static(temp_board) == self.symbol:
                return move

        # 2. Check if opponent can win in their next move, and block it
        for move in available_moves:
            temp_board = list(board)
            temp_board[move] = self.opponent_symbol
            if TicTacToeEngine.check_winner_static(temp_board) == self.opponent_symbol:
                return move

        # 3. Prefer the center
        if 4 in available_moves:
            return 4

        # 4. Prefer corners (0, 2, 6, 8)
        corners = [c for c in [0, 2, 6, 8] if c in available_moves]
        if corners:
            return random.choice(corners)

        # 5. Fallback to edges (1, 3, 5, 7)
        edges = [e for e in [1, 3, 5, 7] if e in available_moves]
        if edges:
            return random.choice(edges)

        return random.choice(available_moves)

    def _get_hard_move(self, board: list[str], available_moves: list[int]) -> int:
        """
        Hard mode: Unbeatable AI using Minimax with Alpha-Beta Pruning.
        If there are multiple moves with the same best outcome, it randomly picks
        one of them to keep the game interesting and varied.
        """
        # For the first move if the board is completely empty, pick center or a random corner
        # to save computation and make the first move instant.
        if len(available_moves) == 9:
            return random.choice([4, 0, 2, 6, 8])

        best_score = -float('inf')
        best_moves = []

        for move in available_moves:
            board[move] = self.symbol
            score = self._minimax(board, 0, -float('inf'), float('inf'), False)
            board[move] = ' '  # Undo move

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    def _minimax(self, board: list[str], depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        """
        Recursive Minimax helper with Alpha-Beta Pruning.
        """
        # Base cases: terminal board states
        winner = TicTacToeEngine.check_winner_static(board)
        if winner == self.symbol:
            return 10 - depth  # Prefer faster wins
        elif winner == self.opponent_symbol:
            return -10 + depth  # Delay inevitable losses
        elif winner == 'Draw':
            return 0

        # Find empty indices
        available_moves = [i for i, cell in enumerate(board) if cell == ' ']

        if is_maximizing:
            max_eval = -float('inf')
            for move in available_moves:
                board[move] = self.symbol
                eval_score = self._minimax(board, depth + 1, alpha, beta, False)
                board[move] = ' '  # Undo move
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Pruning
            return max_eval
        else:
            min_eval = float('inf')
            for move in available_moves:
                board[move] = self.opponent_symbol
                eval_score = self._minimax(board, depth + 1, alpha, beta, True)
                board[move] = ' '  # Undo move
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Pruning
            return min_eval
