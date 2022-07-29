from common import *


bg_color = "#444444"
# sg.theme_background_color(), sg.theme_background_color()
buttons_layout = [
    [
     sg.Text('Media Hub', background_color=bg_color),
     sg.Text(' ' * 102, background_color=bg_color),
     # sg.Button('', image_data=MAC_GREEN,
     #           button_color=(bg_color, bg_color), key='MN-MINIMIZE'),
     # sg.Button('', image_data=MAC_ORANGE,
     #           button_color=(bg_color, bg_color)),
     sg.Button(image_data=MAC_RED,
               button_color=(bg_color, bg_color), key='MN-EXIT'),
     ], ]

frame_layout = [sg.Frame('', buttons_layout, element_justification='right', background_color=bg_color)]
