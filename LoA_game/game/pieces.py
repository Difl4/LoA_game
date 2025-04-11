import pygame

class Piece(pygame.sprite.Sprite):
    """A class to represent a game piece."""

    def __init__(self, settings, color, pos):
        """
        Initialize the piece.
        
        Args:
            settings: An instance of the Settings class.
            color: The color of the piece ('white' or 'black').
            pos: A tuple (x, y) representing the pixel position of the piece.
        """
        super().__init__()
        # Load the piece image based on color.
        image_path = settings.white_piece if color == 'white' else settings.black_piece
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, settings.piece_size)
        self.rect = self.image.get_rect(topleft=pos)