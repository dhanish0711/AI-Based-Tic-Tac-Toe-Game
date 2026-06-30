import tkinter as tk
from tkinter import messagebox, ttk
from src.engine import TicTacToeEngine
from src.ai import TicTacToeAI

class TicTacToeGUI:
    """
    A premium Tkinter GUI for the Tic-Tac-Toe game.
    Features a modern dark theme, smooth Canvas animations, scoreboard,
    and side controls for setting difficulty and player symbol.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe VS AI")
        self.root.resizable(False, False)
        
        # Color Palette
        self.BG_DARK = "#1a1b26"       # Deep slate dark
        self.BG_SIDE = "#24283b"       # Sidebar background
        self.GRID_COLOR = "#414868"    # Soft blue-gray for grid lines
        self.COLOR_X = "#00f0ff"       # Neon Cyan for X
        self.COLOR_O = "#ff007f"       # Neon Pink for O
        self.COLOR_WIN = "#50fa7b"     # Neon Green for winning line
        self.TEXT_COLOR = "#c0caf5"    # Cool gray-white for text
        self.ACCENT_COLOR = "#bb9af7"  # Soft purple accent
        self.HIGHLIGHT_BG = "#2f344f"  # Cell highlight on hover

        self.root.configure(bg=self.BG_DARK)

        # Game State
        self.game = TicTacToeEngine()
        self.user_symbol = "X"
        self.ai_symbol = "O"
        self.difficulty = "hard"
        self.ai_thinking = False

        # Score Tracker
        self.scores = {"player": 0, "ai": 0, "draws": 0}

        # Setup GUI Elements
        self._setup_styles()
        self._create_widgets()
        
        # Draw initial grid
        self.draw_grid()

    def _setup_styles(self):
        """Configure custom styles for Tkinter widgets."""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure fonts and dark-theme frames
        style.configure("TFrame", background=self.BG_SIDE)
        style.configure("Sidebar.TFrame", background=self.BG_SIDE)
        
        style.configure("TLabel", background=self.BG_SIDE, foreground=self.TEXT_COLOR, font=("Arial", 10))
        style.configure("Title.TLabel", background=self.BG_SIDE, foreground=self.ACCENT_COLOR, font=("Helvetica", 16, "bold"))
        style.configure("Header.TLabel", background=self.BG_SIDE, foreground=self.TEXT_COLOR, font=("Arial", 11, "bold"))
        
        # Configure Radiobuttons
        style.configure("TRadiobutton", background=self.BG_SIDE, foreground=self.TEXT_COLOR, font=("Arial", 10))
        style.map("TRadiobutton",
                  background=[("active", self.BG_SIDE)],
                  foreground=[("active", self.COLOR_X)])

        # Configure Button
        style.configure("TButton",
                        background=self.GRID_COLOR,
                        foreground=self.TEXT_COLOR,
                        bordercolor=self.BG_DARK,
                        font=("Arial", 11, "bold"),
                        padding=6)
        style.map("TButton",
                  background=[("active", self.HIGHLIGHT_BG), ("pressed", self.BG_DARK)],
                  foreground=[("active", "#ffffff")])

    def _create_widgets(self):
        """Create the window layout and widgets."""
        # Main Layout: Sidebar (left) and Board (right)
        self.main_container = tk.Frame(self.root, bg=self.BG_DARK)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # --- SIDEBAR PANEL (Controls & Stats) ---
        self.sidebar = ttk.Frame(self.main_container, style="Sidebar.TFrame", padding=15)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        # Title
        title_lbl = ttk.Label(self.sidebar, text="TIC-TAC-TOE", style="Title.TLabel")
        title_lbl.pack(anchor=tk.W, pady=(0, 2))
        
        subtitle_lbl = ttk.Label(self.sidebar, text="AI Decision Engine", font=("Helvetica", 8, "italic"), foreground=self.GRID_COLOR)
        subtitle_lbl.pack(anchor=tk.W, pady=(0, 15))

        # Separator
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # 1. Choose Difficulty
        ttk.Label(self.sidebar, text="Difficulty Level", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        self.diff_var = tk.StringVar(value="hard")
        
        easy_rb = ttk.Radiobutton(self.sidebar, text="Easy (Random)", value="easy", variable=self.diff_var, command=self.on_settings_change)
        medium_rb = ttk.Radiobutton(self.sidebar, text="Medium (Heuristic)", value="medium", variable=self.diff_var, command=self.on_settings_change)
        hard_rb = ttk.Radiobutton(self.sidebar, text="Hard (Minimax)", value="hard", variable=self.diff_var, command=self.on_settings_change)
        
        easy_rb.pack(anchor=tk.W, pady=2)
        medium_rb.pack(anchor=tk.W, pady=2)
        hard_rb.pack(anchor=tk.W, pady=2)

        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # 2. Choose Player Symbol
        ttk.Label(self.sidebar, text="Play As", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        self.symbol_var = tk.StringVar(value="X")
        
        x_rb = ttk.Radiobutton(self.sidebar, text="X (Goes First)", value="X", variable=self.symbol_var, command=self.on_symbol_change)
        o_rb = ttk.Radiobutton(self.sidebar, text="O (Goes Second)", value="O", variable=self.symbol_var, command=self.on_symbol_change)
        
        x_rb.pack(anchor=tk.W, pady=2)
        o_rb.pack(anchor=tk.W, pady=2)

        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # 3. Scoreboard Section
        ttk.Label(self.sidebar, text="Scoreboard", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 8))
        
        self.score_frame = tk.Frame(self.sidebar, bg=self.HIGHLIGHT_BG, bd=1, relief=tk.SOLID)
        self.score_frame.pack(fill=tk.X, pady=5)
        
        # Wins/Losses display inside score frame
        self.lbl_player_score = tk.Label(self.score_frame, text="Player (X): 0", bg=self.HIGHLIGHT_BG, fg=self.COLOR_X, font=("Arial", 10, "bold"), pady=4)
        self.lbl_player_score.pack(anchor=tk.W, padx=10)
        
        self.lbl_ai_score = tk.Label(self.score_frame, text="AI (O): 0", bg=self.HIGHLIGHT_BG, fg=self.COLOR_O, font=("Arial", 10, "bold"), pady=4)
        self.lbl_ai_score.pack(anchor=tk.W, padx=10)
        
        self.lbl_draws = tk.Label(self.score_frame, text="Draws: 0", bg=self.HIGHLIGHT_BG, fg=self.TEXT_COLOR, font=("Arial", 10, "bold"), pady=4)
        self.lbl_draws.pack(anchor=tk.W, padx=10)

        # Restart Button
        self.btn_restart = ttk.Button(self.sidebar, text="Restart Game", command=self.restart_game)
        self.btn_restart.pack(fill=tk.X, pady=(20, 0))

        # --- RIGHT SIDE: BOARD & STATUS ---
        self.board_container = tk.Frame(self.main_container, bg=self.BG_DARK)
        self.board_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Status Bar above the board
        self.lbl_status = tk.Label(
            self.board_container, 
            text="Your Turn (X)", 
            font=("Arial", 12, "bold"), 
            bg=self.BG_DARK, 
            fg=self.COLOR_X,
            pady=8
        )
        self.lbl_status.pack(fill=tk.X)

        # Canvas Game Board
        self.board_size = 360
        self.canvas = tk.Canvas(
            self.board_container, 
            width=self.board_size, 
            height=self.board_size, 
            bg=self.BG_DARK, 
            highlightthickness=1,
            highlightbackground=self.GRID_COLOR
        )
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_grid(self):
        """Draws the Tic-Tac-Toe grid lines on the Canvas."""
        self.canvas.delete("all")
        
        # Draw 2 vertical lines
        self.canvas.create_line(120, 10, 120, 350, fill=self.GRID_COLOR, width=5, capstyle=tk.ROUND)
        self.canvas.create_line(240, 10, 240, 350, fill=self.GRID_COLOR, width=5, capstyle=tk.ROUND)
        
        # Draw 2 horizontal lines
        self.canvas.create_line(10, 120, 350, 120, fill=self.GRID_COLOR, width=5, capstyle=tk.ROUND)
        self.canvas.create_line(10, 240, 350, 240, fill=self.GRID_COLOR, width=5, capstyle=tk.ROUND)

    def on_settings_change(self):
        """Triggered when difficulty changes."""
        self.difficulty = self.diff_var.get()

    def on_symbol_change(self):
        """Triggered when player changes their character (X or O). Restarts game."""
        self.user_symbol = self.symbol_var.get()
        self.ai_symbol = "O" if self.user_symbol == "X" else "X"
        
        # Update Scoreboard Labels
        self.lbl_player_score.configure(text=f"Player ({self.user_symbol}): {self.scores['player']}", fg=self.COLOR_X if self.user_symbol == "X" else self.COLOR_O)
        self.lbl_ai_score.configure(text=f"AI ({self.ai_symbol}): {self.scores['ai']}", fg=self.COLOR_O if self.user_symbol == "X" else self.COLOR_X)
        
        self.restart_game()

    def restart_game(self):
        """Resets the game state and board view."""
        self.game.reset()
        self.ai_thinking = False
        self.draw_grid()
        self.update_status()

        # If user is O, AI goes first as X
        if self.user_symbol == "O":
            self.trigger_ai_move()

    def update_status(self):
        """Updates the top status text based on game engine state."""
        if self.game.winner:
            if self.game.winner == "Draw":
                self.lbl_status.configure(text="It's a Draw! 🤝", fg=self.TEXT_COLOR)
            elif self.game.winner == self.user_symbol:
                self.lbl_status.configure(text="You Won! 🎉", fg=self.COLOR_X if self.user_symbol == "X" else self.COLOR_O)
            else:
                self.lbl_status.configure(text="AI Won! 💀", fg=self.COLOR_O if self.user_symbol == "X" else self.COLOR_X)
        else:
            if self.game.current_player == self.user_symbol:
                self.lbl_status.configure(text="Your Turn", fg=self.COLOR_X if self.user_symbol == "X" else self.COLOR_O)
            else:
                self.lbl_status.configure(text="AI is thinking...", fg=self.COLOR_O if self.user_symbol == "X" else self.COLOR_X)

    def on_canvas_click(self, event):
        """Processes clicking on the grid canvas."""
        # Block clicks if it's the AI's turn or game is over
        if self.game.is_game_over() or self.game.current_player != self.user_symbol or self.ai_thinking:
            return

        col = event.x // 120
        row = event.y // 120
        index = row * 3 + col

        if self.game.is_valid_move(index):
            # Record user move
            player = self.game.current_player
            self.game.make_move(index)
            self.draw_symbol(index, player)
            
            self.update_status()
            
            # Check if game is over
            if self.game.is_game_over():
                self.handle_game_over()
            else:
                # Trigger AI turn after a short delay
                self.trigger_ai_move()

    def draw_symbol(self, index: int, player: str, animated: bool = True):
        """Draws X or O on the canvas at the specified index (0-8)."""
        row = index // 3
        col = index % 3
        
        # Bounding box coordinates for the cell
        x1 = col * 120 + 25
        y1 = row * 120 + 25
        x2 = col * 120 + 95
        y2 = row * 120 + 95
        
        if player == "X":
            color = self.COLOR_X
            if animated:
                # Draw cross lines in stages
                self.animate_line(x1, y1, x2, y2, color, width=8, step=0)
                self.root.after(150, lambda: self.animate_line(x2, y1, x1, y2, color, width=8, step=0))
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=8, capstyle=tk.ROUND, tags=f"cell_{index}")
                self.canvas.create_line(x2, y1, x1, y2, fill=color, width=8, capstyle=tk.ROUND, tags=f"cell_{index}")
        else:
            color = self.COLOR_O
            if animated:
                self.animate_oval(x1, y1, x2, y2, color, width=8)
            else:
                self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=8, tags=f"cell_{index}")

    def animate_line(self, x1, y1, x2, y2, color, width, step=0, total_steps=10):
        """Animates drawing a straight line incremental by step."""
        if step > total_steps:
            return
        
        # Calculate current position of the line end
        curr_x = x1 + (x2 - x1) * (step / total_steps)
        curr_y = y1 + (y2 - y1) * (step / total_steps)
        
        # Redraw lines up to current position
        line_tag = f"line_{x1}_{y1}"
        self.canvas.delete(line_tag)
        self.canvas.create_line(x1, y1, curr_x, curr_y, fill=color, width=width, capstyle=tk.ROUND, tags=line_tag)
        
        self.root.after(15, lambda: self.animate_line(x1, y1, x2, y2, color, width, step + 1, total_steps))

    def animate_oval(self, x1, y1, x2, y2, color, width, angle=0, step=15):
        """Animates drawing an oval by drawing arcs incrementally."""
        if angle > 360:
            # Draw final clean oval
            self.canvas.delete(f"arc_{x1}_{y1}")
            self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=width)
            return

        arc_tag = f"arc_{x1}_{y1}"
        self.canvas.delete(arc_tag)
        # Create arc from 0 to current angle
        self.canvas.create_arc(
            x1, y1, x2, y2, 
            start=90, extent=-angle, 
            style=tk.ARC, outline=color, width=width, 
            tags=arc_tag
        )
        
        self.root.after(15, lambda: self.animate_oval(x1, y1, x2, y2, color, width, angle + step, step))

    def trigger_ai_move(self):
        """Triggers the AI's move calculation and animation."""
        self.ai_thinking = True
        self.update_status()
        
        # Add a delay of 600ms so the AI feels like it's "thinking"
        self.root.after(600, self.execute_ai_move)

    def execute_ai_move(self):
        if not self.ai_thinking or self.game.is_game_over():
            self.ai_thinking = False
            return

        ai_player = TicTacToeAI(self.ai_symbol)
        
        try:
            best_move = ai_player.get_move(self.game.board, self.difficulty)
            player = self.game.current_player
            
            # Make the move in engine
            self.game.make_move(best_move)
            self.draw_symbol(best_move, player)
            
            self.update_status()
            
            # Check if game is over
            if self.game.is_game_over():
                self.handle_game_over()
        except Exception as e:
            messagebox.showerror("AI Error", f"An error occurred in AI calculation: {e}")
        finally:
            self.ai_thinking = False
            self.update_status()

    def draw_winning_line(self, line: tuple[int, int, int]):
        """Draws a neon green line across the winning cells."""
        # Helper to convert indices 0-8 to canvas center coordinates
        centers = []
        for index in line:
            row = index // 3
            col = index % 3
            cx = col * 120 + 60
            cy = row * 120 + 60
            centers.append((cx, cy))
            
        x1, y1 = centers[0]
        x2, y2 = centers[2]
        
        # Add an animation to draw the winning line
        self.animate_line(x1, y1, x2, y2, self.COLOR_WIN, width=10)

    def handle_game_over(self):
        """Performs game over processing: highlights winner, updates scores."""
        # 1. Update Scoreboard and Draw winning line if there's a winner
        if self.game.winner == "Draw":
            self.scores["draws"] += 1
            self.lbl_draws.configure(text=f"Draws: {self.scores['draws']}")
        else:
            winning_line = self.game.get_winning_line()
            if winning_line:
                self.draw_winning_line(winning_line)
                
            if self.game.winner == self.user_symbol:
                self.scores["player"] += 1
                lbl_txt = f"Player ({self.user_symbol}): {self.scores['player']}"
                self.lbl_player_score.configure(text=lbl_txt)
            else:
                self.scores["ai"] += 1
                lbl_txt = f"AI ({self.ai_symbol}): {self.scores['ai']}"
                self.lbl_ai_score.configure(text=lbl_txt)
                
        # 2. Update status label
        self.update_status()
