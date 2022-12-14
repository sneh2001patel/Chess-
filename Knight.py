import pygame as pg
import random
import time
from settings import *


class Knight(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos, symbol):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.symbol = symbol
        self.image = game.black_knight if color == 1 else game.white_knight
        self.image = pg.transform.scale(self.image, ((TILE, TILE)))
        # self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.pos = pos
        self.color = color
        # self.rect.center = (x,y)

    def update(self):
        pass
        # self.rect.center = (self.x, self.y)

    def handle_movement(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)

    def valid_moves(self, impossible=[], king_check=False, checkMoves=[], numChecks=0):
        moves = []
        kills = []
        # print("Current: ", self.game.board[self.pos[1]][self.pos[0]])
        # print("Up: ", self.game.board[self.pos[1] - 1][self.pos[0]])
        # print("Down: ", self.game.board[self.pos[1] + 1][self.pos[0]])
        # print("Right: ", self.game.board[self.pos[1]][self.pos[0] + 1])
        # print("Left: ", self.game.board[self.pos[1]][self.pos[0] - 1])

        if (self.pos[1] - 1 >= 0) and (self.pos[0] + 2 <= 7):
            if self.game.board[self.pos[1] - 1][self.pos[0] + 2] == "":
                moves.append([self.pos[0] + 2, self.pos[1] - 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] - 1][self.pos[0] + 2]:
                        kills.append([self.pos[0] + 2, self.pos[1] - 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] - 1][self.pos[0] + 2]:
                        kills.append([self.pos[0] + 2, self.pos[1] - 1])

        if (self.pos[1] - 2 >= 0) and (self.pos[0] + 1 <= 7):
            if self.game.board[self.pos[1] - 2][self.pos[0] + 1] == "":
                moves.append([self.pos[0] + 1, self.pos[1] - 2])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] - 2][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] - 2])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] - 2][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] - 2])

        if (self.pos[1] - 2 >= 0) and (self.pos[0] - 1 >= 0):
            if self.game.board[self.pos[1] - 2][self.pos[0] - 1] == "":
                moves.append([self.pos[0] - 1, self.pos[1] - 2])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] - 2][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] - 2])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] - 2][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] - 2])

        if (self.pos[1] + 2 <= 7) and (self.pos[0] - 1 >= 0):
            if self.game.board[self.pos[1] + 2][self.pos[0] - 1] == "":
                moves.append([self.pos[0] - 1, self.pos[1] + 2])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] + 2][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] + 2])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] + 2][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] + 2])

        if (self.pos[1] + 1 <= 7) and (self.pos[0] - 2 >= 0):
            if self.game.board[self.pos[1] + 1][self.pos[0] - 2] == "":
                moves.append([self.pos[0] - 2, self.pos[1] + 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] + 1][self.pos[0] - 2]:
                        kills.append([self.pos[0] - 2, self.pos[1] + 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] + 1][self.pos[0] - 2]:
                        kills.append([self.pos[0] - 2, self.pos[1] + 1])

        if (self.pos[1] - 1 >= 0) and (self.pos[0] - 2 >= 0):
            if self.game.board[self.pos[1] - 1][self.pos[0] - 2] == "":
                moves.append([self.pos[0] - 2, self.pos[1] - 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] - 1][self.pos[0] - 2]:
                        kills.append([self.pos[0] - 2, self.pos[1] - 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] - 1][self.pos[0] - 2]:
                        kills.append([self.pos[0] - 2, self.pos[1] - 1])

        if (self.pos[1] + 1 <= 7) and (self.pos[0] + 2 <= 7):
            if self.game.board[self.pos[1] + 1][self.pos[0] + 2] == "":
                moves.append([self.pos[0] + 2, self.pos[1] + 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] + 1][self.pos[0] + 2]:
                        kills.append([self.pos[0] + 2, self.pos[1] + 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] + 1][self.pos[0] + 2]:
                        kills.append([self.pos[0] + 2, self.pos[1] + 1])

        if (self.pos[1] + 2 <= 7) and (self.pos[0] + 1 <= 7):
            if self.game.board[self.pos[1] + 2][self.pos[0] + 1] == "":
                moves.append([self.pos[0] + 1, self.pos[1] + 2])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] + 2][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] + 2])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] + 2][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] + 2])

        if king_check and numChecks == 1:
            moves = [i for i in checkMoves if i in moves]
            kills = [i for i in checkMoves if i in kills]
        elif numChecks > 1:
            moves = []
            kills = []

        return {"moves": moves, "kills": kills}

    def all_position(self,  board, updated=[]):
        moves = []

        if (self.pos[1] - 1 >= 0) and (self.pos[0] + 2 <= 7):
            moves.append([self.pos[0] + 2, self.pos[1] - 1])

        if (self.pos[1] - 2 >= 0) and (self.pos[0] + 1 <= 7):
            moves.append([self.pos[0] + 1, self.pos[1] - 2])

        if (self.pos[1] - 2 >= 0) and (self.pos[0] - 1 >= 0):
            moves.append([self.pos[0] - 1, self.pos[1] - 2])

        if (self.pos[1] + 2 <= 7) and (self.pos[0] - 1 >= 0):
            moves.append([self.pos[0] - 1, self.pos[1] + 2])

        if (self.pos[1] + 1 <= 7) and (self.pos[0] - 2 >= 0):
            moves.append([self.pos[0] - 2, self.pos[1] + 1])

        if (self.pos[1] - 1 >= 0) and (self.pos[0] - 2 >= 0):
            moves.append([self.pos[0] - 2, self.pos[1] - 1])

        if (self.pos[1] + 1 <= 7) and (self.pos[0] + 2 <= 7):
            moves.append([self.pos[0] + 2, self.pos[1] + 1])

        if (self.pos[1] + 2 <= 7) and (self.pos[0] + 1 <= 7):
            moves.append([self.pos[0] + 1, self.pos[1] + 2])

        return moves