import time
import pyautogui
import win32gui
import cv2
import pytesseract
from PIL import ImageGrab,  Image
import pydirectinput
import math


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

    def get_horse_level(self):
        pyautogui.screenshot('BDO/horse_trainer/game_screen.png')
        x,y = self.match_image('BDO/horse_trainer/game_screen.png', 'BDO/horse_trainer/level_reference.png')
        pyautogui.screenshot('BDO/horse_trainer/horse_level.png', region=(x+12, y-10, 30, 30))
        pytesseract.pytesseract.tesseract_cmd = r'c:\program files\tesseract-ocr\tesseract.exe'
        #self.set_active()
        new_image_path = 'BDO/horse_trainer/horse_lvl_new'
        originalimage = cv2.imread('BDO/horse_trainer/horse_level.png')
        #originalimage = cv2.resize(originalimage, (0,0), fx=3, fy=3)
        copyimage = originalimage.copy()
        greyscale = cv2.cvtColor(copyimage, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(greyscale,160,255,cv2.ADAPTIVE_THRESH_MEAN_C)
        new_thresh = 255 - thresh
        cv2.imwrite((new_image_path + '.png'), new_thresh)
        level = int(pytesseract.image_to_string(Image.open('BDO/horse_trainer/horse_lvl_new.png'), lang='eng', config='--psm 7 -c tessedit_char_whitelist=1234567890'))
        return level

    def match_image(self, largeImg, smallImg, threshold=0.3, debug=False):
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

def filter_string(raw_string):
    new_string = ''
    for x in raw_string:
        print(ord(x))
        if ord(x) != 10:
            new_string = new_string + x
        else:
            break;
    return new_string
def is_time_interval(minute = -1, hour = -1, second = -1):
    current_hour = time.strftime("%H")
    current_min = time.strftime("%M")
    current_sec = time.strftime("%S")
    if minute != -1:
        if hour == -1:
            minute_check = int(current_min) % minute == 0
        else:
            minute_check = int(current_min) == 0
    else:
        minute_check = True

    if hour != -1:
         hour_check = int(current_hour) % hour == 0
    else:
        hour_check = True

    if second != -1:
        if minute == -1:
            second_check = int(current_sec) % second == 0
        else:
            second_check = int(current_sec) == 0
            
    else:
        second_check = True
    
    if minute_check and second_check and hour_check:
        time.sleep(1)
        return True
    else:
        time.sleep(1)
        return False

def click(x,y, button='left'):
    pyautogui.mouseDown(x,y, button=button)
    time.sleep(0.5) 
    pyautogui.mouseUp(x,y, button=button)

def set_path():
    pydirectinput.press('m')
    time.sleep(1)
    game_img = 'BDO/horse_trainer/game_screen.png'
    click(1369,1052)
    time.sleep(1)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'BDO/horse_trainer/route_1.png', threshold = 0.3)
    click(x,y)
    time.sleep(0.5)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'BDO/horse_trainer/load_route.png', threshold = 0.3)
    click(x,y)
    time.sleep(0.5)
    pydirectinput.press('m')
    time.sleep(2)
    pydirectinput.press('t')
    time.sleep(1)
    pydirectinput.press('p')
    

