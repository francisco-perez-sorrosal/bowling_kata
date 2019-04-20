# TODO: Refactor this shit
from enum import Enum

REGULAR_FRAMES_IN_GAME = 10


class RollOutput(Enum):
    REGULAR, STRIKE, SPARE = range(3)


def get_points_per_roll(roll_char, previous_roll_points=0):
    if roll_char in [str(j) for j in range(1, 10)]:
        return RollOutput.REGULAR, int(roll_char)
    elif roll_char == '-':
        return RollOutput.REGULAR, 0
    elif roll_char == 'X':
        return RollOutput.STRIKE, 10
    else:  # '/'
        return RollOutput.SPARE, 10 - previous_roll_points


class BaseFrame:

    def __init__(self, frame_str):
        self.frame_str = frame_str
        self.next_frame = None
        self.rolls = [0, 0]
        self.strike = False
        self.spare = False

    def set_next_frame(self, frame):
        self.next_frame = frame

    def calculate_play_points(self):
        points = 0
        if self.spare:
            points += self.next_frame.rolls[0]
        if self.strike:
            points += self.next_frame.calculate_points()
            if self.next_frame.strike:
                points += self.next_frame.next_frame.rolls[0]
        return points

    def calculate_points(self):
        return sum(self.rolls)


class RegularFrame(BaseFrame):

    def __init__(self, frame_str):
        super().__init__(frame_str)

        for i, char in enumerate(self.frame_str):
            roll_output, self.rolls[i] = get_points_per_roll(char) if i == 0 else get_points_per_roll(char, self.rolls[i - 1])
            if roll_output == RollOutput.STRIKE:
                self.strike = True
            if roll_output == RollOutput.SPARE:
                self.spare = True


class ExtraFrame(BaseFrame):

    def __init__(self, frame_str):
        super().__init__(frame_str)

        for i, char in enumerate(self.frame_str):
            roll_output, self.rolls[i] = get_points_per_roll(char) if i == 0 else get_points_per_roll(char, self.rolls[i - 1])


class Bowling:

    def calculate_result(self, game_str):
        frames = self.get_frames(game_str)
        return self.calculate_frames_points(frames)

    def calculate_frames_points(self, frames):
        frames_points = 0
        print(len(frames))
        for i in range(REGULAR_FRAMES_IN_GAME):
            print(i)
            frame = frames[i]
            frames_points += frame.calculate_points() + frame.calculate_play_points()
        return frames_points

    def get_frames(self, game_str):
        regular_frames_str, extra_frame_str = game_str.split('||')
        frames = self.get_regular_frames(regular_frames_str)
        frames.append(ExtraFrame(extra_frame_str))
        for i in range(REGULAR_FRAMES_IN_GAME):
            frames[i].set_next_frame(frames[i + 1])
        return frames

    def get_regular_frames(self, frames_str):
        frames_strs = frames_str.split('|')
        frames = []
        for frame_str in frames_strs:
            frames.append(RegularFrame(frame_str))
        assert len(frames) == REGULAR_FRAMES_IN_GAME
        return frames
