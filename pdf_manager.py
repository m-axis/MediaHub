from element_generator import *
from collections import OrderedDict
from common import *
from PyPDF2 import PdfFileReader, PdfFileWriter

window = sg.Window("PDF Page Swap", layout)
col_img = [OrderedDict(), OrderedDict()]
img_size = [300, 300]
file_src = ["", ""]
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
    global col_img
    a_ks = all_keys()
    for a_k in a_ks:
        if f"IMAGE-PF-PAGE-{col}-" in a_k and not "-IMAGE" in a_k:
            act_img(a_k, dormant=True)
    if col_img[col]:
        col_img[col] = OrderedDict()


def act_img(i_key, visible=True, dormant=False):
    global col_img
    col = int(i_key.split("-")[-2])
    i_pos = int(i_key.split("-")[-1])
    frame_key = f'FRAME-{i_key}'
    up_key = f"UP-{i_key}"
    down_key = f"DOWN-{i_key}"
    check_key = f"CHECK-{i_key}"
    num_key = f"NUM-{i_key}"
    if not dormant:
        col_img[col][i_key][IMG_CHK] = visible
        update(i_key, source=resize_b(col_img[col][i_key][IMG_SRC], img_size[col]) if visible else BLANK_PDF)
        update(frame_key, value="Selected" if visible else "")
        update(up_key, visible=visible)
        update(down_key, visible=visible)
        update(check_key, value=visible)
        update(num_key, value=f"Page {col_img[col][i_key][IMG_POS] + 1}")
    else:
        if i_key in col_img[col].keys():
            col_img[col][i_key][IMG_CHK] = False
            col_img[col][i_key][IMG_SRC] = ""
        update(check_key, value=False)
    update(frame_key, visible=not dormant)


def on_file_load(file_path, col):
    global col_img
    global img_size
    images = pdf_to_image(file_path)
    file_src[col] = file_path
    pg_cnt = len(images)
    if 40 <= pg_cnt < 70:
        img_size[col] = 200
    elif 70 <= pg_cnt < 120:
        img_size[col] = 120
    elif 120 <= pg_cnt < 180:
        img_size[col] = 50
    elif 180 <= pg_cnt < 260:
        img_size[col] = 40
    elif 260 <= pg_cnt < 300:
        img_size[col] = 20
    elif pg_cnt > 300:
        img_size[col] = 10
    else:
        img_size[col] = 300
    a_ks = all_keys()
    clear_col_img(col)
    # GUI Updates
    update(f'PF-IMAGE-PLACEHOLDER-{col}', source='')
    update('BROWSE-PF-FILENAME-1', disabled=False)
    update('PF-SAVE', disabled=False)
    update('PF-PREVIEW', disabled=False)
    update('PF-CLEAR-COL-1', disabled=False)
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
                                           source=resize_b(img_b, img_size[col]),
                                           enable_events=True))
            act_img(i_key)
            print(f"New image key: {i_key} -- Size: {img_size[col]}")
        i += 1  # Increase counter for current file image key
    refresh(f'PF-VIEW-COLUMN-{col}')


def selected_pages():
    global col_img
    final_list = []
    for c_img in col_img:
        col_l = []
        for i_hash in c_img:
            if c_img[i_hash][IMG_CHK]:
                col_l.append(c_img[i_hash][IMG_POS])
        final_list.append(col_l)
    return final_list


def on_preview():
    global col_img
    pre_img = []
    for c_img in col_img:
        for i_hash in c_img:
            if c_img[i_hash][IMG_CHK]:
                pre_img.append([sg.Image(source=c_img[i_hash][IMG_SRC])])

    layout_p = [
        sg.Column(pre_img, key="PF-PREVIEW-COLUMN", size=P_VIEW_SIZE,
                  scrollable=True, vertical_scroll_only=True, justification="c"),
    ]
    win_p = sg.Window("File Preview", [layout_p], modal=True)
    while True:
        event_p, values_p = win_p.read()
        if event_p == "Exit" or event_p == sg.WIN_CLOSED:
            break
    win_p.close()


