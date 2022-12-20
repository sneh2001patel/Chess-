import pygame as pg
import random
import time
from settings import *


class Pawn(pg.sprite.Sprite):

    def __init__(self, game, x, y, color, pos, symbol):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.symbol = symbol  # how board array sees it
        self.has_moved = False
        self.color = color
        self.image = game.black_pawn if color == 1 else game.white_pawn
        self.image = pg.transform.scale(self.image, ((TILE, TILE))) # size of the piece and image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = pos
        self.rect.center = (self.x, self.y)
        self.score = 1

    def update(self):
        pass

    # ask prompt which piece you want to change the pawn with
    def choose_piece(self, ai=False):
        if not ai:
            s_out = "Pawn has reached the end of the board please pick which piece you want (Q, H, R, B): "
            while True:
                s = input(s_out)
                s = s.upper()
                if s == "Q" or s == "H" or s == "R" or s == "B":
                    return s
                else:
                    s_out = "Invalid Input please give a proper input (Q, H, R, B): "
        else:
            return random.choice(["Q", "H", "R", "B"])

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
        self.has_moved = True

    # Get valid moves for the pawn what can it take
    def valid_moves(self, impossible=[], king_check=False, checkMoves=[], numChecks=0):
        moves = []
        kills = []
        # Possible Moves
        if not self.has_moved:
            # White pawn move up the board (2 if pawn hasnt moved)
            if self.color == 0:
                for i in range(1, 3):
                    if (self.pos[1] - i >= 0) and (self.game.board[self.pos[1] - i][self.pos[0]] == ""):
                        if not self.kill_check([self.pos[0], self.pos[1] - i], checkMoves, numChecks):
                            moves.append([self.pos[0], self.pos[1] - i])
                        else:
                            break
                    else:
                        break
            # Black pawn move down the board (2 if pawn hasnt moved)
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
            # Move pawn 1 else wise
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
            # check diagonals
            if (self.pos[1] - 1 >= 0) and (self.pos[0] + 1 <= 7):
                if ("b" in self.game.board[self.pos[1] - 1][self.pos[0] + 1]):
                    if not self.kill_check([self.pos[0] + 1, self.pos[1] - 1], checkMoves, numChecks):
                        kills.append([self.pos[0] + 1, self.pos[1] - 1])
            if (self.pos[1] - 1 >= 0) and (self.pos[0] - 1 >= 0):
                if ("b" in self.game.board[self.pos[1] - 1][self.pos[0] - 1]):
                    if not self.kill_check([self.pos[0] - 1, self.pos[1] - 1], checkMoves, numChecks):
                        kills.append([self.pos[0] - 1, self.pos[1] - 1])
        # check diagonals
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

        # if the king is check only moves that can block the king's check are
        # going to be apart of the moves array/kills array
        if king_check and numChecks == 1:
            moves = [i for i in checkMoves if i in moves]
            kills = [i for i in checkMoves if i in kills]
        elif numChecks > 1: # cant block if the king is checked by 2 pieces
            moves = []
            kills = []

        return {"moves": moves, "kills": kills}

    def kill_check(self, move, check_spaces, num_checks):
        # Pawn cannot move if that move results in the king getting checked
        b = self.game.board
        new_board = [sublst[:] for sublst in b]
        # create a board with new move taken
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

        # check if thatnew position causes the king to get checked or not.
        k = self.game.get_king(a)
        return self.game.ischeck(k.pos, moves)

    def all_position(self, board, updated=[]):
        moves = []
        # get all possible kills it can take.
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
