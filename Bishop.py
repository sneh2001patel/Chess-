import pygame as pg
import random
import time
from settings import *


class Bishop(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos, symbol):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.symbol = symbol
        self.image = game.black_bishop if color == 1 else game.white_bishop
        self.image = pg.transform.scale(self.image, ((TILE, TILE)))  # size of the piece and image
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.pos = pos
        self.color = color
        self.score = 3
        # self.rect.center = (x,y)

    def update(self):
        pass
        # self.rect.center = (self.x, self.y)

    # move the piece by changing x,y positions
    def handle_movement(self, x, y):
        self.x = x
        self.y = y
        # If the king is in check no piece will be able to move only time a piece can move is when it
        # block the king's check therefore that check will become false
        if self.color == 0:
            self.game.white_check = False
        else:
            self.game.black_check = False
        self.rect.center = (self.x, self.y)

    def valid_moves(self, impossible=[], king_check=False, checkMoves=[], numChecks=0):
        moves = []
        kills = []

        # Up-right directions
        i = 1
        while True:
            if (self.pos[1] - i >= 0) and (self.pos[0] + i <= 7) and (
                    self.game.board[self.pos[1] - i][self.pos[0] + i] == ""):
                if not self.move_check([self.pos[0] + i, self.pos[1] - i], checkMoves, numChecks):
                    moves.append([self.pos[0] + i, self.pos[1] - i])
                else:
                    break
                i += 1
            else:
                break

        if (self.pos[1] - i >= 0) and (self.pos[0] + i <= 7):
            if self.color == 0:
                if "b" in self.game.board[self.pos[1] - i][self.pos[0] + i]:
                    kills.append([self.pos[0] + i, self.pos[1] - i])

            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1] - i][self.pos[0] + i]) and (
                        self.game.board[self.pos[1] - i][self.pos[0] + i] != ""):
                    kills.append([self.pos[0] + i, self.pos[1] - i])

        # Up-Left directions
        j = 1
        while True:
            if (self.pos[1] - j >= 0) and (self.pos[0] - j >= 0) and (
                    self.game.board[self.pos[1] - j][self.pos[0] - j] == ""):
                if not self.move_check([self.pos[0] - j, self.pos[1] - j], checkMoves, numChecks):
                    moves.append([self.pos[0] - j, self.pos[1] - j])
                else:
                    break
                j += 1
            else:
                break
        if (self.pos[1] - j >= 0) and (self.pos[0] - j >= 0):
            if self.color == 0:
                if "b" in self.game.board[self.pos[1] - j][self.pos[0] - j]:
                    kills.append([self.pos[0] - j, self.pos[1] - j])

            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1] - j][self.pos[0] - j]) and (
                        self.game.board[self.pos[1] - j][self.pos[0] - j] != ""):
                    kills.append([self.pos[0] - j, self.pos[1] - j])
        # down-right directions
        k = 1
        while True:
            if (self.pos[1] + k <= 7) and (self.pos[0] + k <= 7) and (
                    self.game.board[self.pos[1] + k][self.pos[0] + k] == ""):
                if not self.move_check([self.pos[0] + k, self.pos[1] + k], checkMoves, numChecks):
                    moves.append([self.pos[0] + k, self.pos[1] + k])
                else:
                    break
                k += 1
            else:
                break

        if (self.pos[1] + k <= 7) and (self.pos[0] + k <= 7):
            if self.color == 0:
                if "b" in self.game.board[self.pos[1] + k][self.pos[0] + k]:
                    kills.append([self.pos[0] + k, self.pos[1] + k])
            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1] + k][self.pos[0] + k]) and (
                        self.game.board[self.pos[1] + k][self.pos[0] + k] != ""):
                    kills.append([self.pos[0] + k, self.pos[1] + k])

        # down-right directions
        m = 1
        while True:
            if (self.pos[1] + m <= 7) and (self.pos[0] - m >= 0) and (
                    self.game.board[self.pos[1] + m][self.pos[0] - m] == ""):
                if not self.move_check([self.pos[0] - m, self.pos[1] + m], checkMoves, numChecks):
                    moves.append([self.pos[0] - m, self.pos[1] + m])
                else:
                    break
                m += 1
            else:
                break
        if (self.pos[1] + m <= 7) and (self.pos[0] - m >= 0):
            if self.color == 0:
                if "b" in self.game.board[self.pos[1] + m][self.pos[0] - m]:
                    kills.append([self.pos[0] - m, self.pos[1] + m])
            if self.color == 1:
                if ("b" not in self.game.board[self.pos[1] + m][self.pos[0] - m]) and (
                        self.game.board[self.pos[1] + m][self.pos[0] - m] != ""):
                    kills.append([self.pos[0] - m, self.pos[1] + m])

        # if the king is check only moves that can block the king's check are
        # going to be apart of the moves array/kills array
        if king_check and numChecks == 1:
            moves = [i for i in checkMoves if i in moves]
            kills = [i for i in checkMoves if i in kills]
        elif numChecks > 1: # cant block if the king is checked by 2 pieces
            moves = []
            kills = []
        # filter the kills by checking if moving to the kill position results in check
        kills = self.kill_check(kills, checkMoves, numChecks)
        return {"moves": moves, "kills": kills}

    def kill_check(self, kills, check_spaces, num_checks):
        b = self.game.board
        aproved_kills = []
        # go thru the kills
        for kill in kills:
            # create a new board and update with the new kill positions
            new_board = [sublst[:] for sublst in b]
            new_board[self.pos[1]][self.pos[0]] = ""
            new_board[kill[1]][kill[0]] = self.symbol
            t = self.game.turn
            inverse = self.game.opponent(t)

            moves = []
            symbols = self.game.piece_on_board(new_board, inverse)
            sprites = []
            for i in symbols:
                sym_sprite = self.game.get_sprite(i, inverse)
                sprites.append(sym_sprite)

            for sprite in sprites:
                pos = sprite.all_position(new_board)
                moves += pos

            # check if enemy moves are where king is
            k = self.game.get_king(t)
            if not self.game.ischeck(k.pos, moves):
                aproved_kills.append(kill)
        return aproved_kills

    # check if move does not result in check
    def move_check(self, move, check_spaces, num_checks):

        # create a new board with move update
        b = self.game.board
        new_board = [sublst[:] for sublst in b]
        new_board[self.pos[1]][self.pos[0]] = ""
        new_board[move[1]][move[0]] = self.symbol
        a = self.game.turn
        inverse = self.game.opponent(a)

        sprites = self.game.white_sprites
        if inverse == 1:
            sprites = self.game.black_sprites

        moves = []
        for sprite in sprites:
            pos = sprite.all_position(new_board)
            moves += pos

        # check if enemy moves is not where king is
        k = self.game.get_king(a)
        return self.game.ischeck(k.pos, moves)

    def all_position(self, board, updated=[]):
        # get all moves for each direction no matter what
        moves = []
        i = 1
        while True:
            if (self.pos[1] - i >= 0) and (self.pos[0] + i <= 7):
                move = board[self.pos[1] - i][self.pos[0] + i]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                moves.append([self.pos[0] + i, self.pos[1] - i])
                i += 1
            else:
                break

        # Up-Left directions
        j = 1
        while True:
            if (self.pos[1] - j >= 0) and (self.pos[0] - j >= 0):
                move = board[self.pos[1] - j][self.pos[0] - j]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                moves.append([self.pos[0] - j, self.pos[1] - j])
                j += 1
            else:
                break
        # down-right directions
        k = 1
        while True:
            if (self.pos[1] + k <= 7) and (self.pos[0] + k <= 7):
                move = board[self.pos[1] + k][self.pos[0] + k]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                moves.append([self.pos[0] + k, self.pos[1] + k])
                k += 1
            else:
                break

        # down-right directions
        m = 1
        while True:
            if (self.pos[1] + m <= 7) and (self.pos[0] - m >= 0):
                move = board[self.pos[1] + m][self.pos[0] - m]
                if self.color == 0:
                    if move != "" and move != "bK":
                        break
                else:
                    if move != "K" and move != "":
                        break
                moves.append([self.pos[0] - m, self.pos[1] + m])
                m += 1
            else:
                break

        return moves