def on_up(button):
    global col_img
    global img_size
    img_k = button.replace("UP-", "")
    img_i = int(button.split("-")[-1])
    col = int(button.split("-")[-2])
    if img_i == 0:
        show_message("Page already at the top!")
    else:
        l_img_i = img_i - 1
        temp_k = img_k.split("-")
        temp_k.pop()
        l_img_k = "-".join(temp_k) + f"-{l_img_i}"
        # Swap hash values for both images
        temp_h = col_img[col][l_img_k]
        col_img[col][l_img_k] = col_img[col][img_k]
        col_img[col][img_k] = temp_h
        # Swap UI images
        act_img(img_k, col_img[col][img_k][IMG_CHK])
        act_img(l_img_k, col_img[col][l_img_k][IMG_CHK])
        refresh(f"PF-VIEW-COLUMN-{col}")


def on_down(button):
    global col_img
    global img_size
    img_k = button.replace("DOWN-", "")
    img_i = int(button.split("-")[-1])
    col = int(button.split("-")[-2])
    if (img_i + 1) == len(col_img[col]):
        show_message("Page already at the bottom!")
    else:
        n_img_i = img_i + 1
        temp_k = img_k.split("-")
        temp_k.pop()
        n_img_k = "-".join(temp_k) + f"-{n_img_i}"
        # Swap hash values for both images
        temp_h = col_img[col][n_img_k]
        col_img[col][n_img_k] = col_img[col][img_k]
        col_img[col][img_k] = temp_h
        # Swap UI images
        act_img(img_k, col_img[col][img_k][IMG_CHK])
        act_img(n_img_k, col_img[col][n_img_k][IMG_CHK])
        refresh(f"PF-VIEW-COLUMN-{col}")


def on_save(fp):
    global col_img
    save_page = []
    for c_img in col_img:
        temp = []
        for i_hash in c_img:
            if c_img[i_hash][IMG_CHK]:
                temp.append(c_img[i_hash][IMG_POS])
        save_page.append(temp)
    f_fmt = fp.split("/")[-1]
    output = PdfFileWriter()
    col = 0
    for src in file_src:
        if src:
            pdf_file = convert_to_pdf(src)
            if pdf_file:
                temp_pdf = PdfFileReader(open(pdf_file, "rb"))
                temp_pdf.decrypt('')
                for s_page in save_page[col]:
                    output.addPage(temp_pdf.getPage(s_page))
            else:
                show_message(f"Error converting to pdf\n{src}")
                break
        col += 1
    with open(fp, "wb") as outputStream:
        output.write(outputStream)
    # for del_file in files_to_delete:
    #     os.remove(del_file)
    show_message("File saved successfully!", True)


def main():
    while True:
        event, values = window.read()
        if event in ('-exit-', None):
            break
        elif 'PF-FILENAME-0' == event:
            on_file_load(values[event], 0)
        elif 'PF-FILENAME-1' == event:
            on_file_load(values[event], 1)
        elif "CHECK-IMAGE-PF-PAGE-" in event:
            img_key = event.replace("CHECK-", "")
            act_img(img_key, values[event])
        elif "IMAGE-PF-PAGE-" in event and "-IMAGE-PF-PAGE" not in event:
            img_key = event
            chk_key = f"CHECK-{event}"
            act_img(img_key, not values[chk_key])
        elif "UP-IMAGE-PF-PAGE-" in event:
            on_up(event)
        elif "DOWN-IMAGE-PF-PAGE-" in event:
            on_down(event)
        elif "PF-PREVIEW" == event:
            on_preview()
        elif "PF-FILE-SAVE" == event:
            on_save(values[event])
        elif "PF-CLEAR-COL-" in event:
            col = int(event.split("-")[-1])
            clear_col_img(col)
        else:
            print(event)
    window.close()


if __name__ == '__main__':
    main()
