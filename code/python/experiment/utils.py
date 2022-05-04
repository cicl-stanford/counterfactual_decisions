import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import json
import numpy as np
from numpy.random import rand
from scipy.stats import binom
import shutil
import pygame


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FLOOR = (255, 255, 255)  # white
    LINE = (200, 200, 200)   # light gray
    WALL = (0, 0, 0)         # black
    DOOR = (130, 130, 130)   # dark gray
    AGENT = (150, 110, 180)
    LIGHT_RED = (255, 190, 190)
    LIGHT_BLUE = (180, 230, 255)


def str_to_color(color):
    return Color.LIGHT_RED if color == "red" else Color.LIGHT_BLUE


def opp_color(color):
    return "red" if color == "blue" else "blue"


DOWN, UP, LEFT, RIGHT, STAY = (0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)


def get_action_from_location(location_one, location_two):
    return tuple(map(lambda i, j: i - j, location_two, location_one))


def bernoulli(p):
    if rand() < p:
        return True
    return False


def make_gif(image_dir, file_path, include_00):
    import imageio
    images = []
    for f in sorted(os.listdir(image_dir)):
        if not include_00 and f == '00.png': continue
        images.append(imageio.imread(os.path.join(image_dir, f)))
    # hold first and last frame a little longer
    images = [images[0]]*3 + images
    images += [images[-1]]*3
    imageio.mimsave(file_path + '.gif', images, fps=1.5)


# read in trial information from json
def read_trials():
    return json.load(open('../../experiment/experiment.json', 'r'))


# clear directory or create if doesn't exist
def make_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        for f in os.listdir(path):
            full_f = os.path.join(path, f)
            if os.path.isfile(full_f):
                os.remove(full_f)
            elif os.path.isdir(full_f):
                shutil.rmtree(full_f)


