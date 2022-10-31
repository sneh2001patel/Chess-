import pygame as pg
import random
import time
from settings import *


class Rook(pg.sprite.Sprite):

    def __init__(self, game, x, y, color):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.black_rook if color == 1 else game.white_rook
        self.image = pg.transform.scale(self.image, ((100, 100)))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        # self.rect.center = (x,y)

    def update(self):
        self.rect.center = (self.x, self.y)
