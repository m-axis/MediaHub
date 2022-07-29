from PyPDF2 import PdfFileMerger, utils
from datetime import datetime
from common import *

column_layout = [[sg.Input(sorted(sg.user_settings_get_entry('-filenames-', [])),
                           size=(50, 1),
                           key='PF-FILENAME0'), sg.FileBrowse(),
                  # sg.Button(enable_events=True, image_data=PLUS_ICO, key="PF-PLUS")
                  sg.Button(image_data=PLUS_ICO, key='PF-PLUS',
                            button_color=(sg.theme_background_color(), sg.theme_background_color()))
                  ],
                 [sg.Input(sorted(sg.user_settings_get_entry('-filenames-', [])),
                           size=(50, 1),
                           key='PF-FILENAME1'), sg.FileBrowse()]

                 ]

pdf_merger = [
    [sg.Column(column_layout, key='PF-COLUMN')],
    [sg.Button(image_data=MERGE_BTN, key='PF-MERGE',
               button_color=(sg.theme_background_color(), sg.theme_background_color()))],
]

files_to_delete = []


def get_file_name(ff="pdf"):
    now = datetime.now()
    return now.strftime(f"%Y%m%d%H%M%S%f.{ff}")


async def new_file_browser(i):
    return [[sg.Input(sorted(sg.user_settings_get_entry('-filenames-', [])),
                      size=(50, 1),
                      key=f'PF-FILENAME{i}'), sg.FileBrowse()]]


async def convert_to_pdf(file_path):
    msg = {"status": False, "msg": ''}
    global files_to_delete
    try:
        file_format = file_path.split(".")[-1]
        dir_path = f'{cwd}\\temp'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if file_format.upper() != "PDF" and file_format.lower() in IMAGES:
            img = Image.open(file_path)
            new_file_path = f'{dir_path}\\{get_file_name()}'
            try:
                img.convert('RGB')
                img.save(new_file_path)
            except Exception as error:
                rgb = Image.new('RGB', img.size, (255, 255, 255))  # white background
                rgb.paste(img, mask=img.split()[3])
                rgb.save(new_file_path, 'PDF', resoultion=100.0)
                logging.warning(f"pdf_merger - convert_to_pdf: {error}")
            files_to_delete.append(new_file_path)
            msg["status"] = True
            msg["msg"] = new_file_path
        elif file_format.upper() == "PDF":
            msg["status"] = True
            msg["msg"] = file_path
    except Exception as error:
        msg["status"] = False
        msg["msg"] = error
        logging.error(f"pdf_merger - convert_to_pdf: {error}\n{traceback.format_exc()}")
    return msg


async def merge_pdf(files, result_file_name="result.pdf"):
    msg = {"status": False, "msg": ''}
    global files_to_delete
    file_with_error = ""
    try:
        if len(files) >= 2:
            merger = PdfFileMerger()
            for pdf in files:
                file_with_error = pdf
                temp = await convert_to_pdf(pdf)
                if not temp['status']:
                    raise Exception(temp['msg'])
                merger.append(temp['msg'])
            file_path = f'{cwd}\\mergedPDFs'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            merger.write(f"{file_path}\\{result_file_name}")
            merger.close()
            msg["status"] = True
            msg["msg"] = f"{len(files)} files merged to a pdf successfully and saved in 'mergedPDFs' folder"
        else:
            raise Exception(
                f"Choose at least two files to merge.")
    except FileNotFoundError as fnf:
        msg["status"] = False
        msg["msg"] = fnf
        logging.warning(f"pdf_merger - merge_pdf: {fnf}\n{traceback.format_exc()}")
    except utils.PdfReadError as re:
        msg["status"] = False
        msg["msg"] = f"File can not be decrypted: \n{file_with_error}"
        logging.warning(f"pdf_merger - merge_pdf: {re}\n{traceback.format_exc()}")
    except Exception as error:
        msg["status"] = False
        msg["msg"] = f"{error} with file: \n{file_with_error}"
        logging.error(f"pdf_merger - merge_pdf: {error}\n{traceback.format_exc()}")
    try:
        if len(files_to_delete) >= 1:
            for file in files_to_delete:
                os.remove(file)
        files_to_delete = []
    except Exception as error:
        logging.error(f"Error deleting file: {error}")
    return msg
