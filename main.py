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


class Game:

    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.moves = []

    def load_data(self):
        self.board = []
        a = []
        with open('board.txt', 'rt') as f:
            contents = f.read()
            for letter in contents:
                if letter == "\n":
                    self.board.append(a)
                    a = []
                else:
                    if letter == ".":
                        a.append("")
                    else:
                        a.append(letter)
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

        self.board.append(a)
        print(self.board)

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

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == "P":
                    color = 0
                    if i < 2:
                        color = 1
                    pawn = Pawn(self, TILE * j + 50, TILE * i + 50, color, [j,i])
                    self.pawn_sprites.add(pawn)

                if self.board[i][j] == "R":
                    color = 0
                    if i < 2:
                        color = 1
                    rook = Rook(self, TILE * j + 50, TILE * i + 50, color)
                    self.rook_sprites.add(rook)

                if self.board[i][j] == "B":
                    color = 0
                    if i < 2:
                        color = 1
                    bishop = Bishop(self, TILE * j + 50, TILE * i + 50, color)
                    self.rook_sprites.add(bishop)

                if self.board[i][j] == "H":
                    color = 0
                    if i < 2:
                        color = 1
                    knight = Knight(self, TILE * j + 50, TILE * i + 50, color)
                    self.rook_sprites.add(knight)

                if self.board[i][j] == "Q":
                    color = 0
                    if i < 2:
                        color = 1
                    queen = Queen(self, TILE * j + 50, TILE * i + 50, color)
                    self.rook_sprites.add(queen)

                if self.board[i][j] == "K":
                    color = 0
                    if i < 2:
                        color = 1
                    king = King(self, TILE * j + 50, TILE * i + 50, color)
                    self.rook_sprites.add(king)

        self.all_sprites.add(self.pawn_sprites)
        self.all_sprites.add(self.rook_sprites)
        self.all_sprites.add(self.bishop_sprites)
        self.all_sprites.add(self.knight_sprites)
        self.all_sprites.add(self.king_sprites)
        self.all_sprites.add(self.queen_sprites)

        self.run()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.running:
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                piece = [s for s in self.pawn_sprites if s.rect.collidepoint(pos)]
                self.moves = piece[0].valid_moves()
                print(self.moves)
                # p = Rook(self, TILE * 4 + 50, TILE * 4 + 50, 0)
                # self.rook_sprites.add(p)

                # self.display_moves(piece[0].valid_moves())


    def display_moves(self, moves):
        for move in moves:
            pg.draw.rect(self.display, GREEN, pg.Rect(TILE * move[0] + 25, TILE * move[1] + 25, 50, 50))

    def update(self):
        # for move in moves:
        #     pg.draw.rect(self.display, GREEN, pg.Rect(TILE * 0 + 25, TILE * 5 + 25, 50, 50))
        self.all_sprites.update()


    def draw(self):
        self.display.fill(BLACK)  # draw background

        # Cheate the chess board
        for j in range(BOARDLEN):
            for i in range(int(BOARDLEN / 2)):
                if j % 2 == 0:
                    pg.draw.rect(self.display, WHITE, (i * TILE * 2, j * TILE, 100, 100))
                else:
                    pg.draw.rect(self.display, WHITE, ((i * TILE * 2) + 100, j * TILE, 100, 100))

        for move in self.moves:
            pg.draw.rect(self.display, GREEN, pg.Rect(TILE * move[0] + 25, TILE * move[1] + 25, 50,50))
        self.all_sprites.draw(self.display)
        pg.display.update()


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.new()

pg.quit()
quit()
