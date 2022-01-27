import time

import pyautogui
from enum import Enum


class Hotkeys(Enum):
    """
    What the current keybindings are set to in mGBA
    """
    A_BUTTON = 'x'
    B_BUTTON = 'z'
    L_BUTTON = 'a'
    R_BUTTON = 's'
    START = 'enter'
    SELECT = 'del'
    DPAD_UP = 'up'
    DPAD_DOWN = 'down'
    DPAD_LEFT = 'left'
    DPAD_RIGHT = 'right'


class FEController:
    """
    An representation of the state of the cursor in the game state
    Holds the x and y position on the grid of the cursor and updates accordingly as it moves
    from tile to tile

    This class is also used to interface with button presses
    """

    def __init__(self, delay=0.01):
        self.cursor_x = 0
        self.cursor_y = 0
        self.button_delay = delay

    def set_cursor_position(self, x, y):
        """
        internally sets the cursor position
        this does not move the mouse, it SETS

        :param x:
        :param y:
        :return:
        """
        self.cursor_x = x
        self.cursor_y = y

    def move_cursor_to_position(self, x, y):
        pyautogui.countdown(3)
        """
        Moves the cursor to the position specified from it's current x and y

        :param x: desired x coordinate
        :param y: desired y coordinate
        :return:
        """
        manhattan_x = x - self.cursor_x
        manhattan_y = y - self.cursor_y

        print(manhattan_x)
        print(manhattan_y)

        if manhattan_x > 0:
            self.input(Hotkeys.DPAD_RIGHT, abs(manhattan_x))
        elif manhattan_x < 0:
            self.input(Hotkeys.DPAD_LEFT, abs(manhattan_x))

        if manhattan_y > 0:
            self.input(Hotkeys.DPAD_UP, abs(manhattan_y))
        elif manhattan_y < 0:
            self.input(Hotkeys.DPAD_DOWN, abs(manhattan_y))

        self.cursor_x = x
        self.cursor_y = y

    def input(self, button: Hotkeys, n=1):
        """
        Executes a button press given by key n times.

        :param button: must be an enum that is a member of the Hotkeys class
        :param n: the amount of times to execute the key press
        :return:
        """
        for i in range(n):
            pyautogui.keyDown(button.value)
            pyautogui.sleep(self.button_delay)
            pyautogui.keyUp(button.value)

