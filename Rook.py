import pygame as pg
import random
import time
from settings import *


class Rook(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.black_rook if color == 1 else game.white_rook
        self.image = pg.transform.scale(self.image, ((100, 100)))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.pos = pos
        self.color = color
        # self.rect.center = (x,y)

    def update(self):
        self.rect.center = (self.x, self.y)

    def valid_moves(self):
        moves = []
        # print("Current: ", self.game.board[self.pos[1]][self.pos[0]])
        # print("Up: ", self.game.board[self.pos[1] - 1][self.pos[0]])
        # print("Down: ", self.game.board[self.pos[1] + 1][self.pos[0]])
        # print("Right: ", self.game.board[self.pos[1]][self.pos[0] + 1])
        # print("Left: ", self.game.board[self.pos[1]][self.pos[0] - 1])

        # Up directions
        i = 1
        while True:
            if (self.pos[1] - i >= 0) and (self.game.board[self.pos[1] - i][self.pos[0]] == ""):
                moves.append([self.pos[0], self.pos[1] - i])
                i += 1
            else:
                break

        # Down Direction
        j = 1
        while True:
            if (self.pos[1] + j <= 7) and (self.game.board[self.pos[1] + j][self.pos[0]] == ""):
                moves.append([self.pos[0], self.pos[1] + j])
                j += 1
            else:
                break

        # Left Direction
        k = 1
        while True:
            if (self.pos[0] - k >= 0) and (self.game.board[self.pos[1]][self.pos[0] - k] == ""):
                moves.append([self.pos[0] - k, self.pos[1]])
                k += 1
            else:
                break

        # # Right Direction
        m = 1
        while True:
            if (self.pos[0] + m <= 7) and (self.game.board[self.pos[1]][self.pos[0] + m] == ""):
                # print("Ads")
                moves.append([self.pos[0] + m, self.pos[1]])
                m += 1
            else:
                break

        return moves
