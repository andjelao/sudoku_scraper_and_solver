""" scrape https://nine.websudoku.com/ and get the layout of numbers on the sudoku board"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary # pylint: disable=unused-import

URL = "https://nine.websudoku.com/"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
driver.get(URL)
driver.implicitly_wait(10)
page = driver.page_source
driver.quit()
soup = BeautifulSoup(page, 'html.parser')

class Finder:
    """
    a class for finding a specified element using different functions
    """
    def __init__(self, source, element, value):
        self.source = source
        self.element = element
        self.value = value
    def find_element_by_id(self):
        """finds specified element by its id"""
        return self.source.find(self.element, id = self.value)
    def find_all_elements_with_a_value(self):
        """finds all elements that have a value"""
        return self.source.find_all(self.element, value = self.value)
    def find_parents_id(self):
        """ find the id of a parent of the specified element"""
        return self.element.find_parent(self.value).get('id').replace('c','')

class Number: #pylint: disable=too-few-public-methods
    """ a class whose objects are numbers on the sudoku board,
    with their values, columns and rows """
    def __init__(self, value, column_number, row_number):
        self.value = value
        self.column_number = column_number
        self.row_number = row_number
    def __repr__(self):
        return f"[value: {self.value}, column: {self.column_number}, row: {self.row_number}]"

sudoku_table = Finder(soup, "table", "puzzle_grid").find_element_by_id()
list_of_inputs_with_numbers = Finder(sudoku_table, "input", True).find_all_elements_with_a_value()
list_of_number_objects = []
for i in list_of_inputs_with_numbers:
    coordinates = Finder("", i, 'td' ).find_parents_id()
    list_of_number_objects.append(Number(i['value'], coordinates[0], coordinates[1]))
