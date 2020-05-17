class GameStatus:
    def __init__(self):
        self.game_started = False
        self.game_running = False
        self.game_over = False
        self.winner = None
        self.game_controls = False
        self.game_about = False
        self.game_paused = False
        self.game_selection = False
        self.game_menu = True
        self.player1_selected = False
        self.player2_selected = False
        self.game_menu_text = ["start", "controls", "about", "exit"]
        self.pause_menu_text = ["resume", "controls", "about", "exit"]
        self.game_selection_text = ["ship 1", "ship 2", "ship 3"]

