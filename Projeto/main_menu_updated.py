import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.font.init()

class Settings:
    """A class to store all settings for Lines of Action."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = int((2/3) * pygame.display.Info().current_h)
        self.screen_height = self.screen_width

        # Board settings
        self.rows = 8
        self.cols = 8
        self.square_size = self.screen_width // self.cols
        self.light_color = (238, 238, 210)
        self.dark_color = (233, 116, 81)

        # Button settings
        self.button_width = 2.5 * self.square_size
        self.button_height = self.square_size // 2

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

        # Player Settings
        self.player_options = ['Human', 'Minimax(cuts)', 'Minimax(no cuts)', 'Negamax(cuts)', 'Negamax(no cuts)', 'MCTS']

        # Game settings
        self.fps = 60


settings = Settings()
SCREEN_WIDTH = settings.screen_width
SCREEN_HEIGHT = settings.screen_height
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
COLOR_BASE = "#e8d1a5"
COLOR_HOVER = "white"
COLOR_BACK_HOVER = "Green"
COLOR_BLACK = "black"
FONT_CACHE = {}
CUSTOM_FONT_PATH = 'nunito_sans/NunitoSans-Regular.ttf'  # Replace with your font file path

def get_font(size):
    key = (CUSTOM_FONT_PATH, size)
    if key not in FONT_CACHE:
        try:
            font = pygame.font.Font(CUSTOM_FONT_PATH, size)
            FONT_CACHE[key] = font
        except FileNotFoundError:
            pass
            fallback_key = (None, size)
            if fallback_key not in FONT_CACHE:
                FONT_CACHE[fallback_key] = pygame.font.SysFont(None, size)
            return FONT_CACHE[fallback_key]
    return FONT_CACHE[key]

class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, size_factor=1):
        super().__init__()
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.size_factor = size_factor
        self.render_text(self.base_color)

        if self.image is None:
            # Create a transparent surface based on the size of the text
            self.image = pygame.Surface((self.text.get_width(), self.text.get_height()), pygame.SRCALPHA)  # Transparent surface
            self.image.fill((0, 0, 0, 0))  # Completely transparent background
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def render_text(self, color):
        # Render text on the button with the provided color
        self.text = self.font.render(self.text_input, True, color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkforinput(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.checkforinput(position):
            self.render_text(self.hovering_color)
        else:
            self.render_text(self.base_color)

def display_screen(title, subtitle, elements):
    pygame.display.set_caption(title)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(background, (0, 0))

        # Split the title into two parts and adjust the font size
        title_font_size = 120
        title_text1 = get_font(title_font_size).render("Lines", True, COLOR_BASE)
        title_text2 = get_font(title_font_size).render("of Action", True, COLOR_BASE)

        # Get the rects for the title text and adjust their positions
        title_rect1 = title_text1.get_rect(center=(SCREEN_WIDTH // 2, 75))
        title_rect2 = title_text2.get_rect(center=(SCREEN_WIDTH // 2, 75 + title_rect1.height + 10))

        SCREEN.blit(title_text1, title_rect1)
        SCREEN.blit(title_text2, title_rect2)

        subtitle_font_size = 50
        subtitle_text = get_font(subtitle_font_size).render(subtitle, True, COLOR_BASE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, title_rect2.bottom + 30))
        SCREEN.blit(subtitle_text, subtitle_rect)

        for element in elements:
            element.change_color(mouse_pos)
            element.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for element in elements:
                    if element.checkforinput(mouse_pos):
                        return element.text_input

        pygame.display.update()

def settings_screen(settings):
    back_button = Button(None, (65, SCREEN_HEIGHT - 65), "BACK", get_font(45), COLOR_BASE, COLOR_BACK_HOVER)
    
    # Title positioning (draw the title text manually)
    title_font = get_font(60)
    title_text = title_font.render("Choose Board Size", True, COLOR_BASE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))

    # Button positions adjusted to move them down a bit
    button_y_start = 300
    button_spacing = 80
    board_size_button_1 = Button(None, (SCREEN_WIDTH // 2, button_y_start), "8x8", get_font(60), COLOR_BASE, COLOR_HOVER)
    board_size_button_2 = Button(None, (SCREEN_WIDTH // 2, button_y_start + button_spacing), "10x10", get_font(60), COLOR_BASE, COLOR_HOVER)
    board_size_button_3 = Button(None, (SCREEN_WIDTH // 2, button_y_start + 2 * button_spacing), "12x12", get_font(60), COLOR_BASE, COLOR_HOVER)

    elements = [back_button, board_size_button_1, board_size_button_2, board_size_button_3]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Clear the screen with the background image
        SCREEN.blit(background, (0, 0))

        # Draw "Choose Board Size" title above the buttons
        SCREEN.blit(title_text, title_rect)

        for element in elements:
            element.change_color(mouse_pos)
            element.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for element in elements:
                    if element.checkforinput(mouse_pos):
                        # Handle user selection and update rows and cols in the settings object
                        if element.text_input == "BACK":
                            menu()  # Go back to the menu
                        elif element.text_input == "8x8":
                            settings.rows = 8
                            settings.cols = 8
                            menu()
                        elif element.text_input == "10x10":
                            settings.rows = 10
                            settings.cols = 10
                            menu()
                        elif element.text_input == "12x12":
                            settings.rows = 12
                            settings.cols = 12
                            menu()

        pygame.display.update()

def menu():
    play_button = Button(None, (SCREEN_WIDTH // 2, 375), "PLAY", get_font(75), COLOR_BASE, COLOR_HOVER)
    settings_button = Button(None, (SCREEN_WIDTH // 2, 525), "SETTINGS", get_font(75), COLOR_BASE, COLOR_HOVER)

    elements = [play_button, settings_button]
    choice = display_screen("Lines of Action", "", elements)

    if choice == "PLAY":
        play()
    elif choice == "SETTINGS":
        settings_screen(settings)  # Pass the settings object to the settings screen

def play():
    # Initialize button indices for each piece option
    button1_option_index = 0  # This will track the selected option for black pieces
    button2_option_index = 0  # This will track the selected option for white pieces
    button_options = ['Human', 'Minimax', 'Minimax α-β', 'Negamax', 'Negamax α-β', 'MCTS']
    
    back_button = Button(None, (65, SCREEN_HEIGHT - 65), "BACK", get_font(45), COLOR_BASE, COLOR_BACK_HOVER)
    
    # Increase the separation between the buttons by 100 pixels
    button1 = Button(None, (SCREEN_WIDTH // 2 - 150, 375), button_options[button1_option_index], get_font(60), COLOR_BASE, COLOR_HOVER)
    button2 = Button(None, (SCREEN_WIDTH // 2 + 150, 375), button_options[button2_option_index], get_font(60), COLOR_BASE, COLOR_HOVER)

    # Black Pieces title, adjusted higher above button1
    black_pieces_text = get_font(40).render("Black Pieces", True, COLOR_BASE)
    black_pieces_rect = black_pieces_text.get_rect(center=(SCREEN_WIDTH // 2 - 150, 375 - 50))

    # White Pieces title, adjusted higher above button2
    white_pieces_text = get_font(40).render("White Pieces", True, COLOR_BASE)
    white_pieces_rect = white_pieces_text.get_rect(center=(SCREEN_WIDTH // 2 + 150, 375 - 50))

    # Add a "Play" button under the piece options
    play_button = Button(None, (SCREEN_WIDTH // 2, 475 + 100), "PLAY", get_font(75), COLOR_BASE, COLOR_HOVER)

    elements = [back_button, button1, button2, play_button]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Clear the screen with the background image
        SCREEN.blit(background, (0, 0))

        # Render the title for "Lines of Action", moved 30px down (10px + 20px)
        title_font_size = 120
        title_text = get_font(title_font_size).render("Lines of Action", True, COLOR_BASE)

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 75 + 30))  # Moved 30px down (10px + 20px)
        SCREEN.blit(title_text, title_rect)

        # Render Black and White Pieces titles
        SCREEN.blit(black_pieces_text, black_pieces_rect)
        SCREEN.blit(white_pieces_text, white_pieces_rect)

        for element in elements:
            element.change_color(mouse_pos)
            element.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle button text based on the option clicked
                if button1.checkforinput(mouse_pos):
                    button1_option_index = (button1_option_index + 1) % len(button_options)
                    button1.text_input = button_options[button1_option_index]
                if button2.checkforinput(mouse_pos):
                    button2_option_index = (button2_option_index + 1) % len(button_options)
                    button2.text_input = button_options[button2_option_index]

                # Handle "Back" button
                if back_button.checkforinput(mouse_pos):
                    menu()  # Go back to the main menu

                # Handle the "Play" button click
                if play_button.checkforinput(mouse_pos):
                    black_piece_choice = button1.text_input
                    white_piece_choice = button2.text_input
                    print(f"Black Pieces: {black_piece_choice}")
                    print(f"White Pieces: {white_piece_choice}")
                    return  # Stop this function and proceed to the game

        pygame.display.update()

if __name__ == "__main__":
    settings = Settings()  # Create an instance of the Settings class
    menu()