import math
import pyautogui
import pydirectinput
import cv2
import win32gui
import time
import pandas as pd
import io
import os
import keyboard

class Client:

    def __init__(self, handle=None):
        self._handle = handle
        self.dimensions = None

    def register_window(self, name="", nth=0):
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
        self.dimensions = win32gui.GetWindowRect(self._handle)
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
    
    def get_window_dims(self):
        return self.dimesions

    def screenshot(self,file,x1=0,y1=0,x2=0,y2=0):
        if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
            x1 = self.dimensions[0]
            y1 = self.dimensions[1]
            x2 = self.dimensions[2]
            y2 = self.dimensions[3]
        pyautogui.screenshot(file, region=(x1,y1,x2-x1,y2-y1))


class Barterer(Client):

    def __init__(self):
        super().__init__(handle=None)
        self.home = os.getcwd() + '\BDO\master_barterer'
        self.game_img = self.home + '\screenshots\game_screen.png'
        config = self.home + '\config.txt'

        os.chdir(self.home)
        self.barter_data = self.get_barter_data('barter.html')
        self.config = config
        

    def click(self, x,y, button='left'):
        pyautogui.moveTo(x,y)
        time.sleep(0.3)
        pyautogui.mouseDown(x,y, button=button)
        time.sleep(0.5) 
        pyautogui.mouseUp(x,y, button=button)

    def open_barters(self):
        pydirectinput.press('esc')
        time.sleep(0.3)
        self.screenshot(self.game_img)
        x,y = self.match_image(self.game_img, 'screenshots/barter_icon.png')
        self.click(x,y)
        time.sleep(0.3)

    def get_route(self,item_name, tier):
        pydirectinput.moveTo(1100,375)
        self.click(1100,375)
        time.sleep(1)
        self.screenshot(self.game_img)
        if tier == 1:
            pydirectinput.moveTo(1100,400)
            time.sleep(0.5)
            self.click(1100,400)
        elif tier == 2:
            x,y = self.match_image(self.game_img, 'screenshots/tier2_trades.png')
            self.click(x,y)
            time.sleep(0.5)
        elif tier == 3:
            x,y = self.match_image(self.game_img, 'screenshots/tier3_trades.png')
            self.click(x,y)
            time.sleep(0.5)

        elif tier == 4:
            x,y = self.match_image(self.game_img, 'screenshots/tier4_trades.png')
            self.click(x,y)
            time.sleep(0.5)

        elif tier == 5:
            x,y = self.match_image(self.game_img, 'screenshots/tier5_trades.png')
            self.click(x,y)
            time.sleep(0.5)

        self.screenshot(self.game_img)
        x1,y1 = self.match_image(self.game_img, 'screenshots/search.png')
        self.click(x1-100,y1)
        time.sleep(1)
        for x in item_name:
            pydirectinput.press(x)
        pydirectinput.press('enter')
        self.screenshot(self.game_img)
        x,y = self.match_image(self.game_img, 'BDO/master_barterer/screenshots/navigate_button.png')
        pyautogui.moveTo(x,y)
        time.sleep(0.5)
        self.click(x,y)
        self.click(x1-100,y1)
        for x in range(len(item_name)):
            pydirectinput.press('backspace')
        pydirectinput.press('esc')
        pydirectinput.press('esc')
        pydirectinput.press('t')
        time.sleep(10)

    def barter(self, quantity):
        self.screenshot(self.game_img)
        while not self.match_image(self.game_img, 'screenshots/anchor_button.png'):
            time.sleep(1)
            self.screenshot(self.game_img)
        pydirectinput.press('ctrlleft')
        time.sleep(1)
        x,y = self.match_image(self.game_img, 'screenshots/anchor_button.png')
        self.click(x,y)
        pyautogui.moveTo(500,500)
        time.sleep(0.5)
        self.screenshot(self.game_img)
        x,y = self.match_image(self.game_img, 'screenshots/barter_button.png')
        self.click(x,y)
        time.sleep(0.5)
        self.screenshot(self.game_img)
        x,y = self.match_image(self.game_img, 'screenshots/exchange.png')
        self.click(x,y)
        time.sleep(0.5)
        pydirectinput.press(quantity)
        pydirectinput.press('enter')
        pydirectinput.press('esc')
        time.sleep(0.5)
        self.screenshot(self.game_img)
        x,y = self.match_image(self.game_img, 'screenshots/depart_button.png')
        self.click(x,y)
        pydirectinput.keyDown('s')
        time.sleep(20)
        pydirectinput.keyUp('s')

    def read_config(self): # Reads config file for auto status and max_quantities desired
        file_opener = open(self.config)
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

    def get_barter_data(self, html_file):
        self.barter_data = pd.read_html(html_file)
        return self.barter_data[0]

    def look_up_item(self,item_name): # Returns database item name, tier, and quantity
        name_columns = ["B","E","H","K","N"]
        for tier, x in enumerate(name_columns):
            for index, row in enumerate(self.barter_data[x]):
                if index < 16:
                    if type(row) is float: # Skips over NaN values for empty cells
                        pass
                    else:
                        
                        # Returns the full item name, tier of item, and quantity held
                        # chr(ord(x) + 1) used to convert column to ascii and then look one over for quantity
                        if item_name in row.lower():
                            return row.lower(), int(tier + 1), int(self.barter_data[chr(ord(x) + 1)][index]) 
                else:
                    break
        return False

    def get_barter_quantity(self,tier): # Returns maximum barters for a given tier
        if tier !=5:
            return 10
        else:
            return 6

    def click_img(self,img, threshold,is_item=True,button='left', offset_x=0, offset_y=0, region=None): #
        
        if is_item:
            self.change_directory('items')
        else:
            self.change_directory('utility')
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        if region is not None:
            x1,y1,x2,y2 = region
        self.screenshot(self.game_img,x1,y1,x2,y2)
        while not self.match_image(self.game_img, img, threshold=threshold):
            self.screenshot(self.game_img,x1,y1,x2,y2)
            time.sleep(0.05)
        x,y = self.match_image(self.game_img, img,threshold=threshold)
        self.click(x+offset_x,y+offset_y,button=button)
        pyautogui.moveTo(0,10)
        os.chdir('..')

    def to_iliya(self):
        pydirectinput.press('m')
        self.click_img('find_npc.png', 0.2)
        self.click_img('favorites.png',0.3)
        if not 'screenshots' in os.getcwd():
            os.chdir('screenshots')
        while not self.match_image(self.game_img,'dario_favorite.png',threshold=0.1):
            pyautogui.screenshot(self.game_img)
        x,y = self.match_image(self.game_img,'dario_favorite.png',threshold=0.1)
        a,b = self.match_image('dario_favorite.png', 'locate_npc.png',threshold=0.2)
        self.click(x+a/2 - 10, y)
        pydirectinput.press('m')
        time.sleep(1.5)
        pydirectinput.press('t')
        print('Navigating to Dario at Iliya\n')
        os.chdir('..')

    def to_dario(self):
        at_iliya = False
        count = 0
        if not 'screenshots' in os.getcwd():
            os.chdir('screenshots/utility')
        print('Going ashore\n')
        while not at_iliya:
            self.screenshot(self.game_img)
            if self.match_image(self.game_img,'disembark.png', threshold=0.1):
                count += 1
                time.sleep(0.5)
            else:
                count = 0

            if count == 3:
                at_iliya = True

        pydirectinput.press('ctrl')
        while self.match_image(self.game_img,'disembark.png', threshold=0.1):
            self.click_img('disembark.png',threshold=0.1)
            os.chdir('screenshots')
            time.sleep(1)
            self.screenshot(self.game_img)
            
        time.sleep(1)
        pydirectinput.press('ctrl')
        print('Talking to Dario')
        pydirectinput.press('r')

    def repair_ship(self):
        print('Repair ship\n')
        self.click_img('repair_icon.png',threshold=0.2,is_item=False)
        if not 'screenshots' in os.getcwd():
            os.chdir('screenshots/utility')
        while not self.match_image(self.game_img,'repair.png',threshold=0.2):
            self.screenshot(self.game_img)
            time.sleep(0.3)
        x, y = self.match_image(self.game_img,'repair.png',threshold=0.2)
        self.click(x-120,y)
        pydirectinput.press('space')
        pydirectinput.press('esc')

    def buy_supplies(self):
        print('Buying supplies for the ship\n')
        self.click_img('wharf.png',0.2,is_item=False)
        self.click_img('buy_supplies.png',0.2,is_item=False)
        pydirectinput.press('space')

    def unload_ship(self, barter_item_list):
        print('Offloading', barter_item_list[0],'from the ship\n')
        self.click(304,215)
        self.click_img('load_cargo.png',0.2,is_item=False)
        if not 'screenshots' in os.getcwd():
            os.chdir('screenshots/utility')

        # Finds the load icon from the load cargo to then generate the region for the 'My Ship' inventory
        while not self.match_image(self.game_img,'load_icon.png',threshold=0.1):
            self.screenshot(self.game_img)
            time.sleep(0.3)
        x, y = self.match_image(self.game_img,'load_icon.png',threshold=0.1)
        x -= 20
        y += 50
        
        while self.match_image(self.game_img, barter_item_list[0] + '.png', threshold=0.15):
            self.click_img(barter_item_list[0] + '.png',threshold=0.2, button='right', offset_x = x, offset_y = y,
                    region=(x,y,400,500))
            pydirectinput.press('f')
            pydirectinput.press('space')
            os.chdir('screenshots')
            time.sleep(0.5)
            self.screenshot(self.game_img, x,y,400,500)
        barter_item_list.pop(0)
        return barter_item_list

    def load_ship(self, barter_item_list):
        print('Loading', barter_item_list[0],'on the ship\n')
        pydirectinput.pause = 0.01
        self.click_img('barter_info.png',0.1,is_item=False)
        
        # Gets the tier of the item and then clicks on that appropriate tier sort option
        tier_trade = "tier" + str(self.look_up_item(barter_item_list[0])[1]) + "_trades.png"
        self.screenshot(self.game_img)
        self.change_directory('screenshots')
        while not self.match_image(self.game_img,'barter_ui.png',threshold=0.1):
            self.screenshot(self.game_img)
        ui_x,ui_y = self.match_image(self.game_img,'barter_ui.png',threshold=0.1)
        self.click(ui_x+800,ui_y+240)
        self.click_img(tier_trade,0.2,is_item=False)

        # Clicks the text field to search item
        self.click(ui_x+800,ui_y+200)
        for c in barter_item_list[0]:
            pydirectinput.press(c)
        pydirectinput.press('enter')
        print(ui_x,ui_y)
        self.screenshot(self.game_img,ui_x,ui_y,1500,860)
        os.chdir('items')
        # Searches all pngs to find the item on the left hand side to trade for desired item
        item_to_get = ' '
        while item_to_get == ' ':
            for x in os.listdir():
                if x != barter_item_list[0] + '.png' and x != 'barter_ui.png':
                    if self.match_image(self.game_img,x,threshold=0.1,debug=True):
                        item_to_get = x
                        break             
        pydirectinput.press('esc')
        pydirectinput.press('esc')
        pyautogui.moveTo(0,10)
        time.sleep(1)
        self.screenshot(self.game_img)
        while not self.match_image(self.game_img,item_to_get,threshold=0.1):
            pyautogui.moveTo(2222,922)
            for _ in range(6):
                pyautogui.scroll(-1)
                time.sleep(0.05)
            pyautogui.moveTo(0,10)
            self.screenshot(self.game_img)
        x,y = self.match_image(self.game_img,item_to_get,threshold=0.1)
        self.click(x,y,button='right')
        quantity = str(self.get_barter_quantity(self.look_up_item(barter_item_list[0])[1]))
        for x in quantity:
            pydirectinput.press(x)

        pydirectinput.press('space')
        pydirectinput.press('esc')
        pydirectinput.press('esc')
        pydirectinput.press('esc')
        time.sleep(0.5)

    def board_ship(self):
        print("Boarding ship!\n")
        pydirectinput.press('ctrl')
        if not 'screenshots' in os.getcwd():
            os.chdir('screenshots')
        self.screenshot(self.game_img)
        while self.match_image(self.game_img,'board_button.png',threshold=0.2):
            self.click_img('board_button.png',threshold=0.2)
            os.chdir('screenshots')
            self.screenshot(self.game_img)
        print('Ready to set sail!\n')

    def iliya_routine(self,barter_item_list):
        items = []
        self.to_iliya()
        self.to_dario()
        self.repair_ship()
        self.buy_supplies()
        items = self.unload_ship(barter_item_list)
        self.load_ship(items)
        self.board_ship()
        return items

    def change_directory(self, target_path):
        path_found = ''
        w = os.walk(self.home)
        for dir_path, dir_names, file_names in w:
            if target_path in dir_names:
                path_found = dir_path + '\\' + target_path
        os.chdir(path_found)


