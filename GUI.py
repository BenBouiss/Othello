import board_file

CELL_WIDTH = 3
CELL_HEIGHT = 3

WIDTH = board_file.WIDTH
LENGTH = board_file.LENGTH

class Gui(object):
    def __init__(self):
        pass
    
    def print_up_border(self):
        for i in range(WIDTH*5 - 3): # per cell
            if i % 4 == 0:
                print('+', end = '')
            else:
                print("-", end = '') 
        print('')
    
    def print_middle_cell(self, row):
        j = 0
        #print('A', end = '')
        for i in range(WIDTH*5 - 2):
            if i % 4 == 0:
                print('|', end = '')
            elif i%2==0 and i%4 !=0 and j<len(row):
                #print(row[j], j, row)
                print(row[j], end = '') 
                j+=1
            else:
                print(' ', end = '')
        print('')
        
    def Pretty_print(self, Board):
        self.print_up_border()
        for row in Board:
            self.print_middle_cell(row)
            self.print_up_border()


if __name__ == '__main__':
    GuiT = Gui('Ben')
    GuiT.print_up_border()
    GuiT.print_up_border()