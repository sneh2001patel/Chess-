import pygame as pg
import random
import time
from settings import *


class King(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.black_king if color == 1 else game.white_king
        self.image = pg.transform.scale(self.image, ((100,100)))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.pos = pos
        self.color = color
        # self.rect.center = (x,y)

    def update(self):
        self.rect.center = (self.x, self.y)
