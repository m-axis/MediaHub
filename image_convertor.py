import os
from PIL import UnidentifiedImageError

from common import *

image_format = sg.Combo(values=IMAGES, default_value=IMAGES[0], size=(10, 1),
                        key='IC-CONVERT-TO')

image_converter = [[sg.Input(sorted(sg.user_settings_get_entry('-filenames-', [])),
                             size=(50, 1),
                             key='IC-FILENAME', enable_events=True), sg.FileBrowse()],
                   [sg.Text('Convert To     :'), image_format],
                   [sg.Button(image_data=CONVERT_BTN, key='IC-CONVERT',
                              button_color=(sg.theme_background_color(), sg.theme_background_color()))],
                   [sg.Column([[sg.Text()]], key='IC-IMG-COL')]
                   ]


async def convert_format(image_path, convert_to):
    msg = {"status": False, "msg": ''}
    try:
        cwd = os.getcwd()
        current_filename = image_path.split("/")[-1]
        file_path = f'{cwd}\\converted'
        file_name = current_filename.split(".")[0]
        convert_from = current_filename.split(".")[-1]
        if not image_path:
            raise Exception(f"Please choose an image to begin with.")
        elif convert_from.upper() == convert_to.upper():
            raise Exception(f"Converting image from '.{convert_from}' to '.{convert_to}' not allowed.")
        else:
            img = Image.open(image_path)
            try:
                img.convert('RGB')
            except Exception as er:
                logging.warning(f"image_convertor - convert_format {er}")
                rgb = Image.new('RGB', img.size, (255, 255, 255))  # white background
                rgb.paste(img, mask=img.split()[3])
                img = rgb
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            img.save(f'{file_path}\\{file_name}.{convert_to}')
            msg["status"] = True
            msg["msg"] = f"Image converted to {convert_to} successfully. "
            logging.info(msg["msg"])
    except UnidentifiedImageError:
        msg["status"] = False
        msg["msg"] = f"Not an image: {image_path}"
        logging.warning(msg["msg"])
    except Exception as error:
        msg["status"] = False
        msg["msg"] = error
        logging.error(msg["msg"])
    return msg
