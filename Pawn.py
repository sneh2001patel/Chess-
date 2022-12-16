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
        self.score = 1

    def update(self):
        pass

    def choose_piece(self):
        s_out = "Pawn has reached the end of the board please pick which piece you want (Q, H, R, B): "
        while True:
            s = input(s_out)
            s = s.upper()
            if s == "Q" or s == "H" or s == "R" or s == "B":
                return s
            else:
                s_out = "Invalid Input please give a proper input (Q, H, R, B): "

    def handle_movement(self, x, y):
        self.x = x
        self.y = y
        if self.color == 0:
            self.game.white_check = False
        else:
            self.game.black_check = False
        self.rect.center = (self.x, self.y)
        self.has_moved = True

    def valid_moves(self, impossible=[], king_check=False, checkMoves=[], numChecks=0):
        moves = []
        kills = []
        # Possible Moves
        if not self.has_moved:
            if self.color == 0:
                for i in range(1, 3):
                    if (self.pos[1] - i >= 0) and (self.game.board[self.pos[1] - i][self.pos[0]] == ""):
                        if not self.kill_check([self.pos[0], self.pos[1] - i], checkMoves, numChecks):
                            moves.append([self.pos[0], self.pos[1] - i])
                        else:
                            break
                    else:
                        break
            if self.color == 1:
                for i in range(1, 3):
                    if (self.pos[1] + i <= 7) and (self.game.board[self.pos[1] + i][self.pos[0]] == ""):
                        if not self.kill_check([self.pos[0], self.pos[1] + i], checkMoves, numChecks):
                            moves.append([self.pos[0], self.pos[1] + i])
                        else:
                            break
                    else:
                        break

        else:
            if self.color == 0:
                if (self.pos[1] - 1 >= 0) and (self.game.board[self.pos[1] - 1][self.pos[0]] == ""):
                    if not self.kill_check([self.pos[0], self.pos[1] - 1], checkMoves, numChecks):
                        moves.append([self.pos[0], self.pos[1] - 1])
            if self.color == 1:
                if (self.pos[1] + 1 <= 7) and (self.game.board[self.pos[1] + 1][self.pos[0]] == ""):
                    if not self.kill_check([self.pos[0], self.pos[1] + 1], checkMoves, numChecks):
                        moves.append([self.pos[0], self.pos[1] + 1])

        # Kills
        if self.color == 0:  # white
            if (self.pos[1] - 1 >= 0) and (self.pos[0] + 1 <= 7):
                if ("b" in self.game.board[self.pos[1] - 1][self.pos[0] + 1]):
                    if not self.kill_check([self.pos[0] + 1, self.pos[1] - 1], checkMoves, numChecks):
                        kills.append([self.pos[0] + 1, self.pos[1] - 1])
            if (self.pos[1] - 1 >= 0) and (self.pos[0] - 1 >= 0):
                if ("b" in self.game.board[self.pos[1] - 1][self.pos[0] - 1]):
                    if not self.kill_check([self.pos[0] - 1, self.pos[1] - 1], checkMoves, numChecks):
                        kills.append([self.pos[0] - 1, self.pos[1] - 1])

        if self.color == 1:  # black
            if (self.pos[1] + 1 <= 7) and (self.pos[0] - 1 >= 0):
                if ("b" not in self.game.board[self.pos[1] + 1][self.pos[0] - 1]) and (
                        self.game.board[self.pos[1] + 1][self.pos[0] - 1] != ""):
                    if not self.kill_check([self.pos[0] - 1, self.pos[1] + 1], checkMoves, numChecks):
                        kills.append([self.pos[0] - 1, self.pos[1] + 1])

            if (self.pos[1] + 1 <= 7) and (self.pos[0] + 1 <= 7):
                if ("b" not in self.game.board[self.pos[1] + 1][self.pos[0] + 1]) and (
                        self.game.board[self.pos[1] + 1][self.pos[0] + 1] != ""):
                    if not self.kill_check([self.pos[0] + 1, self.pos[1] + 1], checkMoves, numChecks):
                        kills.append([self.pos[0] + 1, self.pos[1] + 1])

        if king_check and numChecks == 1:
            moves = [i for i in checkMoves if i in moves]
            kills = [i for i in checkMoves if i in kills]
        elif numChecks > 1:
            moves = []
            kills = []

        return {"moves": moves, "kills": kills}

    def kill_check(self, move, check_spaces, num_checks):
        b = self.game.board
        new_board = [sublst[:] for sublst in b]
        new_board[self.pos[1]][self.pos[0]] = ""
        new_board[move[1]][move[0]] = self.symbol
        print("NEW BORAD")
        self.game.display_board(new_board)
        a = self.game.turn
        inverse = self.game.opponent(a)

        sprites = self.game.white_sprites
        if inverse == 1:
            sprites = self.game.black_sprites

        moves = []
        for sprite in sprites:
            pos = sprite.all_position(new_board)
            moves += pos

        k = self.game.get_king(a)
        return self.game.ischeck(k.pos, moves)

    def all_position(self, board, updated=[]):
        moves = []

        if self.color == 0:
            if (self.pos[1] - 1 >= 0) and (self.pos[0] + 1 <= 7):
                moves.append([self.pos[0] + 1, self.pos[1] - 1])
            if (self.pos[1] - 1 >= 0) and (self.pos[0] - 1 >= 0):
                moves.append([self.pos[0] - 1, self.pos[1] - 1])
        if self.color == 1:
            if (self.pos[1] + 1 <= 7) and (self.pos[0] - 1 >= 0):
                moves.append([self.pos[0] - 1, self.pos[1] + 1])
            if (self.pos[1] + 1 <= 7) and (self.pos[0] + 1 <= 7):
                moves.append([self.pos[0] + 1, self.pos[1] + 1])
        return moves
