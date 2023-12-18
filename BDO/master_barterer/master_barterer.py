from barter_functions import Barterer
import os
import keyboard
import pyautogui



bdo_bot = Barterer()
bdo_bot.register_window("BLACK DESERT")
#bdo_bot.set_active()
check_pos = False
while check_pos:
    if keyboard.is_pressed('~'):
        print(pyautogui.position())
items = ['ancient order', 'urchin spine']

#bdo_bot.look_up_item(items[0])
bdo_bot.load_ship(['stone slab', 'ancient order'])


# test = True
# if not test:
#     raw_item_list = input("Enter name of items in barter route: ")
#     barter_item_list = []
#     item_quantity = []
#     item_name = ''
#     for index, x in enumerate(raw_item_list):
#         if x != ',':
#             item_name += x
#         else:
#             if not bdo_bot.look_up_item(item_name, html_file):
#                 print(item_name + " was not found\n")
#             else:
#                 barter_item_list.append(bdo_bot.look_up_item(item_name, html_file)[0])
#                 item_name = ''

#         if index == len(raw_item_list) - 1 :
#             if not bdo_bot.look_up_item(item_name, html_file):
#                 print(item_name + " was not found\n")
#             else:
#                 barter_item_list.append(bf.look_up_item(item_name, html_file)[0])

#     if len(barter_item_list) > 0:
#         bdo = Client()
#         bdo.register_window()
#         bdo.set_active()
#         game_img = 'screenshots/game_screen.png'
#         tier = 2
#         for index,item in enumerate(barter_item_list):
#             bf.open_barters()
#             bf.get_route(item, tier)
#             bf.barter(item_quantity[index])
#             tier += 1
#             if tier == 6:
#                 tier = 1

