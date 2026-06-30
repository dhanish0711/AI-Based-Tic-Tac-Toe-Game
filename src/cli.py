import os
import sys
import time
from src.engine import TicTacToeEngine
from src.ai import TicTacToeAI

# ANSI Color Codes for premium terminal visuals
CYAN = '\033[96m'
PINK = '\033[95m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
GRAY = '\033[90m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_cell(val: str, idx: int) -> str:
    """Formats a single board cell with colors. Shows index if cell is empty."""
    if val == 'X':
        return f"{CYAN}{BOLD}X{RESET}"
    elif val == 'O':
        return f"{PINK}{BOLD}O{RESET}"
    else:
        return f"{GRAY}{idx + 1}{RESET}"

def print_board(board: list[str]):
    """Prints a beautiful styled board to the terminal."""
    r1 = f" {format_cell(board[0], 0)} │ {format_cell(board[1], 1)} │ {format_cell(board[2], 2)} "
    r2 = f" {format_cell(board[3], 3)} │ {format_cell(board[4], 4)} │ {format_cell(board[5], 5)} "
    r3 = f" {format_cell(board[6], 6)} │ {format_cell(board[7], 7)} │ {format_cell(board[8], 8)} "
    
    divider = f"{GRAY}───┼───┼───{RESET}"
    
    print()
    print(r1)
    print(divider)
    print(r2)
    print(divider)
    print(r3)
    print()

def print_header(difficulty: str, user_symbol: str, ai_symbol: str):
    """Prints a stylized header."""
    clear_screen()
    print(f"{YELLOW}{BOLD}╔═══════════════════════════════════════╗{RESET}")
    print(f"{YELLOW}{BOLD}║         TIC-TAC-TOE VS AI             ║{RESET}")
    print(f"{YELLOW}{BOLD}╚═══════════════════════════════════════╝{RESET}")
    print(f" Mode: {BOLD}CLI{RESET} | Difficulty: {GREEN}{BOLD}{difficulty.upper()}{RESET}")
    print(f" Player: {CYAN}{BOLD}{user_symbol}{RESET} vs AI: {PINK}{BOLD}{ai_symbol}{RESET}")
    print(f" {GRAY}Type numbers 1-9 to make a move.{RESET}")
    print(f"{YELLOW}{'─' * 41}{RESET}")

def get_cli_settings() -> tuple[str, str]:
    """Interactively prompts user for difficulty and player symbol."""
    clear_screen()
    print(f"{YELLOW}{BOLD}╔═══════════════════════════════════════╗{RESET}")
    print(f"{YELLOW}{BOLD}║         TIC-TAC-TOE SETUP             ║{RESET}")
    print(f"{YELLOW}{BOLD}╚═══════════════════════════════════════╝{RESET}")
    
    # 1. Choose Difficulty
    print(f"\nSelect {BOLD}Difficulty{RESET}:")
    print(f" [{GREEN}1{RESET}] Easy   {GRAY}(Random AI moves){RESET}")
    print(f" [{YELLOW}2{RESET}] Medium {GRAY}(Heuristic blocking & winning){RESET}")
    print(f" [{RED}3{RESET}] Hard   {GRAY}(Perfect Unbeatable Minimax){RESET}")
    
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    diff_choice = ''
    while diff_choice not in difficulty_map:
        diff_choice = input(f"\nEnter choice (1-3) [{YELLOW}3{RESET}]: ").strip()
        if not diff_choice:
            diff_choice = '3'
    difficulty = difficulty_map[diff_choice]
    
    # 2. Choose Player Symbol
    print(f"\nSelect your {BOLD}Symbol{RESET}:")
    print(f" [{CYAN}X{RESET}] Play as X (Goes first)")
    print(f" [{PINK}O{RESET}] Play as O (Goes second)")
    
    symbol_choice = ''
    while symbol_choice not in ['x', 'o', 'X', 'O']:
        symbol_choice = input(f"\nEnter choice (X or O) [{CYAN}X{RESET}]: ").strip()
        if not symbol_choice:
            symbol_choice = 'X'
    user_symbol = symbol_choice.upper()
    
    return difficulty, user_symbol

def run_cli_game(default_difficulty: str = None, default_symbol: str = None):
    """Runs the main CLI game loop."""
    # Enable ANSI terminal coloring on Windows
    if os.name == 'nt':
        os.system('')

    # Get settings from command line or prompt user
    if default_difficulty and default_symbol:
        difficulty = default_difficulty.lower()
        user_symbol = default_symbol.upper()
    else:
        difficulty, user_symbol = get_cli_settings()

    ai_symbol = 'O' if user_symbol == 'X' else 'X'
    
    # Initialize Game Engine and AI
    game = TicTacToeEngine()
    ai = TicTacToeAI(ai_symbol)
    
    play_again = True
    
    while play_again:
        game.reset()
        
        while not game.is_game_over():
            print_header(difficulty, user_symbol, ai_symbol)
            print_board(game.board)
            
            if game.current_player == user_symbol:
                # User's turn
                print(f" {BOLD}Your Turn!{RESET} Enter a position (1-9): ", end="")
                try:
                    move_str = input().strip()
                    # Exit game if user types exit/quit
                    if move_str.lower() in ['exit', 'quit', 'q']:
                        print(f"\n{YELLOW}Thanks for playing!{RESET}")
                        sys.exit(0)
                        
                    move_val = int(move_str) - 1
                    if not game.make_move(move_val):
                        print(f"\n{RED}Invalid move! Cell is occupied or out of bounds. Try again.{RESET}")
                        time.sleep(1.5)
                except ValueError:
                    print(f"\n{RED}Invalid input! Please enter a number between 1 and 9.{RESET}")
                    time.sleep(1.5)
            else:
                # AI's turn
                print(f" {GRAY}AI ({ai_symbol}) is calculating move...{RESET}")
                time.sleep(0.6)  # Give a slight delay for realistic pacing
                ai_move = ai.get_move(game.board, difficulty)
                game.make_move(ai_move)
        
        # Game Over Screen
        print_header(difficulty, user_symbol, ai_symbol)
        print_board(game.board)
        
        if game.winner == 'Draw':
            print(f"{YELLOW}{BOLD}🤝 It's a DRAW! Well played.{RESET}\n")
        elif game.winner == user_symbol:
            print(f"{GREEN}{BOLD}🎉 CONGRATULATIONS! You defeated the AI!{RESET}\n")
        else:
            print(f"{RED}{BOLD}💀 DEFEAT! The AI ({ai_symbol}) won the game.{RESET}\n")
            
        ans = input("Play again? (y/n) [y]: ").strip().lower()
        if ans not in ['', 'y', 'yes']:
            play_again = False
            
    print(f"\n{YELLOW}Thanks for playing! Goodbye.{RESET}")
