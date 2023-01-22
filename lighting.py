import logging
import math
from typing import NamedTuple

import numpy as np
import pygame

from conts import HEIGHT, WIDTH, TILE_SIZE


class Line(NamedTuple):

    start: tuple
    end: tuple

    def find_len(self):
        # find whole number of pixel along line
        diff_x = self.end[0] - self.start[0]
        diff_y = self.end[1] - self.start[1]
        return math.ceil(math.hypot(diff_x, diff_y))

    @property
    def angle(self):
        return math.atan2(self.end[1] - self.start[1], self.end[0] - self.start[0])

    def find_angle(self, point):
        return math.atan2(point[1] - self.start[1], point[0] - self.start[0])

    def _find_intersection(self, rect):
        points = [rect.topleft, rect.bottomleft, rect.topright, rect.bottomright]

        angles = [self.find_angle(i) for i in points]
        max_angle = max(angles)
        min_angle = min(angles)
        angle = self.angle
        if angle < min_angle or angle > max_angle:
            return

        points = np.linspace(self.start, self.end, self.find_len())

        # use 2 egg problem
        # find which point collides
        for index, point in enumerate(points[:31]):
            # check if point in rect
            if rect.collidepoint(point):
                return list(point)

        for index, point in enumerate(points[::30]):
            # check if point in rect
            if rect.collidepoint(point):
                break

        for point in points[index - 2 :]:
            if rect.collidepoint(point):
                return list(point)

        return False

    def find_intersection(self, others):
        if not others:
            return False

        points = []
        for i in others:
            # line[0] = pos of mouse
            angle_range = find_angles(i, self.start)

            # find angle of line
            dx = abs(self.end[0] - self.start[0])
            dy = abs(self.end[1] - self.start[1])
            theata = math.atan2(dx, dy)
            direction = angle_range[0] > theata or angle_range[1] < theata
            if not direction:
                continue

            if point := self._find_intersection(i):
                points.append(point)

        min_point = self[-1]
        min_dis = math.hypot(self.start[0] - self.end[0], self.start[1] - self.end[1])
        for i in points:
            if min_dis > (
                dis := math.hypot(self.start[0] - i[0], self.start[1] - i[1])
            ):
                min_dis = dis
                min_point = i
        return min_point


def get_corners(rect):
    c1 = (rect[0], rect[1])
    c2 = (rect[0], rect[1] + rect[3])
    c3 = (rect[0] + rect[2], rect[1])
    c4 = (rect[0] + rect[2], rect[1] + rect[3])

    return [c1, c2, c3, c4]


def find_angles(rect, pos):
    min_theata = 10_000
    max_theata = -10_000
    for i in get_corners(rect):
        dx = abs(i[0] - pos[0])
        dy = abs(i[1] - pos[1])
        _theata = math.atan2(dx, dy)

        min_theata = min(min_theata, _theata)
        max_theata = max(max_theata, _theata)

    return (max_theata, min_theata)


def check_others(others, mouse_pos):
    for i in others:
        if i.collidepoint(mouse_pos):
            return i


def get_rays(pos, others, coners):
    logging.info(f"{pos=}, f{len(others)}")
    if others:
        if check_others(others, pos):
            return False
    points = []

    for i in coners:
        x, y = i
        last_point = (x, y)
        if new := Line(pos, last_point).find_intersection(others):
            last_point = new

        points.append(last_point)

    points = [tuple(i) for i in points]
    angles_and_points = [(i, math.atan2(i[1] - pos[1], i[0] - pos[0])) for i in points]
    angles_and_points.sort(key=lambda x: x[1])
    points = [i[0] for i in angles_and_points]

    return points
