""" scrape https://nine.websudoku.com/ and get the layout of numbers on the sudoku board"""
from tkinter import * # pylint: disable=unused-import, unused-wildcard-import
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary # pylint: disable=unused-import

class WebScraper:
    """
    a class for scraping a website using Selenium and Beautiful soup
    """
    def scrape(self, u_r_l):
        """scrapes code"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.get(u_r_l)
        driver.implicitly_wait(10)
        page = driver.page_source
        driver.quit()
        return BeautifulSoup(page, 'html.parser')
    def find_element_by_id(self, source, element, value):
        """finds specified element by its id"""
        return source.find(element, id = value)
    def find_all_elements_with_a_value(self, source, element, value):
        """finds all elements that have a value"""
        return source.find_all(element, value = value)
    def find_parents_id(self, element, value):
        """ find the id of the parent of the specified element"""
        return element.find_parent(value).get('id')

soup = WebScraper().scrape("https://nine.websudoku.com/")
sudoku_table = WebScraper().find_element_by_id(soup, "table", "puzzle_grid" )
inputs_with_numbers = WebScraper().find_all_elements_with_a_value(sudoku_table, "input", True)

class SudokuBoard:
    """Sudoku game class"""
    def __init__(self):
        """constructor"""
        self.board = [["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", "", ""]]
        self.original_numbers = []
        self.row, self.col = -1, -1
        self.fill_in_the_starting_board()
        self.visualize()

    def fill_in_the_starting_board(self):
        """ fills the board data structure with starting numbers for the game"""
        for i in inputs_with_numbers:
            coordinates = WebScraper().find_parents_id(i, 'td' ).replace('c','')
            row = int(coordinates[0])
            column = int(coordinates[1])
            self.original_numbers.append((row, column))
            self.board[row][column] = int(i['value'])
        return self.board

    def visualize(self):
        """ Sudoku GIU - canvas with 9 * 9 grid, buttons with numbers 1-9 and a "Clear" button"""
        self.root = Tk()
        self.root.title("Sudoku")
        square = 50
        num_sq = 9
        thick_every = 3
        normal = 1
        wide = 3
        self.canvas = Canvas(self.root, width = num_sq * square, height= 450, bg ='white')
        self.canvas.bind("<Button-1>", self._cell_clicked)
        self.canvas.bind("<Key>", self._key_pressed)
        self.canvas.bind("<BackSpace>", self.do_backspace)
        self.canvas.pack(pady = 10)
        self._draw_puzzle()

        # draw horizontal lines
        x_1 = 0
        x_2 = 9 * square
        for _k in range(0, square * (num_sq + 1), square):
            y_1 = _k
            y_2 = _k
            if _k % thick_every:
                _w = normal
            else:
                _w = wide
            self.canvas.create_line(x_1, y_1, x_2, y_2, width = _w)

        # draw vertical lines
        y_1 = 0
        y_2 = 9 * square
        for _k in range(0, square * (num_sq + 1), square):
            x_1 = _k
            x_2 = _k
            if _k % thick_every:
                _w = normal
            else:
                _w = wide
            self.canvas.create_line(x_1, y_1, x_2, y_2, width = _w)

        # draw buttons
        buttons = Frame(self.root)
        buttons.pack()
        for _i in range(1, 10):
            button = Button(buttons, text = _i, width = 5, height = 2, bg = "black", \
            fg = "white", command = lambda _i = _i: self.number_button_pressed(_i))
            button.pack(side = LEFT)
        clear = Button(buttons, text = "Clear", width = 6, height = 2, bg = "white", \
        command = self.clear)
        clear.pack(side = LEFT)

        self.root.resizable(False, False)
        self.root.configure(bg = "white")
        self.root.mainloop()

    def _draw_puzzle(self):
        """fills cells with numbers from the board"""
        self.canvas.delete("numbers")
        for _x in range(9):
            for _y in range(9):
                element = self.board[_x][_y] 
                x_coor = _y * 50 + 25
                y_coor = _x * 50 + 25
                if (_x, _y) not in self.original_numbers:
                    self.canvas.create_text(x_coor, y_coor, text= element, \
                    tags="numbers", font = ("serif", 12))
                else:
                    self.canvas.create_text(x_coor, y_coor, text= element, \
                    tags="numbers", font = ("arial"))

    def _cell_clicked(self, event):
        """sets the focus on the selected cell"""
        _x, _y = event.x, event.y
        self.row, self.col = _y // 50, _x // 50
        self.canvas.focus_set()
        self._draw_cursor()

    def _draw_cursor(self):
        """draws the red rectangle selector on the selected cell"""
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x_0 = self.col * 50 + 1
            y_0 = self.row * 50 + 1
            x_1 = (self.col + 1) * 50 - 1
            y_1 = (self.row + 1) * 50 - 1
            if (self.row, self.col) not in self.original_numbers:
                self.canvas.create_rectangle(
                    x_0, y_0, x_1, y_1,
                    outline="red", tags="cursor")

    def _key_pressed(self, event):
        """puts the pressed keybord key in the selected cell"""
        if self.row >= 0 and self.col >= 0 and event.char in "123456789":
            self.board[self.row][self.col] = int(event.char)
            self._draw_puzzle()
            self._draw_cursor()
            self.check_win()

    def number_button_pressed(self, text):
        """puts the number`s value in the selected cell"""
        if self.row >= 0 and self.col >= 0:
            self.board[self.row][self.col] = int(text)
            self._draw_puzzle()
            self._draw_cursor()
            self.check_win()

    def clear(self):
        """clears the selected cell"""
        if self.row >= 0 and self.col >= 0:
            self.board[self.row][self.col] = ""
            self._draw_puzzle()
            self._draw_cursor()

    def do_backspace(self, event):
        """clears the selected cell with the backspace keyboard key"""
        if self.row >= 0 and self.col >= 0:
            self.board[self.row][self.col] = ""
            self._draw_puzzle()
            self._draw_cursor()
    
    def check_win(self):
        """checks if the winner filled the sudoku correctly"""
        for row in range(9):
            if not self.check_row(row):
                return False
        for column in range(9):
            if not self.check_column(column):
                return False
        for r in range(0, 7, 3):
            for c in range(0, 7, 3):
                if not self.check_square(r, c):
                    return False
        self.win()
        
    def check_block(self, block):
        """checks if the particular area is filled correctly"""
        return set(block) == set(range(1, 10))
    
    def check_row(self, row):
        """checks if the row is filled correctly"""
        return self.check_block(self.board[row])
    
    def check_column(self, column):
        """checks if the column is filled correctly"""
        return self.check_block(
            [self.board[row][column] for row in range(9)]
        )

    def check_square(self, r, c):
        """ checks if the board squares are filled correctly"""
        block = []
        for row in range(r, r + 3, 1):
            for column in range(c, c + 3, 1):
                block.append(self.board[row][column])
        return self.check_block(block)

    def win(self):
        self.win_frame = Frame(self.root, bg = "white")
        self.win_frame.pack()
        label = Label(self.win_frame, text = "Congrats! You have won!!!", bg = "white")
        label.pack(pady = 3)
        self.name_entry_frame = Frame(self.win_frame, bg = "white")
        self.name_entry_frame.pack()
        name = Label(self.name_entry_frame, text = "Your name:", bg = "white")
        name.pack(side = LEFT, pady = 3)
        entry_name = Entry(self.name_entry_frame, bd = 2)
        entry_name.pack(side = RIGHT, pady = 3)
        self.surname_entry_frame = Frame(self.win_frame, bg = "white")
        self.surname_entry_frame.pack()
        surname = Label(self.surname_entry_frame, text = "Your surname:", bg = "white")
        surname.pack(side = LEFT, pady = 3)
        entry_surname = Entry(self.surname_entry_frame, bd = 2)
        entry_surname.pack(side = RIGHT, pady = 3)
        submit = Button(self.win_frame, text = "Submit", bg = "black", fg = "white", height = 1, width = 6)
        submit.pack(pady = 3)
game = SudokuBoard()
