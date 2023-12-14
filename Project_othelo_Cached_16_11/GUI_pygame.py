import board_file
import pawn_file
import utils
import Player_file
import GUI
import engine_file
import pygame as p
import numpy as np

Game_board = board_file.Board()
Game_board.init_table()
gui = GUI.Gui()
ENGINE = engine_file.engine()

WIDTH = 512
HEIGHT = 512
CELL_WIDTH = 64
CELL_HEIGHT = 64

BOARD_CELL_X = board_file.WIDTH
BOARD_CELL_Y = board_file.LENGTH

IMAGE_DICT = {}
COULEUR_DICT = {'O' : 'white', 'X' : 'black'}
def init(screen):
    #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    for i in range(8):
        for j in range(8):
            p.draw.rect(screen, (p.Color('white') if (i+j)%2 == 0 else p.Color('dark grey'))
                                 , (j*CELL_WIDTH, i*CELL_WIDTH, CELL_HEIGHT, CELL_HEIGHT), 0)
            p.display.flip()


def draw_pawns(screen, board):
    for x, row in enumerate(board):
        for y, elem in enumerate(row):
            if elem != board_file.NULL_VALUE:
                pos = (x*CELL_WIDTH + CELL_WIDTH/2, y*CELL_HEIGHT + CELL_HEIGHT/2)
                pos = (y*CELL_HEIGHT + CELL_HEIGHT/2, x*CELL_WIDTH + CELL_WIDTH/2)
                p.draw.circle(screen, 'black', pos, 17 , width=0)
                p.draw.circle(screen, COULEUR_DICT[elem.couleur], pos, 16 , width=0)
                p.display.flip()

class SCREEN(object):
    def __init__(self):
        Game_board = board_file.Board()
        Game_board.init_table()
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(p.Color('white'))
        init(self.screen)
        draw_pawns(self.screen, Game_board.board)
        p.event.get()
    def update_screen_board(self, board:np.array):
        draw_pawns(self.screen, board)
        p.event.get()

def main():
    gui = SCREEN()
    running = True
    while running:
        x = 1



    
    


if __name__ == '__main__':
    pass
    #main()