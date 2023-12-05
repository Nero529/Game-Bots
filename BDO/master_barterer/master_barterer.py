import math
import pyautogui
import pydirectinput
import cv2
import win32gui
import time
import pandas as pd

class Client:

    def __init__(self, handle=None):
        self._handle = handle

    def register_window(self, name="BLACK DESERT", nth=0):
        """ Assigns the instance to a window (Required before using any other API functions) """
        def win_enum_callback(handle, param):
            if str(win32gui.GetWindowText(handle)).find(name) != -1:
                param.append(handle)
                return handle

        handles = []
        # Get all windows with the name
        win32gui.EnumWindows(win_enum_callback, handles)
        
        handles.sort()
        # Assigns the one at index nth
        self._handle = handles[nth]
        #print('stuff: ', handles[nth])
        return self


    def match_image(self, largeImg, smallImg, threshold=0.2, debug=False):
        """ Finds smallImg in largeImg using template matching """
        """ Adjust threshold for the precision of the match (between 0 and 1, the lowest being more precise """
        """ Returns false if no match was found with the given threshold """
        method = cv2.TM_SQDIFF_NORMED

        # Read the images from the file
        small_image = cv2.imread(smallImg)
        large_image = cv2.imread(largeImg)
        h, w = small_image.shape[:-1]

        result = cv2.matchTemplate(small_image, large_image, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        if (mn >= threshold):
            return False

        # Extract the coordinates of our best match
        x, y = mnLoc

        if debug:
            # Draw the rectangle:
            # Get the size of the template. This is the same size as the match.
            trows, tcols = small_image.shape[:2]

            # Draw the rectangle on large_image
            cv2.rectangle(large_image, (x, y),
                            (x+tcols, y+trows), (0, 0, 255), 2)

            # Display the original image with the rectangle around the match.
            cv2.imshow('output', large_image)

            # The image is only displayed if we call this
            cv2.waitKey(0)

        # Return coordinates to center of match
        return (x + (w * 0.5), y + (h * 0.5))   #return (x + (w * 0.5), y + (h * 0.5))

    def set_active(self):
        """ Sets the window to active if it isn't already """
        if not self.is_active():
            """ Press alt before and after to prevent a nasty bug """
            pyautogui.press('alt')
            win32gui.SetForegroundWindow(self._handle)
            pyautogui.press('alt')
        return self

    def is_active(self):
        """ Returns true if the window is focused """
        return self._handle == win32gui.GetForegroundWindow()

def click(x,y, button='left'):
    pyautogui.mouseDown(x,y, button=button)
    time.sleep(0.5) 
    pyautogui.mouseUp(x,y, button=button)

def open_barters():
    pydirectinput.press('esc')
    time.sleep(0.3)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'barter_icon.png')
    click(x,y)
    time.sleep(0.3)

def get_route(item_name, tier):
    pydirectinput.moveTo(1100,375)
    click(1100,375)
    time.sleep(1)
    pyautogui.screenshot(game_img)
    if tier == 1:
        pydirectinput.moveTo(1100,400)
        time.sleep(0.5)
        click(1100,400)
    elif tier == 2:
        x,y = bdo.match_image(game_img, 'screenshots/tier2_trades.png')
        click(x,y)
        time.sleep(0.5)
    elif tier == 3:
        x,y = bdo.match_image(game_img, 'screenshots/tier3_trades.png')
        click(x,y)
        time.sleep(0.5)

    elif tier == 4:
        x,y = bdo.match_image(game_img, 'screenshots/tier4_trades.png')
        click(x,y)
        time.sleep(0.5)

    elif tier == 5:
        x,y = bdo.match_image(game_img, 'screenshots/tier5_trades.png')
        click(x,y)
        time.sleep(0.5)

    pyautogui.screenshot(game_img)
    x1,y1 = bdo.match_image(game_img, 'screenshots/search.png')
    click(x1-100,y1)
    time.sleep(1)
    for x in item_name:
        pydirectinput.press(x)
    pydirectinput.press('enter')
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'screenshots/navigate_button.png')
    pyautogui.moveTo(x,y)
    time.sleep(0.5)
    click(x,y)
    click(x1-100,y1)
    for x in range(len(item_name)):
        pydirectinput.press('backspace')
    pydirectinput.press('esc')
    pydirectinput.press('esc')
    pydirectinput.press('t')
    time.sleep(10)

def barter(quantity):
    pyautogui.screenshot(game_img)
    while not bdo.match_image(game_img, 'screenshots/anchor_button.png'):
        time.sleep(1)
        pyautogui.screenshot(game_img)
    pydirectinput.press('ctrlleft')
    time.sleep(1)
    x,y = bdo.match_image(game_img, 'screenshots/anchor_button.png')
    click(x,y)
    pyautogui.moveTo(500,500)
    time.sleep(0.5)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'screenshots/barter_button.png')
    click(x,y)
    time.sleep(0.5)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'screenshots/exchange.png')
    click(x,y)
    time.sleep(0.5)
    pydirectinput.press(quantity)
    pydirectinput.press('enter')
    pydirectinput.press('esc')
    time.sleep(0.5)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'screenshots/depart_button.png')
    click(x,y)
    pydirectinput.keyDown('s')
    time.sleep(20)
    pydirectinput.keyUp('s')

def read_config(file): # Reads config file for auto status and max_quantities desired
    file_opener = open(file)
    max_items = []
    auto = False
    for index, x in enumerate(file_opener):
        if index != 0:
            cap = int(x.split(":")[1])
            max_items.append(cap)
        else:
            if "Y" in x:
                auto = True
            
    return auto, max_items

def look_up_item(item_name, html_file): # Returns database item name, tier, and quantity
    barter_data = pd.read_html(html_file)[0]
    name_columns = ["B","E","H","K","N"]
    for tier, x in enumerate(name_columns):
        for index, row in enumerate(barter_data[x]):
            if index < 16:
                if type(row) is float: # Skips over NaN values for empty cells
                    pass
                else:
                    # Returns the full item name, tier of item, and quantity held
                    # chr(ord(x) + 1) used to convert column to ascii and then look one over for quantity
                    if item_name in row.lower():
                        return row.lower(), tier + 1, barter_data[chr(ord(x) + 1)][index] 
            else:
                break
    return False

def get_barter_quantity(tier): # Returns maximum barters for a given tier
    if tier !=5:
        return 10
    else:
        return 6


# Used for getting the player's desired max quantity for each tier of item (to be used for auto checking barter info)
#max_items = read_config("config.txt") 
html_file = 'Barter_Stock.html'
test = False
if not test:
    raw_item_list = input("Enter name of items in barter route: ")
    barter_item_list = []
    item_quantity = []
    item_name = ''
    for index, x in enumerate(raw_item_list):
        if x != ',':
            item_name += x
        else:
            if not look_up_item(item_name, html_file):
                print(item_name + " was not found. Terminating program")
            else:
                barter_item_list.append(look_up_item(item_name, html_file)[0])
                item_name = ''

        if index == len(raw_item_list) - 1 :
            if not look_up_item(item_name, html_file):
                print(item_name + " was not found. Terminating program")
            else:
                barter_item_list.append(look_up_item(item_name, html_file)[0])

    if len(barter_item_list) > 0:
        bdo = Client()
        bdo.register_window()
        bdo.set_active()
        game_img = 'screenshots/game_screen.png'
        tier = 2
        for index,item in enumerate(barter_item_list):
            open_barters()
            get_route(item, tier)
            barter(item_quantity[index])
            tier += 1
            if tier == 6:
                tier = 1
