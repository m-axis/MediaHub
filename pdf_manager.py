from element_generator import *
from common import *
import re

window = sg.Window("PDF", layout)
page_counter0 = 0
page_counter1 = 0
selected_pages = [[],[]]
all_images = [[], []]
while True:
    event, values = window.read()
    if event in ('-exit-', None):
        break
    elif 'PF-FILENAME-0' in event:
        images = pdf_to_image(values[event])
        all_images[0] = images
        window['PF-VIEW-COLUMN-0'].update(visible=True)
        window['FRAME-PF-ACTION'].update(visible=True)
        window['BROWSE-PF-FILENAME-1'].update(visible=True)
        for image_b in images:
            window.extend_layout(window['PF-VIEW-COLUMN-0'],
                                 image(f"IMAGE-PF-PAGE-0-{str(page_counter0)}", source=image_b, enable_events=True))
            page_counter0 += 1
        window.refresh()  # refresh required here
        window['PF-VIEW-COLUMN-0'].contents_changed()
    elif 'PF-FILENAME-1' in event:
        images = pdf_to_image(values[event])
        all_images[1] = images
        window['PF-VIEW-COLUMN-1'].update(visible=True)
        window['FRAME-PF-ACTION'].update(visible=True)
        for image_b in images:
            window.extend_layout(window['PF-VIEW-COLUMN-1'],
                                 image(f"IMAGE-PF-PAGE-1-{str(page_counter1)}", source=image_b, enable_events=True))
            print(f"IMAGE-PF-PAGE-{str(page_counter1)}")
            page_counter1 += 1
        window.refresh()  # refresh required here
        window['PF-VIEW-COLUMN-1'].contents_changed()
    elif "CHECK-IMAGE-PF-PAGE-" in event:
        image_index = int(event.split("-")[-1])
        loc_index = int(event.split("-")[-2])
        image_key = event.replace("CHECK-", "")
        frame_key = f'FRAME-{image_key}'
        up_key = f"UP-{image_key}"
        down_key = f"DOWN-{image_key}"
        if values[event]:
            image_source = all_images[loc_index][image_index]
            frame_title = "Selected"
        else:
            image_source = BLANK_PDF
            frame_title = ""
        window[image_key].update(source=image_source)
        window[frame_key].update(value=frame_title)
        window[up_key].update(visible=values[event])
        window[down_key].update(visible=values[event])
    elif "UP-IMAGE-PF-PAGE-" in event or "DOWN-IMAGE-PF-PAGE-" in event:
        print("Up or Down")
    elif "IMAGE-PF-PAGE-" in event:
        image_index = int(event.split("-")[-1])
        loc_index = int(event.split("-")[-2])
        check_key = f'CHECK-{event}'
        frame_key = f'FRAME-{event}'
        up_key = f"UP-{event}"
        down_key = f"DOWN-{event}"
        if values[check_key]:
            image_source = BLANK_PDF
            frame_title = ""
            checked = False
        else:
            image_source = all_images[loc_index][image_index]
            frame_title = "Selected"
            checked = True
        window[frame_key].update(value=frame_title)
        window[event].update(source=image_source)
        window[check_key].update(value=checked)
        window[up_key].update(visible=checked)
        window[down_key].update(visible=checked)
    else:
        print(event)

window.close()
