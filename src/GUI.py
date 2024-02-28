import board_file
import utils
import string

CELL_WIDTH = 3
CELL_HEIGHT = 3

WIDTH = board_file.WIDTH
LENGTH = board_file.LENGTH

class Gui(object):
    def __init__(self):
        pass
    
    def print_up_border(self, offset = ''):
        print(offset, end = '')
        for i in range(WIDTH*4 + 1): # per cell
            if i % 4 == 0:
                print('+', end = '')
            else:
                print("-", end = '') 
        print('')
    
    def print_middle_cell(self, row, nbr_row):
        j = 0
        #print('A', end = '')
        print(f' {nbr_row} ', end = '')
        for i in range(WIDTH*4 + 1):
            if i % 4 == 0:
                print('|', end = '')
            elif i%2==0 and i%4 !=0 and j<len(row):
                #print(row[j], j, row)
                print(row[j], end = '') 
                j+=1
            else:
                print(' ', end = '')
        print('')
    def print_letter_up(self, offset=''):
        print('   ')
        print(offset, end = '')
        j = 0
        for i in range(WIDTH*4 + 1):
            if i%2==0 and i%4 !=0:
                print(string.ascii_uppercase[j], end = '')
                j+=1
            else:
                print(' ', end = '')
        print('')
            

    def Pretty_print(self, Board):
        offset = '   '
        self.print_letter_up(offset)
        self.print_up_border(offset)
        
        for idr, row in enumerate(Board):
            self.print_middle_cell(row, idr+1)
            self.print_up_border(offset)


if __name__ == '__main__':
    GuiT = Gui('Ben')
    GuiT.print_up_border()
    GuiT.print_up_border()