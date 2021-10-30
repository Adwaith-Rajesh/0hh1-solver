from ast import literal_eval
from io import BytesIO
from pprint import pprint
from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import GameDetails


game = GameDetails()


URL = "https://0hh1.com/"

identifier = {

    "board": (By.ID, "grid"),
    "td": (By.TAG_NAME, "td")

}


def get_element_as_png(driver: webdriver.Chrome, element) -> ...:

    location = element.location
    size = element.size

    sleep(3)

    image = driver.get_screenshot_as_png()

    im = Image.open(BytesIO(image))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points

    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    return pixels


def get_color_val(color: tuple[int, int, int]) -> int:

    TARGET_COLORS = {0: (42, 42, 42, 1), 1: (194, 75, 49, 1), 2: (48, 167, 194, 1)}

    def color_difference(color1, color2):
        return sum([abs(component1 - component2) for component1, component2 in zip(color1, color2)])

    differences = [[color_difference(color, target_value), target_name]
                   for target_name, target_value in TARGET_COLORS.items()]
    differences.sort()  # sorted by the first element of inner lists
    my_color_name = differences[0][1]

    return my_color_name


def get_board_from_element(driver: webdriver.Chrome) -> list[list[int]]:

    demo_board = []

    for i in range(game.shape):
        for j in range(game.shape):
            elem = driver.find_element(By.ID, f"tile-{j}-{i}")
            # print(elem.value_of_css_property("background-color"))

            c_val = elem.find_element(By.CLASS_NAME, "inner").value_of_css_property("background-color")
            print(c_val, f"{i=}, {j=}")
            color_val = get_color_val(literal_eval(c_val[4:]))
            print(color_val)

            demo_board.append(color_val)

    print(demo_board)

    return [demo_board[i:i + game.shape] for i in range(0, len(demo_board), game.shape)]


def get_element(driver: webdriver.Chrome, identifier: tuple[str, str], timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(identifier)
    )


def start(shape: int) -> None:

    game.shape = shape

    driver = webdriver.Chrome()
    driver.get(URL)

    print("Move select the game shape and press enter.")
    input()

    print("Moved")
    board_elem = get_element(driver, identifier["board"])
    game.board_size = board_elem.size["width"]
    # save_element_as_png(driver, board)

    board = get_board_from_element(driver)
    pprint(board, width=game.shape * 5)

    input()


def run(shape: int) -> None:
    start(shape)
