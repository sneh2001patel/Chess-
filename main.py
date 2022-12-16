import pygame as pg
from settings import *
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King

import sys
import os
import random
import time


# hello my name is jenny
class Game:

    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.white_check = False
        self.black_check = False
        self.white_checkMate = False
        self.black_checkMate = False
        self.turn = 0
        self.pieces_moves = []
        self.load_data()
        self.moves = []
        self.white_moves = []
        self.black_moves = []
        self.pos_kills = []
        self.rect_kills = []
        self.rect_moves = []
        self.current_piece = None
        self.white_score = 0
        self.black_score = 0
        self.checkCol = MAGENTA
        self.num_checks = 0
        self.check_spaces = []
        self.test = []
        self.test1 = []

    def load_data(self):
        self.board = []
        with open('board.txt', 'rt') as f:
            contents = f.readlines()
            for line in contents:
                a = line.split()
                a = list(map(lambda x: x.replace('.', ''), a))
                self.board.append(a)

        self.black_king = pg.image.load(BKING).convert_alpha()
        self.white_king = pg.image.load(WKING).convert_alpha()

        self.black_queen = pg.image.load(BQUEEN).convert_alpha()
        self.white_queen = pg.image.load(WQUEEN).convert_alpha()

        self.black_rook = pg.image.load(BROOK).convert_alpha()
        self.white_rook = pg.image.load(WROOK).convert_alpha()

        self.black_bishop = pg.image.load(BBISHOP).convert_alpha()
        self.white_bishop = pg.image.load(WBISHOP).convert_alpha()

        self.black_knight = pg.image.load(BKNIGHT).convert_alpha()
        self.white_knight = pg.image.load(WKNIGHT).convert_alpha()

        self.black_pawn = pg.image.load(BPAWN).convert_alpha()
        self.white_pawn = pg.image.load(WPAWN).convert_alpha()

        # self.board.append(a)

    def run(self):
        self.clock.tick(FPS)
        while self.running:
            self.events()
            self.update()
            self.draw()

    def new(self):
        # Pawn = Green, Rook = Yellow, Bishop = Red, Knight = Cyan, Queen = MAGENTA, King = Blue
        self.all_sprites = pg.sprite.Group()
        # self.pawn_sprites = pg.sprite.Group()
        # self.rook_sprites = pg.sprite.Group()
        # self.bishop_sprites = pg.sprite.Group()
        # self.knight_sprites = pg.sprite.Group()
        # self.queen_sprites = pg.sprite.Group()
        self.king_sprites = pg.sprite.Group()
        self.white_sprites = pg.sprite.Group()
        self.black_sprites = pg.sprite.Group()

        self.display_board(self.board)

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if "P" in self.board[i][j]:
                    color = 0
                    symbol = "P"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bP"
                    pawn = Pawn(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    if color == 0:
                        self.white_sprites.add(pawn)
                    else:
                        self.black_sprites.add(pawn)
                if "R" in self.board[i][j]:
                    color = 0
                    symbol = "R"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bR"
                    rook = Rook(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    if color == 0:
                        self.white_sprites.add(rook)
                    else:
                        self.black_sprites.add(rook)
                if "B" in self.board[i][j]:
                    color = 0
                    symbol = "B"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bB"
                    bishop = Bishop(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    if color == 0:
                        self.white_sprites.add(bishop)
                    else:
                        self.black_sprites.add(bishop)
                if "H" in self.board[i][j]:
                    color = 0
                    symbol = "H"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bH"
                    knight = Knight(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    if color == 0:
                        self.white_sprites.add(knight)
                    else:
                        self.black_sprites.add(knight)
                if "Q" in self.board[i][j]:
                    color = 0
                    symbol = "Q"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bQ"
                    queen = Queen(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    if color == 0:
                        self.white_sprites.add(queen)
                    else:
                        self.black_sprites.add(queen)
                if "K" in self.board[i][j]:
                    color = 0
                    symbol = "K"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bK"
                    king = King(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    self.king_sprites.add(king)
                    if color == 0:
                        self.white_sprites.add(king)
                    else:
                        self.black_sprites.add(king)

        self.all_sprites.add(self.king_sprites)
        # self.all_sprites.add(self.queen_sprites)
        self.all_sprites.add(self.white_sprites)
        self.all_sprites.add(self.black_sprites)
        self.impossible = self.get_all_moves(self.opponent(self.turn))
        king = self.get_king(self.turn)
        self.do_check(king, self.impossible)

        print(self.black_check)
        print(self.white_check)
        self.run()

    def ischeck(self, element, list):
        if element in list:
            return True
        return False

    def do_check(self, king, impossible_list):
        kcol = self.white_check
        if self.ischeck(king.pos, impossible_list):
            if king.color == 0:
                self.white_check = True
            else:
                self.black_check = True
                kcol = self.black_check
            # king_check = self.white_check
            # if piece[0].color == 1:
            #     king_check = self.black_check

            moves = king.valid_moves(impossible_list, kcol, self.check_spaces, self.num_checks)
            all_moves = king.all_position(self.board)
            arr = [i for i in all_moves if i not in moves["moves"]]
            pos = king.pos
            # check_spaces = []
            self.num_checks = 0
            for i in arr:
                diff = (i[0] - pos[0], i[1] - pos[1])
                if diff == (-1, 0):
                    print("left")
                    dirr = self.direction(self.board, pos[1], pos[0], "left", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr
                if diff == (1, 0):
                    print("right")
                    dirr = self.direction(self.board, pos[1], pos[0], "right", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr
                if diff == (0, 1):
                    print("down")
                    dirr = self.direction(self.board, pos[1], pos[0], "down", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr
                if diff == (0, -1):
                    print("up")
                    dirr = self.direction(self.board, pos[1], pos[0], "up", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr
                if diff == (1, 1):
                    print("down-right")
                    dirr = self.direction(self.board, pos[1], pos[0], "down-right", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr
                if diff == (-1, -1):
                    print("up-left")
                    dirr = self.direction(self.board, pos[1], pos[0], "up-left", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr
                if diff == (-1, 1):
                    print("down-left")
                    dirr = self.direction(self.board, pos[1], pos[0], "down-left", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr
                if diff == (1, -1):
                    print("up-right")
                    dirr = self.direction(self.board, pos[1], pos[0], "up-right", king.color)
                    if dirr:
                        self.num_checks += 1
                    self.check_spaces += dirr

            print("Number of checks: ", self.num_checks)
            print("Check: ", self.check_spaces)
            canBlock = False
            if self.num_checks == 1:
                canBlock = self.block_exists(self.check_spaces)

            if not canBlock and len(moves["moves"]) == 0 and len(moves["kills"]) == 0:
                if king.color == 0:
                    print("Black Won!")
                    self.white_checkMate = True
                    self.checkCol = BLUE
                    # self.running = False
                else:
                    print("White Won!")
                    self.black_checkMate = True
                    self.checkCol = BLUE
                    # self.running = False
        # self.num_checks = 0
        # self.white_check = False
        # self.black_check = False
        print("White King Check: ", self.white_check)
        print("Black King Check: ", self.black_check)

    def block_exists(self, check_moves):
        pieces_moves = self.get_all_moves(self.turn, False)
        print(pieces_moves)
        print(check_moves)

        for i in check_moves:
            if i in pieces_moves:
                return True
        return False
        # print(self.turn)
        # print("ASF: ", self.pieces_moves)

    def direction(self, board, i, j, dir, color):
        if dir == "down":
            movs = []
            k = 1
            while True:
                if (i + k) <= 7:
                    if board[i + k][j] != "":
                        if color == 0 and "b" not in board[i + k][j]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i + k][j]:
                            movs = []
                            break
                        movs.append([j, i + k])
                        p = self.find_piece([j, i + k])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break
                    movs.append([j, i + k])
                else:
                    movs = []
                    break
                k += 1
            return movs
        elif dir == "up":
            movs = []
            k = 1
            while True:
                if (i - k) >= 0:
                    if board[i - k][j] != "":
                        if color == 0 and "b" not in board[i - k][j]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i - k][j]:
                            movs = []
                            break
                        movs.append([j, i - k])
                        p = self.find_piece([j, i - k])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break
                    movs.append([j, i - k])
                else:
                    movs = []
                    break
                k += 1
            return movs
        elif dir == "left":
            movs = []
            k = 1
            while True:
                if (j - k) >= 0:
                    if board[i][j - k] != "":
                        if color == 0 and "b" not in board[i][j - k]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i][j - k]:
                            movs = []
                            break
                        movs.append([j - k, i])
                        p = self.find_piece([j - k, i])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break
                    movs.append([j - k, i])
                else:
                    movs = []
                    break
                k += 1
            return movs
        elif dir == "right":
            movs = []
            k = 1
            while True:
                if (j + k) <= 7:
                    if board[i][j + k] != "":
                        if color == 0 and "b" not in board[i][j + k]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i][j + k]:
                            movs = []
                            break

                        movs.append([j + k, i])
                        p = self.find_piece([j + k, i])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break
                    movs.append([j + k, i])
                else:
                    movs = []
                    break
                k += 1
            return movs
        elif dir == "down-right":
            movs = []
            k = 1
            while True:
                if (j + k) <= 7 and (i + k) <= 7:
                    if board[i + k][j + k] != "":
                        if color == 0 and "b" not in board[i + k][j + k]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i + k][j + k]:
                            movs = []
                            break
                        movs.append([j + k, i + k])
                        p = self.find_piece([j + k, i + k])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break
                    movs.append([j + k, i + k])
                else:
                    movs = []
                    break
                k += 1
            return movs
        elif dir == "up-left":
            movs = []
            k = 1
            while True:
                if (j - k) >= 0 and (i - k) >= 0:
                    if board[i - k][j - k] != "":
                        if color == 0 and "b" not in board[i - k][j - k]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i - k][j - k]:
                            movs = []
                            break
                        movs.append([j - k, i - k])
                        p = self.find_piece([j - k, i - k])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break

                    movs.append([j - k, i - k])
                else:
                    movs = []
                    break
                k += 1
            return movs
        elif dir == "down-left":
            movs = []
            k = 1
            while True:
                if (j - k) >= 0 and (i + k) <= 7:
                    if board[i + k][j - k] != "":
                        if color == 0 and "b" not in board[i + k][j - k]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i + k][j - k]:
                            movs = []
                            break
                        movs.append([j - k, i + k])
                        p = self.find_piece([j - k, i + k])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break
                    movs.append([j - k, i + k])
                else:
                    movs = []
                    break
                k += 1
            return movs
        elif dir == "up-right":
            movs = []
            k = 1
            while True:
                if (j + k) <= 7 and (i - k) >= 0:
                    if board[i - k][j + k] != "":
                        if color == 0 and "b" not in board[i - k][j + k]:
                            movs = []
                            break
                        elif color == 1 and "b" in board[i - k][j + k]:
                            movs = []
                            break
                        movs.append([j + k, i - k])
                        p = self.find_piece([j + k, i - k])
                        arr = p.all_position(self.board)
                        a = p.pos
                        arr.append([a[0], a[1]])
                        if not self.isubset(arr, movs):
                            movs = []
                        break
                    movs.append([j + k, i - k])
                else:
                    movs = []
                    break
                k += 1
            return movs

    def isubset(self, arr1, arr2):
        for i in arr2:
            if i not in arr1:
                return False
        return True

    def piece_on_board(self, board, color):
        if color == 0:
            pieces = []
            for row in board:
                for spot in row:
                    if spot != "":
                        if "b" not in spot:
                            pieces.append(spot)
            return pieces
        else:
            pieces = []
            for row in board:
                for spot in row:
                    if spot != "":
                        if "b" in spot:
                            pieces.append(spot)
            return pieces

    def get_sprite(self, symbol, color):
        sprites = self.white_sprites
        if color == 1:
            sprites = self.black_sprites
        for sprite in sprites:
            if sprite.symbol == symbol:
                return sprite

    def find_piece(self, pos):
        for sprite in self.all_sprites:
            if sprite.pos == pos:
                return sprite

    def get_king(self, color):
        for king in self.king_sprites:
            if king.color is color:
                return king

    def get_all_moves(self, color, forK=True):
        moves = []
        sprites = self.white_sprites
        if color == 1:
            sprites = self.black_sprites

        for sprite in sprites:
            if forK:
                pos = sprite.all_position(self.board)
                moves += pos
            else:
                pos = sprite.valid_moves(self.impossible, sprite.color, self.check_spaces, self.num_checks)
                moves += pos["moves"]
                moves += pos["kills"]

        # print("ASdf", moves)
        return moves

    def opponent(self, turn):
        if turn == 0:
            return 1
        else:
            return 0

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.running:
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                piece = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
                if len(piece) > 0:
                    if piece[0].color == self.turn:

                        king_check = self.white_check
                        if piece[0].color == 1:
                            king_check = self.black_check

                        all_moves = piece[0].valid_moves(self.impossible, king_check, self.check_spaces,
                                                         self.num_checks)
                        self.current_piece = piece[0]
                        if self.moves != all_moves["moves"]:
                            self.moves = all_moves["moves"]
                            self.rect_moves = []
                            for move in self.moves:
                                self.rect_moves.append(
                                    pg.Rect(TILE * move[0] + TILE * 0.075, TILE * move[1] + TILE * 0.075, TILE * 0.85,
                                            TILE * 0.85))
                            print(self.moves)
                        else:
                            self.rect_moves = []
                            self.moves = []

                        if self.pos_kills != all_moves["kills"]:
                            self.pos_kills = all_moves["kills"]
                            self.rect_kills = []
                            for kill in self.pos_kills:
                                self.rect_kills.append(
                                    pg.Rect(TILE * kill[0] + TILE * 0.075, TILE * kill[1] + TILE * 0.075, TILE * 0.85,
                                            TILE * 0.85))
                            print(self.pos_kills)
                        else:
                            self.pos_kills = []
                            self.rect_kills = []

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()  # get the mouse pos
                # print(mouse_pos)
                for i in range(len(self.rect_moves)):
                    if self.rect_moves[i].collidepoint(mouse_pos):  # checking if the mouse_pos is inside the rectangle
                        j = self.moves[i][0]
                        k = self.moves[i][1]
                        self.current_piece.handle_movement(TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5))
                        self.turn = self.opponent(self.turn)
                        new_pos = [j, k]
                        self.update_board(self.current_piece.pos, new_pos, self.current_piece.symbol)
                        self.current_piece.pos = new_pos
                        if type(self.current_piece) == Pawn:
                            if self.current_piece.pos[1] == 0 and self.current_piece.color == 0:
                                p = self.current_piece.choose_piece()
                                piece = None
                                sym = p
                                if p == "Q":
                                    piece = Queen(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                  self.current_piece.color, new_pos, sym)
                                elif p == "H":
                                    piece = Knight(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "B":
                                    piece = Bishop(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "R":
                                    piece = Rook(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                 self.current_piece.color, new_pos, sym)

                                self.all_sprites.add(piece)
                                self.white_sprites.add(piece)
                                self.current_piece.kill()
                                self.board[k][j] = sym
                            if self.current_piece.pos[1] == 7 and self.current_piece.color == 1:
                                p = self.current_piece.choose_piece()
                                piece = None
                                sym = p
                                sym = "b" + sym
                                if p == "Q":
                                    piece = Queen(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                  self.current_piece.color, new_pos, sym)
                                elif p == "H":
                                    piece = Knight(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "B":
                                    piece = Bishop(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "R":
                                    piece = Rook(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                 self.current_piece.color, new_pos, sym)

                                self.all_sprites.add(piece)
                                self.black_sprites.add(piece)
                                self.current_piece.kill()
                                self.board[k][j] = sym

                        self.impossible = self.get_all_moves(self.opponent(self.turn))
                        king = self.get_king(self.turn)
                        self.do_check(king, self.impossible)
                        # print(self.opponent(self.turn), self.white_moves, self.black_moves)
                        self.moves = []
                        self.rect_moves = []
                        self.pos_kills = []
                        self.rect_kills = []
                        break

                for i in range(len(self.rect_kills)):
                    if self.rect_kills[i].collidepoint(mouse_pos):
                        # print(self.current_piece)
                        # print("Hello world")
                        pos = pg.mouse.get_pos()
                        piece = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
                        print(self.current_piece)
                        piece[0].kill()
                        j = self.pos_kills[i][0]
                        k = self.pos_kills[i][1]
                        self.current_piece.handle_movement(TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5))
                        self.turn = self.opponent(self.turn)
                        new_pos = [j, k]
                        self.update_board(self.current_piece.pos, new_pos, self.current_piece.symbol)
                        self.current_piece.pos = new_pos

                        if type(self.current_piece) == Pawn:
                            if self.current_piece.pos[1] == 0 and self.current_piece.color == 0:
                                p = self.current_piece.choose_piece()
                                piece = None
                                sym = p
                                if p == "Q":
                                    piece = Queen(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                  self.current_piece.color, new_pos, sym)
                                elif p == "H":
                                    piece = Knight(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "B":
                                    piece = Bishop(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "R":
                                    piece = Rook(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                 self.current_piece.color, new_pos, sym)

                                self.all_sprites.add(piece)
                                self.white_sprites.add(piece)
                                self.current_piece.kill()
                                self.board[k][j] = sym
                            if self.current_piece.pos[1] == 7 and self.current_piece.color == 1:
                                p = self.current_piece.choose_piece()
                                piece = None
                                sym = p
                                sym = "b" + sym
                                if p == "Q":
                                    piece = Queen(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                  self.current_piece.color, new_pos, sym)
                                elif p == "H":
                                    piece = Knight(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "B":
                                    piece = Bishop(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                   self.current_piece.color, new_pos, sym)
                                elif p == "R":
                                    piece = Rook(self, TILE * j + (TILE * 0.5), TILE * k + (TILE * 0.5),
                                                 self.current_piece.color, new_pos, sym)

                                self.all_sprites.add(piece)
                                self.black_sprites.add(piece)
                                self.current_piece.kill()
                                self.board[k][j] = sym

                        self.impossible = self.get_all_moves(self.opponent(self.turn))
                        king = self.get_king(self.turn)
                        self.do_check(king, self.impossible)

                        self.moves = []
                        self.rect_moves = []
                        self.pos_kills = []
                        self.rect_kills = []
                        break

    def update_board(self, current_pos, new_pos, symbol):
        self.board[current_pos[1]][current_pos[0]] = ""
        self.board[new_pos[1]][new_pos[0]] = symbol
        self.display_board(self.board)

    def display_board(self, board):
        print("-------------------")
        for i in board:
            print(i)
        print("-------------------")

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.display.fill(BLACK)  # draw background

        # Cheate the chess board
        for j in range(BOARDLEN):
            for i in range(int(BOARDLEN / 2)):
                if j % 2 == 0:
                    pg.draw.rect(self.display, WHITE, (i * TILE * 2, j * TILE, TILE, TILE))
                else:
                    pg.draw.rect(self.display, WHITE, ((i * TILE * 2) + TILE, j * TILE, TILE, TILE))

        for move in self.rect_moves:
            pg.draw.rect(self.display, GREEN, move)

        for kill in self.rect_kills:
            pg.draw.rect(self.display, RED, kill)

        if self.black_check:
            king = self.get_king(1)
            pg.draw.rect(self.display, self.checkCol, (
                TILE * king.pos[0] + TILE * 0.075, TILE * king.pos[1] + TILE * 0.075, TILE * 0.85, TILE * 0.85))

        if self.white_check:
            king = self.get_king(0)
            pg.draw.rect(self.display, self.checkCol, (
                TILE * king.pos[0] + TILE * 0.075, TILE * king.pos[1] + TILE * 0.075, TILE * 0.85, TILE * 0.85))

        for t in self.test:
            pg.draw.rect(self.display, self.checkCol, (
                TILE * t[0] + TILE * 0.075, TILE * t[1] + TILE * 0.075, TILE * 0.85, TILE * 0.85))
        for t in self.test1:
            pg.draw.rect(self.display, NAVY, (
                TILE * t[0] + TILE * 0.075, TILE * t[1] + TILE * 0.075, TILE * 0.85, TILE * 0.85))

        if self.current_piece != None and (self.moves or self.pos_kills):
            pg.draw.rect(self.display, YELLOW, (
                TILE * self.current_piece.pos[0] + TILE * 0.075, TILE * self.current_piece.pos[1] + TILE * 0.075,
                TILE * 0.85, TILE * 0.85))
        self.all_sprites.draw(self.display)
        pg.display.update()


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.new()

# time.sleep(3)
pg.quit()
quit()
