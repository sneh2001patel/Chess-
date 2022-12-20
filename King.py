import pygame as pg
import random
import time

import Queen
from settings import *


class King(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos, symbol):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.symbol = symbol  # how board array sees it
        self.image = game.black_king if color == 1 else game.white_king
        self.image = pg.transform.scale(self.image, ((TILE, TILE)))  # size of the piece and image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.pos = pos
        self.color = color
        self.check = False

    def update(self):
        pass
        # self.rect.center = (self.x, self.y)

    # move the piece by changing x,y positions
    def handle_movement(self, x, y):
        self.x = x
        self.y = y
        # If the king is in check then the only move it can take will result in the king getting out of a check
        if self.color == 0:
            self.game.white_check = False
        else:
            self.game.black_check = False
        self.rect.center = (self.x, self.y)

    # Get valid moves for the pawn what can it take
    def valid_moves(self, impossible=[], king_check=False, checkMoves=[], numChecks=0):
        moves = []
        kills = []
        # Get moves in all 8 moves for the king
        if (self.pos[1] - 1 >= 0) and (self.pos[0] + 1 <= 7):
            if self.game.board[self.pos[1] - 1][self.pos[0] + 1] == "":
                moves.append([self.pos[0] + 1, self.pos[1] - 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] - 1][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] - 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] - 1][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] - 1])

        if (self.pos[1] - 1 >= 0) and (self.pos[0] - 1 >= 0):
            if self.game.board[self.pos[1] - 1][self.pos[0] - 1] == "":
                moves.append([self.pos[0] - 1, self.pos[1] - 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] - 1][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] - 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] - 1][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] - 1])

        if (self.pos[1] + 1 <= 7) and (self.pos[0] + 1 <= 7):
            if self.game.board[self.pos[1] + 1][self.pos[0] + 1] == "":
                moves.append([self.pos[0] + 1, self.pos[1] + 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] + 1][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] + 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] + 1][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1] + 1])

        if (self.pos[1] + 1 <= 7) and (self.pos[0] - 1 >= 0):
            if self.game.board[self.pos[1] + 1][self.pos[0] - 1] == "":
                moves.append([self.pos[0] - 1, self.pos[1] + 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] + 1][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] + 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] + 1][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1] + 1])

        if self.pos[1] - 1 >= 0:
            if self.game.board[self.pos[1] - 1][self.pos[0]] == "":
                moves.append([self.pos[0], self.pos[1] - 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] - 1][self.pos[0]]:
                        kills.append([self.pos[0], self.pos[1] - 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] - 1][self.pos[0]]:
                        kills.append([self.pos[0], self.pos[1] - 1])

        if self.pos[1] + 1 <= 7:
            if self.game.board[self.pos[1] + 1][self.pos[0]] == "":
                moves.append([self.pos[0], self.pos[1] + 1])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1] + 1][self.pos[0]]:
                        kills.append([self.pos[0], self.pos[1] + 1])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1] + 1][self.pos[0]]:
                        kills.append([self.pos[0], self.pos[1] + 1])

        if self.pos[0] - 1 >= 0:
            if self.game.board[self.pos[1]][self.pos[0] - 1] == "":
                moves.append([self.pos[0] - 1, self.pos[1]])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1]][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1]])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1]][self.pos[0] - 1]:
                        kills.append([self.pos[0] - 1, self.pos[1]])

        if self.pos[0] + 1 <= 7:
            if (self.game.board[self.pos[1]][self.pos[0] + 1] == ""):
                moves.append([self.pos[0] + 1, self.pos[1]])
            else:
                if self.color == 0:
                    if "b" in self.game.board[self.pos[1]][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1]])
                if self.color == 1:
                    if "b" not in self.game.board[self.pos[1]][self.pos[0] + 1]:
                        kills.append([self.pos[0] + 1, self.pos[1]])

        # Filter the moves and kills get all moves from each piece and then
        # check if the moves or kills are that if they are then remove them
        moves = [i for i in moves if i not in impossible]  # it cannot move to a spot that will result in a check
        kills = self.kill_check(kills, checkMoves, numChecks)
        return {"moves": moves, "kills": kills}

    # Check that possible kill does not result in a check
    def kill_check(self, kills, check_spaces, num_checks):
        b = self.game.board
        aproved_kills = []
        for kill in kills:
            # create a new board and move the piece there
            new_board = [sublst[:] for sublst in b]
            new_board[self.pos[1]][self.pos[0]] = ""
            new_board[kill[1]][kill[0]] = self.symbol
            # self.game.display_board(self.game.board)
            # self.game.display_board(new_board)
            a = self.game.turn
            inverse = self.game.opponent(a)

            sprites = self.game.white_sprites
            if inverse == 1:
                sprites = self.game.black_sprites
            moves = []
            for sprite in sprites:
                pos = sprite.all_position(new_board)
                moves += pos

            # after moving check whether or not that piece was is part of the enemy's movements
            if not self.game.ischeck(kill, moves):
                aproved_kills.append(kill)

        return aproved_kills

    def all_position(self, board, updated=[]):
        moves = []
        new_pos = self.pos
        if updated:
            new_pos = updated
        # get all 8 positions
        if (new_pos[1] - 1 >= 0) and (new_pos[0] + 1 <= 7):
            moves.append([new_pos[0] + 1, new_pos[1] - 1])
        if (new_pos[1] - 1 >= 0) and (new_pos[0] - 1 >= 0):
            moves.append([new_pos[0] - 1, new_pos[1] - 1])
        if (new_pos[1] + 1 <= 7) and (new_pos[0] + 1 <= 7):
            moves.append([new_pos[0] + 1, new_pos[1] + 1])
        if (new_pos[1] + 1 <= 7) and (new_pos[0] - 1 >= 0):
            moves.append([new_pos[0] - 1, new_pos[1] + 1])
        if new_pos[1] - 1 >= 0:
            moves.append([new_pos[0], new_pos[1] - 1])
        if new_pos[1] + 1 <= 7:
            moves.append([new_pos[0], new_pos[1] + 1])
        if new_pos[0] - 1 >= 0:
            moves.append([new_pos[0] - 1, new_pos[1]])
        if new_pos[0] + 1 <= 7:
            moves.append([new_pos[0] + 1, new_pos[1]])
        return moves
