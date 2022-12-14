import pygame as pg
import random
import time
from settings import *


class Rook(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos, symbol):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.symbol = symbol
        self.image = game.black_rook if color == 1 else game.white_rook
        self.image = pg.transform.scale(self.image, ((TILE, TILE)))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.pos = pos
        self.color = color
        # self.rect.center = (x,y)

    def update(self):
        pass

    def handle_movement(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x,self.y)

    def valid_moves(self, impossible=[], king_check=False, checkMoves=[], numChecks=0):
        moves = []
        kills = []
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

        if self.pos[1] - i >= 0:
            if self.color == 0:
                if "b" in self.game.board[self.pos[1] - i][self.pos[0]]:
                    kills.append([self.pos[0], self.pos[1] - i])
            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1] - i][self.pos[0]]) and (
                        self.game.board[self.pos[1] - i][self.pos[0]] != ""):
                    kills.append([self.pos[0], self.pos[1] - i])

        # Down Direction
        j = 1
        while True:
            if (self.pos[1] + j <= 7) and (self.game.board[self.pos[1] + j][self.pos[0]] == ""):
                moves.append([self.pos[0], self.pos[1] + j])
                j += 1
            else:
                break
        if self.pos[1] + j <= 7:
            if self.color == 0:
                if "b" in self.game.board[self.pos[1] + j][self.pos[0]]:
                    kills.append([self.pos[0], self.pos[1] + j])
            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1] + j][self.pos[0]]) and (
                        self.game.board[self.pos[1] + j][self.pos[0]] != ""):
                    kills.append([self.pos[0], self.pos[1] + j])

        # Left Direction
        k = 1
        while True:
            if (self.pos[0] - k >= 0) and (self.game.board[self.pos[1]][self.pos[0] - k] == ""):
                moves.append([self.pos[0] - k, self.pos[1]])
                k += 1
            else:
                break
        if self.pos[0] - k >= 0:
            if self.color == 0:
                if "b" in self.game.board[self.pos[1]][self.pos[0] - k]:
                    kills.append([self.pos[0] - k, self.pos[1]])
            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1]][self.pos[0] - k]) and (
                        self.game.board[self.pos[1]][self.pos[0] - k] != ""):
                    kills.append([self.pos[0] - k, self.pos[1]])
        # # Right Direction
        m = 1
        while True:
            if (self.pos[0] + m <= 7) and (self.game.board[self.pos[1]][self.pos[0] + m] == ""):
                # print("Ads")
                moves.append([self.pos[0] + m, self.pos[1]])
                m += 1
            else:
                break
        if self.pos[0] + m <= 7:
            if self.color == 0:
                if "b" in self.game.board[self.pos[1]][self.pos[0] + m]:
                    kills.append([self.pos[0] + m, self.pos[1]])
            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1]][self.pos[0] + m]) and (
                        self.game.board[self.pos[1]][self.pos[0] + m] != ""):
                    kills.append([self.pos[0] + m, self.pos[1]])

        if king_check and numChecks == 1:
            moves = [i for i in checkMoves if i in moves]
            kills = [i for i in checkMoves if i in kills]
        elif numChecks > 1:
            moves = []
            kills = []

        return {"moves": moves, "kills": kills}

    def all_position(self,  board, updated=[]):
        moves = []
        # Up directions
        i = 1
        while True:
            if self.pos[1] - i >= 0:
                move = board[self.pos[1] - i][self.pos[0]]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                moves.append([self.pos[0], self.pos[1] - i])
                i += 1
            else:
                break

        # Down Direction
        j = 1
        while True:
            if self.pos[1] + j <= 7:
                move = board[self.pos[1] + j][self.pos[0]]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                moves.append([self.pos[0], self.pos[1] + j])
                j += 1
            else:
                break
        # Left Direction
        k = 1
        while True:
            if self.pos[0] - k >= 0:
                move = board[self.pos[1]][self.pos[0] - k]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                moves.append([self.pos[0] - k, self.pos[1]])
                k += 1
            else:
                break
        # Right Direction
        m = 1
        while True:
            if self.pos[0] + m <= 7:
                move = board[self.pos[1]][self.pos[0] + m]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                # print("Ads")
                moves.append([self.pos[0] + m, self.pos[1]])
                m += 1
            else:
                break
        return moves