def turn_in(num_horses):
    pydirectinput.keyDown('s')
    time.sleep(1)
    pydirectinput.keyUp('s')
    time.sleep(1)
    pydirectinput.press('m')
    time.sleep(1)
    game_img = 'BDO/horse_trainer/game_screen.png'
    pyautogui.screenshot(game_img)
    click(1469,1052) # Coordinates of find npc button in map
    time.sleep(1)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'BDO/horse_trainer/npc_favorites.png', threshold = 0.3)
    click(x,y)
    time.sleep(0.5)
    click(x + 100, y + 100) # Coordinates for second favorite option (southern stable keeper duvencrune)
    time.sleep(0.5)
    pydirectinput.press('m')
    time.sleep(1.5)
    pydirectinput.press('p')
    time.sleep(1.5)
    pydirectinput.moveTo(1092,408)
    time.sleep(0.5)
    # Coordinates of horse costume pieces
    click(1092,408, button='right')
    click(1150,408, button='right')
    click(1200,408, button='right')
    click(1250,408, button='right')
    pydirectinput.press('p')
    pydirectinput.press('t')
    time.sleep(60)
    pydirectinput.press('r')
    time.sleep(1.5)
    pydirectinput.press('s')
    time.sleep(0.5)
    pydirectinput.press('t')
    pyautogui.screenshot(game_img)
    while not bdo.match_image(game_img, 'BDO/horse_trainer/stable_button.png', threshold = 0.2):
        pyautogui.screenshot(game_img)
        pydirectinput.press('r')
        time.sleep(1.5)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'BDO/horse_trainer/stable_button.png', threshold = 0.2)
    click(x,y)
    time.sleep(0.5)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'BDO/horse_trainer/check_in.png', threshold = 0.2)
    click(x,y)
    time.sleep(1)
    for increment in range(num_horses):
        click(100,275 + increment * 77)
        time.sleep(0.5)
        pyautogui.screenshot(game_img)
        if bdo.match_image(game_img, 'BDO/horse_trainer/imp_button.png', threshold = 0.2):
            x,y = bdo.match_image(game_img, 'BDO/horse_trainer/imp_button.png', threshold = 0.2)
            click(x,y)
            time.sleep(0.5)
            pydirectinput.press('enter')
    


def swap_horse():
    game_img = 'BDO/horse_trainer/game_screen.png'
    pydirectinput.moveTo(900,275)
    time.sleep(1)
    click(100,275)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'BDO/horse_trainer/take_out.png')
    click(x,y)
    time.sleep(1)
    pydirectinput.press('esc')
    time.sleep(0.5)
    pydirectinput.press('esc')
    pydirectinput.press('m')
    time.sleep(2)
    game_img = 'BDO/horse_trainer/game_screen.png'
    pyautogui.screenshot(game_img)
    click(1469,1052) # Coordinates of find npc button in map
    time.sleep(2)
    pyautogui.screenshot(game_img)
    x,y = bdo.match_image(game_img, 'BDO/horse_trainer/npc_favorites.png', threshold = 0.3)
    click(x,y)
    time.sleep(0.5)
    click(x + 100, y + 150) # Coordinates of third favorite option (east of southern stable keeper duvencrune)
    time.sleep(1)
    pydirectinput.press('m')
    time.sleep(2)
    pydirectinput.press('t')
    time.sleep(10)
    pydirectinput.press('ctrlleft')
    click(40,175)   # Coordinates of call horse icon
    time.sleep(7)
    click(40,175)   # Coordinates of call horse icon
    time.sleep(7)
    pydirectinput.press('f7')
    pydirectinput.press('i')
    click(1700,250) # Coordinates of pearl tab in inventory
    for increment in range(4):
        click(1500 + increment * 50, 550, button='right') # Coordinates of horse gear in pearl tab
    pydirectinput.press('esc')
    pydirectinput.press('esc')
    time.sleep(1)
    pydirectinput.press('r')
    time.sleep(1.5)


bdo = Client()
num_horses = int(input('Enter number of horses being trained: '))
bdo.register_window()
bdo.set_active()
time.sleep(1)
horse_finished = False
pydirectinput.press('9')
game_img = 'BDO/horse_trainer/game_screen.png'
for horse_num in range(num_horses):
    horse_level = 1
    count = 0
    set_path()
    print('Horse training commenced')
    while horse_level < 15 or horse_level > 30:
        horse_level = bdo.get_horse_level()
        time.sleep(1)
        count += 1
        if count >= 7200:
            count = 0
            pydirectinput.press('9')
    
    print('Horse number '  + str(horse_num + 1) + ' is done' )
    bdo.set_active()
    pydirectinput.press('p')
    turn_in(num_horses)
    print('Horse turned in')
    swap_horse()
    set_path()
    print('New horse taken out')



