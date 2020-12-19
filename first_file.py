""" scrape code off of https://nine.websudoku.com/ and get the layout of numbers on the sudoku board
"""
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

#find the table which contains the sudoku board
table = soup.find("table", id="puzzle_grid")

#find all inputs from the table and put them in a list
list_of_inputs = table.find_all(value = True)

#get value of every input from the list
#get class of parent element for every input
input_values_list = []
class_list = []
for inp in list_of_inputs:
    input_values_list.append(inp['value'])
    class_list.append(inp.find_parent('td').get('id').replace('c',''))
print(input_values_list)
print(class_list)
