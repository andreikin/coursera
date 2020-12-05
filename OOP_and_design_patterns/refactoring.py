#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier):
        return Vec2d(self.x * multiplier, self.y * multiplier)

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)

    def length(self):
        # return length of vector
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        return (self.x, self.y)


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []
        self.movement = False

    def add_point(self, coord):
        self.points.append(Vec2d(*coord))
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def del_point(self, coord, accuracy=10):
        for i in range(len(self.points)):
            test_x = abs(self.points[i].x - coord[0]) < accuracy
            test_y = abs(self.points[i].y - coord[1]) < accuracy
            if test_x and test_y:
                self.points.pop(i)
                self.speeds.pop(i)
                break

    def draw(self, width=3, color=(255, 255, 255), style="points"):
        if style == "points":
            for point in self.points:
                pygame.draw.circle(gameDisplay, color, (int(point.x), int(point.y)), width)

        if style == "line":
            for i in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(self.points[i].x), int(self.points[i].y)),
                                 (int(self.points[i + 1].x), int(self.points[i + 1].y)), width)

    def set_points(self):
        if self.movement:
            for i in range(len(self.points)):
                self.points[i] = self.points[i] + self.speeds[i]
                if not SCREEN_DIM[0] > self.points[i].x > 0:
                    self.speeds[i].x *= -1
                if not SCREEN_DIM[1] > self.points[i].y > 0:
                    self.speeds[i].y *= -1


class Knot(Polyline):
    def get_knot(self, base, count):
        if len(base) < 3:
            return []
        self.points = []
        for i in range(-2, len(base) - 2):
            pnt = [(base[i] + base[i+1])*0.5, base[i + 1], ((base[i+1] + base[i+2])*0.5)]  # get 3 base points
            self.points.extend([self.__get_point(pnt, 1 / count * j) for j in range(count)])

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.__get_point(points, alpha, deg - 1) * (1 - alpha)

def draw_help():
    """function for drawing help screen"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["LMB", "Add point"])
    data.append(["RMB", "Delete point"])
    data.append(["<- ->", "Speed control"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

# create objects:
points_object = Polyline()
knot_object = Knot()

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True
    hue = 0
    color = pygame.Color(0)
    speed_change_degree=0.2

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points_object.points = []
                    points_object.speeds = []
                    knot_object.points = []
                if event.key == pygame.K_p:
                    pause = not pause
                    points_object.movement = not points_object.movement
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_LEFT:
                    points_object.speeds = [x*(1.0-speed_change_degree)  for x in points_object.speeds]
                if event.key == pygame.K_RIGHT:
                    points_object.speeds = [x*(1.0+speed_change_degree) for x in points_object.speeds]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    points_object.add_point(event.pos)
                else:
                    points_object.del_point(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        if not pause:
            points_object.set_points()
        points_object.draw()
        knot_object.draw(style='line', color=color)
        knot_object.get_knot(points_object.points, steps)
        if show_help:
            draw_help()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    exit(0)


