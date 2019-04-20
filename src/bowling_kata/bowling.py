# TODO: Refactor this shit
from enum import Enum


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


class Frame:

    def __init__(self, frame_str, is_extra=False):
        self.frame_str = frame_str
        self.is_extra = is_extra
        self.rolls = [0, 0]
        self.strike = False
        self.spare = False

    def calculate_points(self):
        points = 0
        for i, char in enumerate(self.frame_str):

            roll_output, self.rolls[i] = get_points_per_roll(char) if i == 0 else get_points_per_roll(char, self.rolls[i - 1])
            if not self.is_extra:
                if roll_output == RollOutput.STRIKE:
                    self.strike = True
                if roll_output == RollOutput.SPARE:
                    self.spare = True
        if self.is_extra:
            print(self.rolls)
        return sum(self.rolls)


class Bowling:

    def calculate_result(self, game_str):
        frames, extra_frame = self.split_input(game_str)
        frames_points = self.calculate_frames_points(frames, extra_frame)
        return frames_points

    def calculate_frames_points(self, frames_str, extra_frame_str):
        frames_points = 0
        frames = self.split_frames(frames_str)
        frames.append(Frame(extra_frame_str, True))
        print(len(frames))
        for i in range(10):
            print(i)
            frame = frames[i]
            frames_points += frame.calculate_points()
            if frame.spare:
                frames[i + 1].calculate_points()
                frames_points += frames[i + 1].rolls[0]
            if frame.strike:
                frames_points += frames[i + 1].calculate_points()
                if frames[i + 1].strike and i + 2 < len(frames):
                    frames[i + 2].calculate_points()
                    frames_points += frames[i + 2].rolls[0]
                if i == 9:
                    print("a {} {}".format(frames[i + 1].calculate_points(), frames[i + 1].is_extra))
        return frames_points

    def split_input(self, game_str):
        return game_str.split('||')

    def split_frames(self, frames_str):
        frames_strs = frames_str.split('|')
        frames = []
        for frame_str in frames_strs:
            frames.append(Frame(frame_str))
        assert len(frames) == 10
        return frames
