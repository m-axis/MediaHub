from element_generator import *
from collections import OrderedDict
from common import *
from PyPDF2 import PdfFileReader, PdfFileWriter

window = sg.Window("PDF Page Swap", layout, size=MAIN_WINDOW_SIZE, resizable=True, icon=APP_ICON, font=WIN_FONT)
col_img = [OrderedDict(), OrderedDict()]
img_size = [300, 300]
file_src = ["", ""]
page_selected = [0, 0]
IMG_SRC = 0
IMG_CHK = 1
IMG_POS = 2
ALLOWED_FILES = ["pdf", "png", "bmp", "jpg", "jpeg", "gif", "tiff"]
pages = 0


def update(key, **kwargs):
    try:
        window[key].update(**kwargs)
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def refresh(key):
    try:
        window.refresh()  # refresh required here
        window[key].contents_changed()
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def all_keys():
    try:
        return window.key_dict.keys()
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")
        return []


def clear_col_img(col, reset=False):
    try:
        global col_img
        global page_selected
        a_ks = all_keys()
        for a_k in a_ks:
            if f"IMAGE-PF-PAGE-{col}-" in a_k and not "-IMAGE" in a_k:
                act_img(a_k, dormant=True)
        if col_img[col]:
            col_img[col] = OrderedDict()
        page_selected[col] = 0
        if reset:
            update(f'PF-IMAGE-PLACEHOLDER-{col}', source=BLANK_PDF)
            update(f'PF-PAGE-LOAD-{col}', value="")
            update_save_btn()
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def act_img(i_key, visible=True, dormant=False, move=False):
    try:
        global col_img
        global page_selected
        global pages
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
        if not move:
            if i_key in col_img[col].keys() and col_img[col][i_key][IMG_CHK]:
                page_selected[col] += 1
            elif i_key in col_img[col].keys() and not col_img[col][i_key][IMG_CHK]:
                page_selected[col] -= 1
            update(f"PF-PAGE-LOAD-{col}", value=f'{page_selected[col]}/{pages}')
        update(frame_key, visible=not dormant)
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def spin_me(col):
    update(f'PF-IMAGE-PLACEHOLDER-{col}', source='')
    update(f'PF-IMAGE-PLACEHOLDER-{col}', data=sg.DEFAULT_BASE64_LOADING_GIF)
    window[f'PF-IMAGE-PLACEHOLDER-{col}'].update_animation_no_buffering(sg.DEFAULT_BASE64_LOADING_GIF,
                                                                        time_between_frames=100)
    refresh(f"PF-VIEW-COLUMN-{col}")


def on_file_load(file_path, col):
    try:
        fmt = file_path.split(".")[-1]
        if fmt.lower() in ALLOWED_FILES:
            global col_img
            global img_size
            global page_selected
            global pages
            page_selected[col] = 0
            images = pdf_to_image(file_path)
            pages = len(images)
            if images:
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
                i = 0
                for img_b in images:
                    # page_selected[col] += 1
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
                    # if i == 0:
                    #     update(f"UP-{img_k}", disabled=True)
                    # if i == pages-1:
                    #     update(f"DOWN-{img_k}", disabled=True)

                    i += 1  # Increase counter for current file image key
                    update(f"PF-PAGE-LOAD-{col}", value=f'{i}/{pages}')
                    refresh(f'PF-VIEW-COLUMN-{col}')
                update(f'PF-IMAGE-PLACEHOLDER-{col}', source='')
                update('BROWSE-PF-FILENAME-1', disabled=False)
                update('PF-SAVE', disabled=False)
                update('PF-PREVIEW', disabled=False)
                update('PF-CLEAR-COL-0', disabled=False)
                update('PF-CLEAR-COL-1', disabled=False)
                refresh(f'PF-VIEW-COLUMN-{col}')
            else:
                show_message("Count not convert pdf to images.")
        else:
            clear_col_img(col, True)
            show_message(
                f".{fmt.upper()} file not allowed. Please choose any of the following files:\n .{' , .'.join(ALLOWED_FILES)}",
                auto_c=False)
    except Exception as error:
        clear_col_img(col)
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def update_save_btn():
    global page_selected
    print(page_selected)
    if page_selected[0] > 0 or page_selected[1] > 0:
        update("PF-SAVE", disabled=False)
        update("PF-PREVIEW", disabled=False)
    else:
        update("PF-SAVE", disabled=True)
        update("PF-PREVIEW", disabled=True)


