class Settings:
    """A class to store all settings for Lines of Action."""

    def __init__(self):
        """Initialize the game's settings."""

        # Screen settings
        self.screen_width = 800
        self.screen_height = 800

        # Board settings
        self.rows = 8
        self.cols = 8
        self.square_size = self.screen_width // self.cols
        self.light_color = (238, 238, 210)
        self.dark_color = (233,116,81)

        # Movement Settings
        self.directions = [
            (1, 0), (-1, 0),  # Horizontal (Right, Left)
            (0, 1), (0, -1),  # Vertical (Down, Up)
            (1, 1), (-1, -1), # Diagonal (Bottom-right, Top-left)
            (1, -1), (-1, 1)  # Diagonal (Bottom-left, Top-right)
        ]

        # Piece settings
        self.piece_size = (self.square_size, self.square_size)
        self.white_piece = 'images/white_checker.bmp'
        self.black_piece = 'images/black_checker.bmp'

        # Game settings
        self.fps = 60