import pygame as pg
import random
import time
from settings import *


class Pawn(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos, symbol):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.symbol = symbol
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
        pass



    def handle_movement(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.has_moved = True


    def valid_moves(self):
        moves = []
        kills = []
        # Possible Moves
        if not self.has_moved:
            if self.color == 0:
                for i in range(1, 3):
                    if (self.pos[1] - i >= 0) and (self.game.board[self.pos[1] - i][self.pos[0]] == ""):
                        moves.append([self.pos[0], self.pos[1] - i])
                    else:
                        break
            if self.color == 1:
                for i in range(1, 3):
                    if (self.pos[1] + i <= 7) and (self.game.board[self.pos[1] + i][self.pos[0]] == ""):
                        moves.append([self.pos[0], self.pos[1] + i])
                    else:
                        break

        else:
            if self.color == 0:
                if (self.pos[1] - 1 >= 0) and (self.game.board[self.pos[1] - 1][self.pos[0]] == ""):
                    moves.append([self.pos[0], self.pos[1] - 1])
            if self.color == 1:
                if (self.pos[1] + 1 <= 7) and (self.game.board[self.pos[1] + 1][self.pos[0]] == ""):
                    moves.append([self.pos[0], self.pos[1] + 1])

        # Kills
        if self.color == 0:  # white
            if ("b" in self.game.board[self.pos[1] - 1][self.pos[0] + 1]) and (self.pos[1] - 1 >= 0) and (
                    self.pos[0] + 1 <= 7):
                kills.append([self.pos[0] + 1, self.pos[1] - 1])

            if ("b" in self.game.board[self.pos[1] - 1][self.pos[0] - 1]) and (self.pos[1] - 1 >= 0) and (
                    self.pos[0] - 1 >= 0):
                kills.append([self.pos[0] - 1, self.pos[1] - 1])
        if self.color == 1:  # black
            if (self.pos[1] + 1 <= 7) and (self.pos[0] - 1 >= 0):
                if ("b" not in self.game.board[self.pos[1] + 1][self.pos[0] - 1]) and (
                        self.game.board[self.pos[1] + 1][self.pos[0] - 1] != ""):
                    kills.append([self.pos[0] - 1, self.pos[1] + 1])

            if (self.pos[1] + 1 <= 7) and (self.pos[0] + 1 <= 7):
                if ("b" not in self.game.board[self.pos[1] + 1][self.pos[0] + 1]) and (
                        self.game.board[self.pos[1] + 1][self.pos[0] + 1] != ""):
                    kills.append([self.pos[0] + 1, self.pos[1] + 1])



        return {"moves": moves, "kills": kills}
