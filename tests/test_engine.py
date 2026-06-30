import unittest
from src.engine import TicTacToeEngine

class TestTicTacToeEngine(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToeEngine()

    def test_initial_state(self):
        """Test if the game initializes in a clean state."""
        self.assertEqual(self.game.board, [' ' for _ in range(9)])
        self.assertEqual(self.game.current_player, 'X')
        self.assertIsNone(self.game.winner)
        self.assertFalse(self.game.is_game_over())

    def test_make_valid_move(self):
        """Test that a valid move updates board and switches player."""
        success = self.game.make_move(0)
        self.assertTrue(success)
        self.assertEqual(self.game.board[0], 'X')
        self.assertEqual(self.game.current_player, 'O')
        self.assertIsNone(self.game.winner)

    def test_make_invalid_move_occupied(self):
        """Test that making a move on an occupied cell is invalid."""
        self.game.make_move(0)  # X plays 0
        success = self.game.make_move(0)  # O tries to play 0
        self.assertFalse(success)
        self.assertEqual(self.game.board[0], 'X')
        self.assertEqual(self.game.current_player, 'O')  # Player shouldn't switch

    def test_make_invalid_move_out_of_bounds(self):
        """Test that making a move out of bounds is invalid."""
        self.assertFalse(self.game.make_move(-1))
        self.assertFalse(self.game.make_move(9))

    def test_winning_horizontal(self):
        """Test that three in a row horizontally wins the game."""
        # Board setup:
        # X X X
        # O O
        #
        self.game.make_move(0)  # X
        self.game.make_move(3)  # O
        self.game.make_move(1)  # X
        self.game.make_move(4)  # O
        self.game.make_move(2)  # X wins
        self.assertEqual(self.game.winner, 'X')
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_winning_line(), (0, 1, 2))

    def test_winning_vertical(self):
        """Test that three in a column vertically wins the game."""
        # Board setup:
        # X O
        # X O
        # X
        self.game.make_move(0)  # X
        self.game.make_move(1)  # O
        self.game.make_move(3)  # X
        self.game.make_move(4)  # O
        self.game.make_move(6)  # X wins
        self.assertEqual(self.game.winner, 'X')
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_winning_line(), (0, 3, 6))

    def test_winning_diagonal(self):
        """Test that three in a diagonal wins the game."""
        # Board setup:
        # X O
        #   X O
        #     X
        self.game.make_move(0)  # X
        self.game.make_move(1)  # O
        self.game.make_move(4)  # X
        self.game.make_move(5)  # O
        self.game.make_move(8)  # X wins
        self.assertEqual(self.game.winner, 'X')
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_winning_line(), (0, 4, 8))

    def test_draw_game(self):
        """Test that a full board with no winner results in a draw."""
        # Board layout:
        # X O X
        # X O O
        # O X X
        moves = [0, 1, 3, 4, 7, 5, 2, 6, 8]
        # 0: X -> board[0]='X'
        # 1: O -> board[1]='O'
        # 3: X -> board[3]='X'
        # 4: O -> board[4]='O'
        # 7: X -> board[7]='X'
        # 5: O -> board[5]='O'
        # 2: X -> board[2]='X'
        # 6: O -> board[6]='O'
        # 8: X -> board[8]='X'
        for move in moves:
            self.game.make_move(move)

        self.assertEqual(self.game.winner, 'Draw')
        self.assertTrue(self.game.is_game_over())
        self.assertIsNone(self.game.get_winning_line())

    def test_reset(self):
        """Test resetting the game."""
        self.game.make_move(0)
        self.game.make_move(4)
        self.game.make_move(8)
        self.game.reset()
        self.test_initial_state()

if __name__ == '__main__':
    unittest.main()
