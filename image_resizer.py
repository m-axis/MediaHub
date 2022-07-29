import os
from PIL import UnidentifiedImageError

from common import *

image_resizer = [
    [sg.Input(sorted(sg.user_settings_get_entry('-filenames-', [])),
              size=(50, 1),
              key='IR-FILENAME', enable_events=True), sg.FileBrowse(key='IR-BROWSE', enable_events=True)],
    [sg.Text('Width (px) *:'), sg.Input(default_text='', size=(4, 1), key='IR-W', enable_events=True),
     sg.Text('Height (px):'), sg.Input(default_text='', size=(4, 1), key='IR-H')],
    [sg.Button(image_data=RESIZE_BTN, key='IR-RESIZE',
               button_color=(sg.theme_background_color(), sg.theme_background_color()))],
    [sg.Column([[sg.Text()]], key='IR-IMG-COL')]

]


async def resize_image(image_path, width, height):
    msg = {"status": False, "msg": ''}
    try:
        cwd = os.getcwd()
        current_filename = image_path.split("/")[-1]
        file_path = f'{cwd}\\resized'
        if not image_path:
            raise Exception(f"Please choose an image to begin with.")
        elif not width or int(width) == 0:
            raise Exception(f"Image width can not be zero.")
        else:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            img = Image.open(image_path)
            try:
                img.convert('RGB')
            except Exception as er:
                logging.warning(f"image_resizer - resize_image {er}")
                rgb = Image.new('RGB', img.size, (255, 255, 255))  # white background
                rgb.paste(img, mask=img.split()[3])
                img = rgb
            now_width = img.size[0]
            now_height = img.size[1]
            wpercent = (int(width) / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            height_ = int(height) if height else hsize
            if now_width < int(width) or now_height < height_:
                raise Exception(
                    f"Resized image ({width}x{height_}) can not be bigger than source image ({now_width}x{now_height}).")
            else:
                img = img.resize((int(width), height_), Image.ANTIALIAS)
                img.save(f"{file_path}\\{current_filename}")
                msg["status"] = True
                msg["msg"] = f"Image resized to {width},{height_}. "
                logging.info(msg["msg"])
    except UnidentifiedImageError:
        msg["status"] = False
        msg["msg"] = f"Not an image: {image_path}"
        logging.warning(msg["msg"])
    except TypeError as typeError:
        msg["status"] = False
        msg["msg"] = "Image is too short."
        logging.warning(msg["msg"])
    except Exception as error:
        msg["status"] = False
        msg["msg"] = error
        logging.error(msg["msg"])
    return msg
