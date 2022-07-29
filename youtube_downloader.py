from pytube import YouTube, exceptions

from common import *

combobox = sg.Combo(values=RESOLUTIONS, default_value='Highest', size=(10, 1),
                    key='YT-RES')
yt_download_layout = [
    [sg.Text('YouTube Link:'), sg.Input(default_text='', size=(60, 1), key='YT-LINK')],
    [sg.Text('Resolution     :'), combobox],
    [sg.Button(image_data=DOWNLOAD_BTN, key='YT-DOWNLOAD',
               button_color=(sg.theme_background_color(), sg.theme_background_color()))]
]


async def download_youtube(link, res, out_path='./'):
    return_val = {"status": False, "msg": ''}
    try:
        yt_video = YouTube(link)
        if res == 'Highest':
            my_video = yt_video.streams.get_highest_resolution()
            my_video.download(out_path)
        else:
            yt_video.streams.filter(file_extension="mp4").get_by_resolution(res).download(out_path)
        return_val["status"] = True
        return_val["msg"] = 'Your video is downloaded successfully'
        logging.warning(return_val["msg"])
    except exceptions.RegexMatchError:
        return_val["status"] = False
        return_val["msg"] = 'Invalid url.'
        logging.warning(return_val["msg"])
    except AttributeError:
        return_val["status"] = False
        return_val["msg"] = f'Resolution {res} does not exists for this video.'
        logging.warning(return_val["msg"])
    except Exception as error:
        return_val["status"] = False
        return_val["msg"] = error
        logging.error(return_val["msg"])
    return return_val
