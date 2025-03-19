def get_matrix_position(x, y, square_size):
    """Convert pixel position (x, y) to matrix indices (row, col)."""
    row = y // square_size
    col = x // square_size
    return row, col

def get_pixel_position(row, col, square_size):
    """Convert matrix indices (row, col) to pixel coordinates (x, y)."""
    x = col * square_size
    y = row * square_size
    return x, y