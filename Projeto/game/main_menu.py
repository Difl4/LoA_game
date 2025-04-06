import pygame
import sys
from ui.button import Button
from ui.option_button import OptionButton

class MainMenu:
    def __init__(self, game):
        """Initialize the main menu with buttons."""
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.running = True

        # Load background image
        self.background_image = pygame.image.load('images/background.bmp')
        self.background_image = pygame.transform.scale(
            self.background_image, 
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.background_rect = self.background_image.get_rect()

        # Title text
        self.title_font = pygame.font.SysFont(None, 100)
        self.title_text = self.title_font.render("Lines of Action", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(self.settings.screen_width // 2, 100))

        # Main menu buttons
        self.main_play_button = Button(
            self.game, "Play", 0.5, 0.5, 
            (220,220,220), self.settings.COLOR_HOVER
        )
        self.settings_button = Button(
            self.game, "Settings", 0.5, 0.7, 
            (220,220,220), self.settings.COLOR_HOVER
        )
        self.back_button = Button(
            self.game, "BACK", 0.5, 0.9, 
            self.settings.COLOR_BASE, self.settings.COLOR_BACK_HOVER
        )

        # Play screen buttons
        self.play_screen_play_button = Button(
            self.game, "Start Game", 0.5, 0.7,
            (240,240,240), self.settings.COLOR_HOVER
        )

        # Board size selector
        self.board_size_selector = OptionButton(
            self.game, 
            f"Board Size: {self.settings.rows}x{self.settings.cols}", 
            0.5, 0.55
        )
        # Customize the options for board size
        self.board_size_selector.options = ['6x6', '7x7', '8x8', '9x9', '10x10']
        # Set initial selection based on current settings
        self.board_size_selector.selected_index = self.settings.rows - 6
        self.board_size_selector.update_text()

        # Player selection options
        self.white_selector = OptionButton(self.game, "Human", 0.25, 0.5)
        self.black_selector = OptionButton(self.game, "Human", 0.75, 0.5)

        # Menu state
        self.show_settings = False
        self.show_player_selection = False

    def run_menu(self):
        """Run the menu loop."""
        self.running = True
        self.show_settings = False
        self.show_player_selection = False
        
        while self.running and not self.game.game_flow.game_active:
            self._check_events()
            self._update_screen()
            self.game.clock.tick(self.settings.fps)
            
    def _check_events(self):
        """Handle key and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game.running = False
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.show_player_selection:
                    self._check_play_screen_buttons(mouse_pos)
                    self._check_back_button(mouse_pos)
                    self.white_selector.handle_event(event)
                    self.black_selector.handle_event(event)
                elif self.show_settings:
                    self._check_back_button(mouse_pos)
                    self.board_size_selector.handle_event(event)
                    self._update_board_size()  # Update board size when selection changes
                else:
                    self._check_main_menu_buttons(mouse_pos)

    def _update_board_size(self):
        """Update the board size based on the current selection."""
        size_str = self.board_size_selector.options[self.board_size_selector.selected_index]
        size = int(size_str.split('x')[0])  # Extract the number before 'x'
        self.settings.rows = size
        self.settings.cols = size
        self.settings.square_size = self.settings.screen_width // size
        self.settings.piece_size = (self.settings.square_size, self.settings.square_size)
        self.game.board.reset_board()

    def _check_main_menu_buttons(self, mouse_pos):
        """Check if any main menu button was clicked."""
        if self.main_play_button.rect.collidepoint(mouse_pos):
            self.show_player_selection = True
            self.show_settings = False
        elif self.settings_button.rect.collidepoint(mouse_pos):
            self.show_settings = True
            self.show_player_selection = False

    def _check_play_screen_buttons(self, mouse_pos):
        """Check if play screen buttons were clicked."""
        if self.play_screen_play_button.rect.collidepoint(mouse_pos):
            self._start_game_with_selections()
        elif self.back_button.rect.collidepoint(mouse_pos):
            self.show_player_selection = False

    def _start_game_with_selections(self):
        """Start the game with the current player selections."""
        white_choice = self.settings.player_options[self.white_selector.selected_index]
        black_choice = self.settings.player_options[self.black_selector.selected_index]
        self.game.game_flow.start_game(white_choice, black_choice)
        self.game.game_flow.game_active = True

    def _check_back_button(self, mouse_pos):
        """Go back to the previous menu when the Back button is clicked."""
        if self.back_button.rect.collidepoint(mouse_pos):
            self.show_settings = False
            self.show_player_selection = False

    def _update_screen(self):
        """Update and redraw the game screen."""
        self.screen.blit(self.background_image, self.background_rect)

        if self.show_settings:
            self.board_size_selector.update()
            self.back_button.update()
            self._draw_title_text()
            self._draw_board_size_label()
        elif self.show_player_selection:
            self.white_selector.update()
            self.black_selector.update()
            self.play_screen_play_button.update()
            self.back_button.update()
            self._draw_title_text()
            self._draw_player_labels()
        else:
            self.main_play_button.update()
            self.settings_button.update()
            self._draw_title_text()

        pygame.display.flip()

    def _draw_board_size_label(self):
        """Draw label for the board size selector."""
        font = pygame.font.SysFont(None, 36)
        label = font.render("Board Size:", True, (255, 255, 255))
        label_rect = label.get_rect(center=(
            self.board_size_selector.rect.centerx,
            self.board_size_selector.rect.y - 30
        ))
        self.screen.blit(label, label_rect)

    def _draw_player_labels(self):
        """Draw labels for the player selection options."""
        font = pygame.font.SysFont(None, 36)
        
        white_label = font.render("White Player:", True, (255, 255, 255))
        white_rect = white_label.get_rect(center=(
            self.white_selector.rect.centerx,
            self.white_selector.rect.y - 30
        ))
        
        black_label = font.render("Black Player:", True, (255, 255, 255))
        black_rect = black_label.get_rect(center=(
            self.black_selector.rect.centerx,
            self.black_selector.rect.y - 30
        ))
        
        self.screen.blit(white_label, white_rect)
        self.screen.blit(black_label, black_rect)

    def _draw_title_text(self):
        """Draw the title on the screen."""
        self.screen.blit(self.title_text, self.title_rect)