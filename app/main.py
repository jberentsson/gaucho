#!/usr/bin/env python

import time
from pycaw.utils import AudioSession

from . import utils

TOP_ROW = [91, 92, 93, 94, 95, 96, 97, 98]
RIGHT_ROW = [19, 29, 39, 49, 59, 69, 79, 89]

COLUMN_0 = [11, 21, 31, 41, 51, 61, 71, 81]
COLUMN_1 = [12, 22, 32, 42, 52, 62, 72, 82]
COLUMN_2 = [13, 23, 33, 43, 53, 63, 73, 83]
COLUMN_3 = [14, 24, 34, 44, 54, 64, 74, 84]
COLUMN_4 = [15, 25, 35, 45, 55, 65, 75, 85]
COLUMN_5 = [16, 26, 36, 46, 56, 66, 76, 86]
COLUMN_6 = [17, 27, 37, 47, 57, 67, 77, 87]
COLUMN_7 = [18, 28, 38, 48, 58, 68, 78, 88]

COLUMNS = (
    COLUMN_0
    + COLUMN_1
    + COLUMN_2
    + COLUMN_3
    + COLUMN_4
    + COLUMN_5
    + COLUMN_6
    + COLUMN_7
)


class Main:
    def __init__(self):
        """ """
        self.programs = utils.list_programs()
        self.button_last = -1
        self.lp = None
        self.offset = 0
        self.n = 8
        self.matrix = [[([0] * self.n)] * self.n]
        self.t = time.time()
        self.volumes = {}

    def update_button(self, x: int, y: int):
        """
        Update button (x, y).
        """
        if self.lp is not None:
            self.lp.LedCtrlXYByCode(x, y, 127)

    def clear_button(self, x: int, y: int):
        """
        Clear a button (x, y).
        """
        if self.lp is not None:
            self.lp.LedCtrlXYByCode(x, y, 0)

    def check_thing(self, x, y):
        """ """
        # TODO: Fix the offset.
        return x >= 0 and y >= 1 and x <= 7 and y <= 8

    def update_column(self, x: int, y: int):
        """
        Update all of the column buttons.
        """
        li0 = list(range(0, 9))
        li1 = list(range(y + 1, 9))

        for i in li0:
            if self.check_thing(x, i):
                self.clear_button(x, i)

        for i in li1:
            if self.check_thing(x, i):
                self.update_button(x, i)

    def handle_button(self, button: int):
        """
        Handle the user input.
        """
        x, y = utils.note2xy(button)

        if x >= len(self.programs):
            return None

        if button in TOP_ROW:
            print(f"TOP ROW - {x}")

        elif button in RIGHT_ROW:
            print(f"RIGHT ROW - {y}")

        elif button in COLUMNS:
            utils.set_volume(self.programs[x], y)
            self.update_column(x, y)

        return button

    def handle_program(self, program: AudioSession, p: int):
        """ """
        try:
            vol = utils.get_volume(program, p)
            if vol and type(vol) == int:
                vol = 8 - vol
                run = False

                if str(program.GroupingParam) in self.volumes:
                    if self.volumes[str(program.GroupingParam)] != vol:
                        run = True
                else:
                    self.volumes[str(program.GroupingParam)] = vol
                    run = True

                if run:
                    match vol:
                        case int(vol):
                            if p not in self.volumes:
                                self.volumes[p] = None

                            if self.volumes[p] != vol:
                                self.volumes[p] = vol
                                return self.update_column(p, vol)
                        case _:
                            print(f"Other: {vol}")
                            return None
        except:
            print("Something went wrong!")

    def volume_to_buttons(self):
        """
        Get the program volume from the Windows API.
        """
        buttons_updated = []
        for p, program in enumerate(self.programs):
            hp = self.handle_program(program, p)
            buttons_updated.append(hp)

        for p in range(len(self.programs), 9):
            self.update_column(p, 9)

        return buttons_updated

    def read_buttons(
        self,
    ):
        """
        Read the button stream.
        """
        while True:
            new_programs = utils.list_programs()
            if self.programs != new_programs:
                self.programs = new_programs
                self.volume_to_buttons()

            if self.lp:
                but = self.lp.ButtonStateRaw()
                if but and len(but) and but[1]:
                    self.handle_button(but[0])

    def run(
        self,
    ):
        """ """
        self.lp = utils.detect_controller()

        if self.lp:
            self.lp.Reset()
            print("\nQUIT: Push one single button ten times in a row.\n")
            self.read_buttons()
            print("bye ...")
            self.lp.Reset()
            self.lp.Close()


if __name__ == "__main__":
    Main().run()
