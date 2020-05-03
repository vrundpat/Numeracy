import pygame


# noinspection SpellCheckingInspection
class Tile(object):
    def __init__(self, x, y, w, h, window):
        self.x = x  # row num
        self.y = y  # col num
        self.w = w  # width
        self.h = h  # height
        self.window = window  # Refrence to the pygame window
        self.color = (255, 255, 255)  # RGB Color values for white

    def draw(self):
        """
        Draw the Tile as a rectangle based on the position and width/height
        :return: None
        """
        # Draw function: pygame.draw.rect(window, RGB Tuple, (x-pixel value, y-pixel value, width, height))
        pygame.draw.rect(self.window, self.color, (self.x * self.w, self.y * self.h, self.w, self.h))
