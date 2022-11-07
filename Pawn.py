import pygame as pg
import random
import time
from settings import *


class Pawn(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.has_moved = False
        self.color = color
        self.image = game.black_pawn if color == 1 else game.white_pawn
        self.image = pg.transform.scale(self.image, ((TILE, TILE)))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = pos
        self.rect.center = (self.x, self.y)

    def update(self):
        self.rect.center = (self.x, self.y)
        # pg.draw.rect(self.game.display, GREEN, pg.Rect(TILE * 0 + 25, TILE * 5 + 25, 50, 50))
        # pg.draw.rect(self.game.display, GREEN, pg.Rect(TILE * 0 + 50, TILE * 5 + 50, 50, 50))

    def valid_moves(self):
        moves = []
        if not self.has_moved:
            if self.color == 1:
                for i in range(2):
                    if self.game.board[self.pos[1] + (i + 1)][self.pos[0]] == "":
                        moves.append([self.pos[0], self.pos[1] + (i + 1)])
                    else:
                        break
            if self.color == 0:
                for i in range(2):
                    if self.game.board[self.pos[1] - (i+1)][self.pos[0]] == "":
                        moves.append([self.pos[0], self.pos[1] - (i+1)])
                    else:
                        break
        else:
            if self.color == 1:
                moves.append([self.pos[0], self.pos[1] + 1])
            if self.color == 0:
                moves.append([self.pos[0], self.pos[1] - 1])
        return moves

