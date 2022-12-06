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
        self.turn = 0
        self.load_data()
        self.moves = []
        self.pos_kills = []
        self.rect_kills = []
        self.rect_moves = []
        self.current_piece = None

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
        self.pawn_sprites = pg.sprite.Group()
        self.rook_sprites = pg.sprite.Group()
        self.bishop_sprites = pg.sprite.Group()
        self.knight_sprites = pg.sprite.Group()
        self.queen_sprites = pg.sprite.Group()
        self.king_sprites = pg.sprite.Group()

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
                    self.pawn_sprites.add(pawn)
                if "R" in self.board[i][j]:
                    color = 0
                    symbol = "R"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bR"
                    rook = Rook(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    self.rook_sprites.add(rook)
                if "B" in self.board[i][j]:
                    color = 0
                    symbol = "B"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bB"
                    bishop = Bishop(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    self.bishop_sprites.add(bishop)
                if "H" in self.board[i][j]:
                    color = 0
                    symbol = "H"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bH"
                    knight = Knight(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    self.knight_sprites.add(knight)
                if "Q" in self.board[i][j]:
                    color = 0
                    symbol = "Q"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bQ"
                    queen = Queen(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    self.queen_sprites.add(queen)
                if "K" in self.board[i][j]:
                    color = 0
                    symbol = "K"
                    if "b" in self.board[i][j]:
                        color = 1
                        symbol = "bK"
                    king = King(self, TILE * j + (TILE * 0.5), TILE * i + (TILE * 0.5), color, [j, i], symbol)
                    self.king_sprites.add(king)

        self.all_sprites.add(self.pawn_sprites)
        self.all_sprites.add(self.rook_sprites)
        self.all_sprites.add(self.bishop_sprites)
        self.all_sprites.add(self.knight_sprites)
        self.all_sprites.add(self.king_sprites)
        self.all_sprites.add(self.queen_sprites)

        self.run()

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
                        all_moves = piece[0].valid_moves()
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
        self.all_sprites.draw(self.display)
        pg.display.update()


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.new()

pg.quit()
quit()
