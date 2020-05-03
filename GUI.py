import pygame
from Tile import Tile


# IMPORTANT RESOURCES USED:
#   Pygame:
#       - https://www.pygame.org/docs/

WIN_HEIGHT = 560   # Length of the Window
WIN_LENGTH = 560   # Height of the Window
width = 20  # Width of each tile and distance between the horizontal and vertical lines
COLOR = (255, 255, 255)  # Color which will be used to paint the entire window (in this case its white)


# noinspection SpellCheckingInspection
class Grid(object):
    def __init__(self, window):
        self.window = window  # PyGame Window built-in object
        self.font_object = pygame.font.SysFont("arial", 35)
        self.acc = "N/A"
        self.pred = "N/A"
        self.tiles = self.generate_tiles()  # Initialize the Tiles
        self.gui_update()  # On instantiation, draw the lines

    def generate_tiles(self):
        """
        Creates the Tile objects for the GUI, stores them in a state variable
        :return: List[List[Tile]]
        """

        # Inner Loop will create a list of size 28 Tile Objects and append that list to another list which will iterate 28 times creating a 2-D List
        tiles = [[Tile(x, y, width, width, self.window) for y in range(28)] for x in range(28)]
        return tiles

    def gui_update(self):
        """
        Draw the lines of the Grid and the Red Box for drawing on the PyGame window
        :return: None
        """
        # Base for the Text
        pygame.draw.rect(self.window, (0, 0, 0), (0, 0, WIN_LENGTH, 40))

        # Line drawing function: pygame.draw.line(window, RGB color Tuple, Start Point, End Point
        for pix in range(WIN_LENGTH // width):  # Draw WIN_LENGTH / WIDTH + 1 horizontal and vertical lines on the screen sapce
            pygame.draw.line(self.window, (12, 149, 240), (pix * width, 0), (pix * width, WIN_HEIGHT))
            pygame.draw.line(self.window, (12, 149, 240), (0, pix * width), (WIN_LENGTH, pix * width))

        #  Lines for the Red Drawing space
        pygame.draw.line(self.window, (61, 104, 189), (4 * 20, 4 * 20), (24 * 20, 4 * 20), 2)
        pygame.draw.line(self.window, (61, 104, 189), (4 * 20, 4 * 20), (4 * 20, 24 * 20), 2)
        pygame.draw.line(self.window, (61, 104, 189), (24 * 20, 4 * 20), (24 * 20, 24 * 20), 2)
        pygame.draw.line(self.window, (61, 104, 189), (4 * 20, 24 * 20), (24 * 20, 24 * 20), 2)

        self.blit_text()

    def reset(self):
        """
        Reset each Tile's color to (255, 255, 255), to mimic "clearing" of the drawing space
        :return: None
        """
        for row in self.tiles:
            for col in row:
                col.color = (255, 255, 255)
        self.window.fill(COLOR)
        self.gui_update()

    def getNeighbors(self, pos_X, pos_Y):
        """
        Get the surrounding Tiles of a given tile based on its position (Adjacent and Diagonal Tiles are considered neighbors)
        :param pos_X: Row in Grid
        :param pos_Y: Column in Grid
        :return: List[Tile]
        """
        neighbors = [self.tiles[pos_X][pos_Y]]  # Neighbors List initialized with the Tile being checked
        if 4 <= pos_X < 23: neighbors.append(self.tiles[pos_X + 1][pos_Y])  # Right
        if 4 < pos_X <= 23: neighbors.append(self.tiles[pos_X - 1][pos_Y])  # Left
        if 4 <= pos_Y < 23: neighbors.append(self.tiles[pos_X][pos_Y + 1])  # Bottom
        if 4 < pos_Y <= 23: neighbors.append(self.tiles[pos_X][pos_Y - 1])  # Top
        if 4 < pos_X <= 23 and 4 < pos_Y <= 23: neighbors.append(self.tiles[pos_X - 1][pos_Y - 1])  # Top Left
        if 4 <= pos_X < 23 and 4 < pos_Y <= 23: neighbors.append(self.tiles[pos_X + 1][pos_Y - 1])  # Top Right
        if 4 < pos_X <= 23 and 4 <= pos_Y < 23: neighbors.append(self.tiles[pos_X - 1][pos_Y + 1])  # Bottom Left
        if 4 <= pos_X < 23 and 4 <= pos_Y < 23: neighbors.append(self.tiles[pos_X + 1][pos_Y + 1])  # Bottom Right

        return neighbors

    def getMatrix(self):
        """
        Create a 2-dimensional list of the tiles, in an transposed orientation of the GUI Grid, marking each colored tile with 1 and each
        uncolored with a 0, creating a matrix similar to that of the MNIST Data
        :return: List[List[Int]]
        """
        matrix = []
        for row in self.tiles:
            temp = []  # 1-D List to hold each row
            for col in row:
                if col.color == (0, 0, 0):  # If Tile is colored, append 1 (skewed Highest Gray-Scale value)
                    temp.append(1)
                else:
                    temp.append(0)  # If the Tile is uncolored, append 0 (lowest Gray-Scale value)
            matrix.append(temp)  # Append the row onto the Matrix
        return matrix

    def blit_text(self):
        """
        Blit the accuracy and prediction texts onto the pygame window
        :return: None
        """
        if self.acc != "N/A":
            acc = self.font_object.render("Accuracy: " + str(round(float(self.acc), 2)) + "%", 25, (255, 255, 255))
        else:
            acc = self.font_object.render("Accuracy: " + self.acc, 25, (255, 255, 255))
        self.window.blit(acc, (20, 10))
        pred = self.font_object.render("Prediction: " + self.pred, 25, (255, 255, 255))
        self.window.blit(pred, (360, 10))

