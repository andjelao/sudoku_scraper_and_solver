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
        """ find the id of a parent of the specified element"""
        return element.find_parent(value).get('id')

soup = WebScraper().scrape("https://nine.websudoku.com/")
sudoku_table = WebScraper().find_element_by_id(soup, "table", "puzzle_grid" )
inputs_with_numbers = WebScraper().find_all_elements_with_a_value(sudoku_table, "input", True)

class SudokuBoard:
    """Sudoku game class"""
    board = [["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""]]

    def fill_in_the_starting_board(self):
        """ fills the board data structure with starting numbers for the game"""
        for i in inputs_with_numbers:
            coordinates = WebScraper().find_parents_id(i, 'td' ).replace('c','')
            SudokuBoard.board[int(coordinates[0])][int(coordinates[1])] = i['value']
        return SudokuBoard.board

    def visualize(self):
        """ Sudoku GIU """
        root = Tk()
        root.title("Sudoku")
        square = 50
        num_sq = 9
        thick_every = 3
        normal = 1
        wide = 3
        canvas = Canvas(root, width = num_sq * square, height= 9 * square, bg ='white')
        canvas.pack()

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
            canvas.create_line(x_1, y_1, x_2, y_2, width = _w)

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
            canvas.create_line(x_1, y_1, x_2, y_2, width = _w)

        # draw cells with text
        for _x in range(9):
            for _y in range(9):
                if SudokuBoard.board[_x][_y] != "":
                    x_coor = _y * 50 + 25
                    y_coor = _x * 50 + 25
                    canvas.create_text(x_coor, y_coor, text= SudokuBoard.board[_x][_y])
        root.mainloop()

SudokuBoard().fill_in_the_starting_board()
SudokuBoard().visualize()
