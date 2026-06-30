import unittest
from src.engine import TicTacToeEngine
from src.ai import TicTacToeAI

class TestTicTacToeAI(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToeEngine()
        self.ai_o = TicTacToeAI('O')  # AI plays O
        self.ai_x = TicTacToeAI('X')  # AI plays X

    def test_easy_ai_returns_valid_move(self):
        """Test that the Easy AI chooses a valid, empty cell."""
        self.game.make_move(0)
        self.game.make_move(1)
        self.game.make_move(2)
        move = self.ai_o.get_move(self.game.board, 'easy')
        self.assertIn(move, self.game.get_available_moves())
        self.assertTrue(self.game.is_valid_move(move))

    def test_medium_ai_wins_immediately(self):
        """Test that the Medium AI will make a winning move if available."""
        # Board layout (O has 2 in a row):
        # O O .
        # X X .
        # . . .
        self.game.board = [
            'O', 'O', ' ',
            'X', 'X', ' ',
            ' ', ' ', ' '
        ]
        move = self.ai_o.get_move(self.game.board, 'medium')
        self.assertEqual(move, 2)  # Should win immediately

    def test_medium_ai_blocks_immediately(self):
        """Test that the Medium AI will block opponent's immediate win."""
        # Board layout (X has 2 in a row):
        # X X .
        # O . .
        # . . .
        self.game.board = [
            'X', 'X', ' ',
            'O', ' ', ' ',
            ' ', ' ', ' '
        ]
        move = self.ai_o.get_move(self.game.board, 'medium')
        self.assertEqual(move, 2)  # Should block X's win

    def test_hard_ai_wins_immediately(self):
        """Test that the Hard AI takes immediate win."""
        # Board layout:
        # O O .
        # X X .
        # . . .
        self.game.board = [
            'O', 'O', ' ',
            'X', 'X', ' ',
            ' ', ' ', ' '
        ]
        move = self.ai_o.get_move(self.game.board, 'hard')
        self.assertEqual(move, 2)

    def test_hard_ai_blocks_immediately(self):
        """Test that the Hard AI blocks opponent's win."""
        # Board layout:
        # X X .
        # O . .
        # . . .
        self.game.board = [
            'X', 'X', ' ',
            'O', ' ', ' ',
            ' ', ' ', ' '
        ]
        move = self.ai_o.get_move(self.game.board, 'hard')
        self.assertEqual(move, 2)

    def test_perfect_play_draws(self):
        """
        Simulate multiple games of Hard AI (X) against Hard AI (O).
        Since Tic-Tac-Toe is a solved game, perfect play by both sides
        must ALWAYS result in a Draw.
        """
        # Run 20 simulated games. Because of random choices when multiple moves are optimal,
        # different game paths will be tested, but they must all end in draws.
        for _ in range(20):
            game = TicTacToeEngine()
            ai_x = TicTacToeAI('X')
            ai_o = TicTacToeAI('O')
            
            while not game.is_game_over():
                if game.current_player == 'X':
                    move = ai_x.get_move(game.board, 'hard')
                else:
                    move = ai_o.get_move(game.board, 'hard')
                game.make_move(move)
                
            self.assertEqual(game.winner, 'Draw', f"Game ended with winner {game.winner} but should be Draw. Final board: {game.board}")

if __name__ == '__main__':
    unittest.main()
