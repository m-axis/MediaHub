from element_generator import *
from collections import OrderedDict
from common import *

window = sg.Window("PDF", layout)
col_img = [OrderedDict(), OrderedDict()]
IMG_SRC = 0
IMG_CHK = 1
IMG_POS = 2


def update(key, **kwargs):
    window[key].update(**kwargs)


def refresh(key):
    window.refresh()  # refresh required here
    window[key].contents_changed()


def all_keys():
    return window.key_dict.keys()


def clear_col_img(col):
    a_ks = all_keys()
    for a_k in a_ks:
        if f"IMAGE-PF-PAGE-{col}-" in a_k and not "-IMAGE" in a_k:
            act_img(a_k, dormant=True)
    if col_img[col]:
        col_img[col] = OrderedDict()


def act_img(i_key, visible=True, dormant=False):
    global col_img
    col = int(i_key.split("-")[-2])
    frame_key = f'FRAME-{i_key}'
    up_key = f"UP-{i_key}"
    down_key = f"DOWN-{i_key}"
    check_key = f"CHECK-{i_key}"
    if not dormant:
        col_img[col][i_key][IMG_CHK] = visible
        update(i_key, source=col_img[col][i_key][IMG_SRC] if visible else BLANK_PDF)
        update(frame_key, value="Selected" if visible else "")
        update(up_key, visible=visible)
        update(down_key, visible=visible)
        update(check_key, value=visible)
    else:
        if i_key in col_img[col].keys():
            col_img[col][i_key][IMG_CHK] = False
            col_img[col][i_key][IMG_SRC] = ""
        update(check_key, value=False)
    update(frame_key, visible=not dormant)


def on_file_load(file_path, col):
    global col_img
    images = pdf_to_image(file_path)
    a_ks = all_keys()
    for a_k in a_ks:
        if f"IMAGE-PF-PAGE-{col}-" in a_k and not "-IMAGE" in a_k:
            act_img(a_k, dormant=True)
    if col_img[col]:
        col_img[col] = OrderedDict()
    # GUI Updates
    update(f'PF-IMAGE-PLACEHOLDER-{col}', source='')
    update('BROWSE-PF-FILENAME-1', disabled=False)
    update('PF-SAVE', disabled=False)
    update('PF-PREVIEW', disabled=False)
    i = 0
    for img_b in images:
        img_k = f"IMAGE-PF-PAGE-{col}-{str(i)}"
        col_img[col][img_k] = []
        col_img[col][img_k].append(img_b)
        col_img[col][img_k].append(True)
        col_img[col][img_k].append(i)
        if img_k in a_ks:
            act_img(img_k)
            print(f"Found image key: {img_k}")
        else:
            i_key = f"IMAGE-PF-PAGE-{col}-{str(i)}"
            window.extend_layout(window[f'PF-VIEW-COLUMN-{col}'],
                                 add_image(i_key,
                                           source=img_b,
                                           enable_events=True))
            act_img(i_key)
            print(f"New image key: {i_key}")
        i += 1  # Increase counter for current file image key
    refresh(f'PF-VIEW-COLUMN-{col}')


def on_preview():
    global col_img


while True:
    event, values = window.read()
    if event in ('-exit-', None):
        break
    elif 'PF-FILENAME-0' in event:
        on_file_load(values[event], 0)
    elif 'PF-FILENAME-1' in event:
        on_file_load(values[event], 1)
    elif "CHECK-IMAGE-PF-PAGE-" in event:
        img_key = event.replace("CHECK-", "")
        act_img(img_key, values[event])
    elif "IMAGE-PF-PAGE-" in event and "-IMAGE-PF-PAGE" not in event:
        img_key = event
        chk_key = f"CHECK-{event}"
        act_img(img_key, not values[chk_key])
        # col = int(event.split("-")[-2])
        # print(col_img[col][event])
    elif "UP-IMAGE-PF-PAGE-" in event or "DOWN-IMAGE-PF-PAGE-" in event:
        print("Up or Down")
    else:
        print(event)

window.close()
