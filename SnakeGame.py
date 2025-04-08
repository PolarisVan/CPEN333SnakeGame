# Group#: B21
# Student Names: Peiyu Qu and Dalisio Pereira Neto

"""
    This program implements a variety of the snake
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue  # the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """

    def __init__(self):
        """
            The initializer instantiates the main window and
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        # some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        # instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT, bg=BACKGROUND_COLOUR)
        self.canvas.pack()
        # create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        # display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour,
            text='Your Score: 0', font=("Helvetica", "11", "bold"))
        # binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self) -> None:
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!",
                                height=3, width=10, font=("Helvetica", "14", "bold"),
                                command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """

    def __init__(self):
        self.queue = gameQueue
        self.gui = gui
        self.queueHandler()

    def queueHandler(self) -> None:
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)

class Game():
    '''
        This class implements most of the game functionalities.
    '''

    def __init__(self):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = gameQueue
        self.score = 0
        # starting length and location of the snake
        # note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        # initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move"
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.1  # speed of snake updates (sec)
        while self.gameNotOver:
            self.move()
            time.sleep(SPEED)  # frame rate

    def whenAnArrowKeyIsPressed(self, e: object) -> None:
        """
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        # ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or
                currentDirection == "Right" and e.keysym == "Left" or
                currentDirection == "Up" and e.keysym == "Down" or
                currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate.
            If based on this new movement, the prey has been
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if
            the game should be over.
            The snake coordinates list (representing its length
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        #everything under this was implemented
        self.isGameOver(NewSnakeCoordinates)

        self.snakeCoordinates.append(NewSnakeCoordinates)

        distance_between = tuple(map(lambda i, j: abs(i - j), NewSnakeCoordinates, self.prey))

        if self.direction == "Left" or self.direction == "Right":

            if all(x < y for x, y in zip(distance_between, (
            (PREY_ICON_WIDTH+SNAKE_ICON_LENGTH)/2, (PREY_ICON_WIDTH+SNAKE_ICON_WIDTH)/2))):
                self.score += 1
                self.createNewPrey()

            else:
                self.snakeCoordinates.pop(0)

            self.queue.put({"move": self.snakeCoordinates})
            self.queue.put({"score": self.score})

        else:

            if all(x < y for x, y in zip(distance_between, (
            (PREY_ICON_WIDTH + SNAKE_ICON_WIDTH) / 2, (PREY_ICON_WIDTH + SNAKE_ICON_LENGTH) / 2))):
                self.score += 1
                self.createNewPrey()

            else:
                self.snakeCoordinates.pop(0)

            self.queue.put({"move": self.snakeCoordinates})
            self.queue.put({"score": self.score})

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of
            head of the snake.
            It is used by the move() method.
        """
        lastX, lastY = self.snakeCoordinates[-1]
        #everything under this was implemented
        if self.direction == "Left":
            lastX = lastX - SNAKE_ICON_LENGTH

        elif self.direction == "Right":
            lastX = lastX + SNAKE_ICON_LENGTH

        elif self.direction == "Up":
            lastY = lastY - SNAKE_ICON_LENGTH

        else:
            lastY = lastY + SNAKE_ICON_LENGTH

        return (lastX, lastY)

    def isGameOver(self, snakeCoordinates: tuple) -> None:
        """
            This method checks if the game is over by
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver
            field and also adds a "game_over" task to the queue.
        """
        x, y = snakeCoordinates
        #returns game over if snake body is in the same position as the window's border, False otherwise

        if self.direction == "Left" or self.direction == "Right":
            if x - SNAKE_ICON_LENGTH/2 < 0 or x + SNAKE_ICON_LENGTH/2 > WINDOW_WIDTH or y - SNAKE_ICON_WIDTH/2 < 0 or y + SNAKE_ICON_WIDTH/2 > WINDOW_HEIGHT or snakeCoordinates in self.snakeCoordinates:
                self.gameNotOver = False
                self.queue.put({"game_over"})

        else:
            if x - SNAKE_ICON_WIDTH/2 < 0 or x + SNAKE_ICON_WIDTH/2 > WINDOW_WIDTH or y - SNAKE_ICON_LENGTH/2 < 0 or y + SNAKE_ICON_LENGTH/2 > WINDOW_HEIGHT or snakeCoordinates in self.snakeCoordinates:
                self.gameNotOver = False
                self.queue.put({"game_over"})

    def createNewPrey(self) -> None:
        """
            This methods picks an x and a y randomly as the coordinate
            of the new prey and uses that to calculate the
            coordinates (x - 5, y - 5, x + 5, y + 5). [you need to replace 5 with a constant]
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the
            queue handler to represent the new prey.
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls.
        """
        THRESHOLD = 15  # sets how close prey can be to borders
        # assumes initial overlapping to be checked
        x_max, y_max = 110,25

        Overlap = True
        while Overlap:
            # creates random temporary prey coordinates to be checked for overlapping
            x = random.randint(THRESHOLD, WINDOW_WIDTH - THRESHOLD)
            y = random.randint(THRESHOLD, WINDOW_HEIGHT - THRESHOLD)
            greater_edge = max(SNAKE_ICON_LENGTH,SNAKE_ICON_WIDTH)
            self.prey = (x, y)

            Overlap = False
            # ensures that the prey is not created under the scoreboard
            if (not (x > x_max)) and (not (y > y_max)):

                Overlap = True
            # ensures that the prey is not created under the snake's body
            else:
                for item in self.snakeCoordinates:
                    distance_between = tuple(map(lambda i, j: abs(i - j), item, self.prey))

                    if (all(x < y for x, y in zip(distance_between, ((PREY_ICON_WIDTH+greater_edge)/2, (PREY_ICON_WIDTH+greater_edge)/2)))):
                        Overlap = True
                        break
        # adds prey to window when no overlap
        self.queue.put({"prey": (x - PREY_ICON_WIDTH/2, y - PREY_ICON_WIDTH/2, x + PREY_ICON_WIDTH/2, y + PREY_ICON_WIDTH/2)})

if __name__ == "__main__":
    # some constants for our GUI
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 300
    SNAKE_ICON_WIDTH = 100
    SNAKE_ICON_LENGTH = 10  # Constant(should not change) implemented
    PREY_ICON_WIDTH = 10 # implemented

    BACKGROUND_COLOUR = "green"  # you may change this colour if you wish
    ICON_COLOUR = "yellow"  # you may change this colour if you wish

    gameQueue = queue.Queue()  # instantiate a queue object using python's queue class

    game = Game()  # instantiate the game object

    gui = Gui()  # instantiate the game user interface

    QueueHandler()  # instantiate the queue handler

    # start a thread with the main loop of the game
    threading.Thread(target=game.superloop, daemon=True).start()

    # start the GUI's own event loop
    gui.root.mainloop()