def on_preview():
    try:
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
        if pre_img:
            win_p = sg.Window("File Preview", [layout_p], modal=True)
            while True:
                event_p, values_p = win_p.read()
                if event_p == "Exit" or event_p == sg.WIN_CLOSED:
                    break
            win_p.close()
        else:
            show_message(f"No page selected for preview. Please select at least 1 page.")
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def on_up(button):
    try:
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
            act_img(img_k, col_img[col][img_k][IMG_CHK], move=True)
            act_img(l_img_k, col_img[col][l_img_k][IMG_CHK], move=True)
            refresh(f"PF-VIEW-COLUMN-{col}")
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def on_down(button):
    try:
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
            act_img(img_k, col_img[col][img_k][IMG_CHK], move=True)
            act_img(n_img_k, col_img[col][n_img_k][IMG_CHK], move=True)
            refresh(f"PF-VIEW-COLUMN-{col}")
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def on_save(fp):
    try:
        global col_img
        save_page = []
        for c_img in col_img:
            temp = []
            for i_hash in c_img:
                if c_img[i_hash][IMG_CHK]:
                    temp.append(c_img[i_hash][IMG_POS])
            save_page.append(temp)
        f_fmt = fp.split("/")[-1]
        col = 0
        new_files = []
        dir_path = f'{os.getenv("APPDATA")}\\MediaHub\\merged'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if save_page:
            for src in file_src:
                if src:
                    pdf_file = convert_to_pdf(src)
                    if pdf_file:
                        with open(pdf_file, "rb") as in_stream:
                            temp_pdf = PdfFileReader(in_stream)
                            output = PdfFileWriter()
                            try:
                                temp_pdf.decrypt('')
                            except Exception as error:
                                print(error)
                            for s_page in save_page[col]:
                                output.addPage(temp_pdf.getPage(s_page))
                            new_file_path = f'{dir_path}\\{get_file_name()}'
                            with open(new_file_path, "wb") as outputStream:
                                output.write(outputStream)
                            files_to_delete.append(new_file_path)
                            new_files.append(new_file_path)
                    else:
                        show_message(f"Error converting to pdf\n{src}")
                        break
                col += 1

            merge_pdfs(new_files, fp)
            for del_file in files_to_delete:
                os.remove(del_file)
            show_message("File saved successfully!", True)
        else:
            show_message(f"No page selected. Please select at least 1 page to create new pdf.")
    except Exception as error:
        logger.error(f"{error} \n{traceback.format_exc()}")
        show_message(f"{error} \n{traceback.format_exc()}")


def main():
    global page_selected
    while True:
        event, values = window.read(timeout=100)
        if event in ('-exit-', None):
            break
        elif 'PF-FILENAME-' in event:
            col = int(event.split("-")[-1])
            spin_me(col)
            on_file_load(values[event], col)
        elif "CHECK-IMAGE-PF-PAGE-" in event:
            col = event.split("-")[-1]
            img_key = event.replace("CHECK-", "")
            act_img(img_key, values[event])
            update_save_btn()
        elif "IMAGE-PF-PAGE-" in event and "-IMAGE-PF-PAGE" not in event:
            col = event.split("-")[-1]
            img_key = event
            chk_key = f"CHECK-{event}"
            act_img(img_key, not values[chk_key])
            update_save_btn()
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
            clear_col_img(col, True)
        else:
            logger.warning(f"Event: {event} not implemented yet.")
    window.close()


if __name__ == '__main__':
    main()
