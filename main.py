import argparse
import sys
from src.cli import run_cli_game

def launch_gui(difficulty: str, symbol: str):
    """Attempts to launch the graphical user interface. Falls back to CLI if it fails."""
    try:
        import tkinter as tk
        from src.gui import TicTacToeGUI
        
        root = tk.Tk()
        app = TicTacToeGUI(root)
        
        # Apply command line defaults if specified
        if difficulty in ['easy', 'medium', 'hard']:
            app.diff_var.set(difficulty)
            app.difficulty = difficulty
        if symbol in ['X', 'O']:
            app.symbol_var.set(symbol)
            app.user_symbol = symbol
            app.ai_symbol = 'O' if symbol == 'X' else 'X'
            # Trigger symbol update without restarting twice
            app.on_symbol_change()
            
        root.mainloop()
    except (ImportError, tk.TclError) as e:
        print(f"\n[Warning] Graphical interface could not be started: {e}")
        print("Falling back to Command Line Interface (CLI) mode...\n")
        # Give user time to read before clearing
        import time
        time.sleep(2)
        run_cli_game(default_difficulty=difficulty, default_symbol=symbol)

def main():
    parser = argparse.ArgumentParser(
        description="Play Tic-Tac-Toe against an AI with multiple difficulty levels.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--mode",
        choices=["gui", "cli"],
        default="gui",
        help="Select user interface mode: 'gui' (default) or 'cli'."
    )
    
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        default="hard",
        help="Set starting difficulty level: 'easy', 'medium', or 'hard'."
    )
    
    parser.add_argument(
        "--symbol",
        choices=["X", "O"],
        default="X",
        help="Set your player symbol: 'X' (goes first) or 'O' (goes second)."
    )
    
    args = parser.parse_args()
    
    if args.mode == "gui":
        launch_gui(args.difficulty, args.symbol)
    else:
        run_cli_game(args.difficulty, args.symbol)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame terminated. Goodbye!")
        sys.exit(0)
