import pygame
import sys
from config.settings import Settings
from button import Button
from game.lines_of_action import LinesOfAction

# Initialize Pygame
pygame.init()
pygame.font.init()

# Initialize settings instance
settings = Settings()
SCREEN_WIDTH = settings.screen_width
SCREEN_HEIGHT = settings.screen_height
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Load background image and adjust its size
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define colors used in the UI
COLOR_BASE = "#e8d1a5"
COLOR_HOVER = "white"
COLOR_BACK_HOVER = "Green"
COLOR_BLACK = "black"

# Cache for font loading
FONT_CACHE = {}
CUSTOM_FONT_PATH = 'nunito_sans/NunitoSans-Regular.ttf'  # Path to custom font

def get_font(size):
    """
    This function loads and returns a font of the specified size.
    It first tries to load the font from the custom font path. 
    If the font is not found, it falls back to the system font.
    
    :param size: The font size to be returned.
    :return: The Pygame Font object.
    """
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

def display_screen(title, subtitle, elements):
    """
    This function displays a screen with a title, subtitle, and a list of interactive elements.
    
    :param title: The main title text to be displayed at the top of the screen.
    :param subtitle: A subtitle text to be displayed below the main title.
    :param elements: A list of button elements that will be displayed on the screen.
    :return: The text of the element that was clicked by the user.
    """
    pygame.display.set_caption(title)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(background, (0, 0))

        # Render and display the main title and subtitle
        title_font_size = 120
        title_text1 = get_font(title_font_size).render("Lines", True, COLOR_BASE)
        title_text2 = get_font(title_font_size).render("of Action", True, COLOR_BASE)

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
    """
    This function handles the settings screen where the user can select the board size.
    
    :param settings: The settings object that holds the configuration for the game.
    """
    back_button = Button(None, (65, SCREEN_HEIGHT - 65), "BACK", get_font(45), COLOR_BASE, COLOR_BACK_HOVER)

    title_font = get_font(60)
    title_text = title_font.render("Choose Board Size", True, COLOR_BASE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))

    button_y_start = 300
    button_spacing = 80
    board_size_button_1 = Button(None, (SCREEN_WIDTH // 2, button_y_start), "8x8", get_font(60), COLOR_BASE, COLOR_HOVER)
    board_size_button_2 = Button(None, (SCREEN_WIDTH // 2, button_y_start + button_spacing), "10x10", get_font(60), COLOR_BASE, COLOR_HOVER)
    board_size_button_3 = Button(None, (SCREEN_WIDTH // 2, button_y_start + 2 * button_spacing), "12x12", get_font(60), COLOR_BASE, COLOR_HOVER)

    elements = [back_button, board_size_button_1, board_size_button_2, board_size_button_3]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.blit(background, (0, 0))
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
                        if element.text_input == "BACK":
                            menu()
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
    """
    This function displays the main menu with the options to play the game or access settings.
    """
    play_button = Button(None, (SCREEN_WIDTH // 2, 375), "PLAY", get_font(75), COLOR_BASE, COLOR_HOVER)
    settings_button = Button(None, (SCREEN_WIDTH // 2, 525), "SETTINGS", get_font(75), COLOR_BASE, COLOR_HOVER)

    elements = [play_button, settings_button]
    choice = display_screen("Lines of Action", "", elements)

    if choice == "PLAY":
        play()
    elif choice == "SETTINGS":
        settings_screen(settings)

def play():
    """
    This function handles the game setup screen where players can select their piece types and options.
    """
    button1_option_index = 0
    button2_option_index = 0
    button_options = ['Human', 'Minimax', 'Minimax α-β', 'Negamax', 'Negamax α-β', 'MCTS']
    
    back_button = Button(None, (65, SCREEN_HEIGHT - 65), "BACK", get_font(45), COLOR_BASE, COLOR_BACK_HOVER)
    
    button1 = Button(None, (SCREEN_WIDTH // 2 - 150, 375), button_options[button1_option_index], get_font(60), COLOR_BASE, COLOR_HOVER)
    button2 = Button(None, (SCREEN_WIDTH // 2 + 150, 375), button_options[button2_option_index], get_font(60), COLOR_BASE, COLOR_HOVER)

    black_pieces_text = get_font(40).render("Black Pieces", True, COLOR_BASE)
    black_pieces_rect = black_pieces_text.get_rect(center=(SCREEN_WIDTH // 2 - 150, 375 - 50))

    white_pieces_text = get_font(40).render("White Pieces", True, COLOR_BASE)
    white_pieces_rect = white_pieces_text.get_rect(center=(SCREEN_WIDTH // 2 + 150, 375 - 50))

    play_button = Button(None, (SCREEN_WIDTH // 2, 475 + 100), "PLAY", get_font(75), COLOR_BASE, COLOR_HOVER)

    elements = [back_button, button1, button2, play_button]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.blit(background, (0, 0))

        title_font_size = 120
        title_text = get_font(title_font_size).render("Lines of Action", True, COLOR_BASE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 75 + 30))  
        SCREEN.blit(title_text, title_rect)

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
                if button1.checkforinput(mouse_pos):
                    button1_option_index = (button1_option_index + 1) % len(button_options)
                    button1.text_input = button_options[button1_option_index]
                if button2.checkforinput(mouse_pos):
                    button2_option_index = (button2_option_index + 1) % len(button_options)
                    button2.text_input = button_options[button2_option_index]

                if back_button.checkforinput(mouse_pos):
                    menu()

                if play_button.checkforinput(mouse_pos):
                    black_piece_choice = button1.text_input
                    white_piece_choice = button2.text_input
                    print(f"Black Pieces: {black_piece_choice}")
                    print(f"White Pieces: {white_piece_choice}")
                    start_game(black_piece_choice, white_piece_choice)  # Start the game here
                    return

        pygame.display.update()

if __name__ == "__main__":
    settings = Settings()  # Create an instance of the Settings class
    menu()  # Start the menu screen
