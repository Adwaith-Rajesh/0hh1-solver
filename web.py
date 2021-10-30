from ast import literal_eval
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from solver import print_board
from solver import solve
from utils import GameDetails


game = GameDetails()


URL = "https://0hh1.com/"

identifier = {

    "board": (By.ID, "grid"),
    "td": (By.TAG_NAME, "td")

}


def print_debug(fn, *args):
    if os.environ.get("VERBOSE", 0):
        fn(*args)


def get_color_val(color: tuple[int, int, int]) -> int:

    TARGET_COLORS = {0: (42, 42, 42, 1), 1: (194, 75, 49, 1), 2: (48, 167, 194, 1)}

    def color_difference(color1, color2):
        return sum([abs(component1 - component2) for component1, component2 in zip(color1, color2)])

    differences = [[color_difference(color, target_value), target_name]
                   for target_name, target_value in TARGET_COLORS.items()]
    differences.sort()  # sorted by the first element of inner lists
    color_code = differences[0][1]

    return color_code


def get_board_from_element(driver: webdriver.Chrome) -> list[list[int]]:

    demo_board = []
    cells_to_click = []

    for i in range(game.shape):
        for j in range(game.shape):
            elem = driver.find_element(By.ID, f"tile-{j}-{i}")
            # print(elem.value_of_css_property("background-color"))

            c_val = elem.find_element(By.CLASS_NAME, "inner").value_of_css_property("background-color")

            # get the color val, 0, 1, 2
            color_val = get_color_val(literal_eval(c_val[4:]))

            cells_to_click.append(f"tile-{j}-{i}")
            demo_board.append(color_val)

    game.cells_to_click = cells_to_click

    return [demo_board[i:i + game.shape] for i in range(0, len(demo_board), game.shape)]


def get_element(driver: webdriver.Chrome, identifier: tuple[str, str], timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(identifier)
    )


def perform_clicks(driver: webdriver.Chrome, solved_board: list[list[int]],
                   cells_to_click: list[str]) -> None:

    for pos, click_count in zip(cells_to_click, [cell for s_list in solved_board for cell in s_list]):
        cell = driver.find_element(By.ID, pos)
        for _ in range(click_count):
            cell.click()


def start(shape: int) -> None:

    game.shape = shape

    driver = webdriver.Chrome()
    driver.get(URL)

    while True:
        print(f"Select a game with the shape {game.shape!r} and press enter.")
        input()

        board_elem = get_element(driver, identifier["board"])
        game.board_size = board_elem.size["width"]
        # save_element_as_png(driver, board)

        print_debug(print, "scanning for the board")

        board = get_board_from_element(driver)

        print_debug(print)
        print_debug(print, "The board")
        print_debug(print_board, board)
        print_debug(print)

        # solve the board
        solve(board)

        print_debug(print, "The solved board")
        print_debug(print_board, board)
        print_debug(print)

        print("Solving the web board")
        perform_clicks(driver, board, game.cells_to_click)

        print("Solved")
        print()

        while True:
            print("Pick the puzzle shape for the next round.")
            shape = int(input())
            if shape in [4, 6, 8, 10, 12]:
                game.shape = shape
                break

            else:
                print("The shape must be any of 4, 6, 8, 10, 12")


def run(shape: int) -> None:
    try:
        start(shape)
    except KeyboardInterrupt:
        print("Bye ...")
        quit()
