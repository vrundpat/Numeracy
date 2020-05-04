from mvc.view.GUI import Grid
import pygame
from mvc.server.Client import Client
import random


class User(object):
    def __init__(self):
        self.connection = Client() # Create the client instance when the User is created
        self.main()  # Call the infinite loop main function, which will be responsible for interacting with the GUI

    def main(self):
        pygame.init()  # Initialze the pygame modeule
        WIN_HEIGHT = WIN_LENGTH = 560  # Set window parameters
        COLOR = (255, 255, 255)
        window = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))  # Create the window
        window.fill(COLOR)  # Color the window to white
        width = 20 # Width of the lines and tiles

        gui = Grid(window)  # Instantiate the GUI Object
        gui.gui_update()

        while True:
            for events in pygame.event.get():  # Poll the events that happened in this frame
                if events.type == pygame.QUIT:
                    pygame.quit()

                if pygame.mouse.get_pressed()[0]:  # Get the event representing the Left Mouse Click
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get cursor position
                    x = float(mouse_x / WIN_LENGTH) * (WIN_LENGTH / width)  # Get the position of the tile that was clicked in this frame
                    y = float(mouse_y / WIN_HEIGHT) * (WIN_HEIGHT / width)
                    if 4 <= int(x) <= 23 and 4 <= int(y) <= 23:
                        neighboring_tiles = gui.getNeighbors(int(x), int(y))  # Get the neighbors of the clicked tile

                        # Since this is where the cursor was most prominently placed, this tile will get a gray scale of 1 (compltely black)
                        neighboring_tiles[0].gs_value = 1
                        neighboring_tiles[0].color = (0, 0, 0)
                        neighboring_tiles[0].draw()

                        for tile in neighboring_tiles[1:]:  # Color the neighhboring 8 tiles of the selected tile
                            tile.color = (0, 0, 0)
                            # Since these tiles are the neighbors, they will at most have 80% of the selected tiles grayscale values, minimum being 40%
                            tile.gs_value = round(random.uniform(0.6, 0.85), 5)
                            tile.draw()

                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_w:
                        accuracy = self.connection.send("Accuracy") # Send need accuracy message
                        if accuracy is not None: gui.acc = accuracy
                        pygame.display.update()
                    else:
                        binaryMatrix = gui.getMatrix()
                        guess = self.connection.send(binaryMatrix)  # Send input to the server and get the predicion made by the network
                        if guess is not None: gui.pred = guess

                if pygame.mouse.get_pressed()[2]:  # Event of the Right Mouse Click
                    gui.reset()  # Reset the GUI to its initial state by reverting tile colors

            gui.gui_update()  # Draw lines before start of next frame
            pygame.display.flip()  # Update the window before next frame

