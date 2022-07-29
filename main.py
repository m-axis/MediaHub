import asyncio
from youtube_downloader import *
from image_convertor import *
from image_resizer import *
from pdf_merger import *
from menu import *


async def main():
    layout = [frame_layout, [sg.TabGroup([[sg.Tab('Youtube Downloader', yt_download_layout),
                                           sg.Tab('Image Converter', image_converter),
                                           sg.Tab('Resize Image', image_resizer),
                                           sg.Tab('Merge PDFs', pdf_merger)
                                           ]
                                          ], key='-TAB GROUP-', expand_x=True,
                                         expand_y=True),

                             ]]

    window = sg.Window('MediaHub', layout,
                       text_justification='r',
                       default_element_size=(15, 1),
                       font=WIN_FONT, icon=APP_ICON, no_titlebar=True, grab_anywhere=True,
                       finalize=True)

    upload_image_status_ir = 0
    upload_image_status_ic = 0
    pdf_file_count = 2
    while True:
        event, values = window.read()
        if event in ('MN-EXIT', None):
            break  # exit button clicked
        elif event == 'MN-MINIMIZE':
            window.Minimize()
        elif event == 'YT-DOWNLOAD':
            link = values['YT-LINK']
            res = values['YT-RES']
            print(f'Downloading video of {res} resolution...')
            window.refresh()
            return_msg = await download_youtube(link, res, './download')
            await show_message(return_msg['msg'], return_msg['status'])
        elif event == 'IC-CONVERT':
            filepath = values['IC-FILENAME']
            convert_to = values['IC-CONVERT-TO']
            return_msg = await convert_format(filepath, convert_to)
            await show_message(return_msg['msg'], return_msg['status'])
        elif event == 'IR-RESIZE':
            filepath = values['IR-FILENAME']
            width = values['IR-W']
            height = values['IR-H']
            return_msg = await resize_image(filepath, width, height)
            await show_message(return_msg['msg'], return_msg['status'])
        elif event == 'PF-PLUS':
            if pdf_file_count < 10:
                window.extend_layout(window['PF-COLUMN'], await new_file_browser(pdf_file_count))
                pdf_file_count += 1
            else:
                await show_message('Only 10 files can be merged at once.', False)
        elif event == 'PF-MERGE':
            value_keys = values.keys()
            files = []
            for i in range(10):
                if f'PF-FILENAME{i}' in value_keys and values[f'PF-FILENAME{i}']:
                    files.append(values[f'PF-FILENAME{i}'])
            return_msg = await merge_pdf(files)
            await show_message(return_msg['msg'], return_msg['status'])
        elif event == 'IR-FILENAME':
            filepath = values['IR-FILENAME']
            if is_image(filepath):
                img_size = await get_image_size(filepath)
                window['IR-W'].update(value=img_size[0])
                window['IR-H'].update(value=img_size[1])
                img = auto_resize(filepath)
                if upload_image_status_ir == 1:
                    window['IR-IMG-UPLOAD'].update(source=img)
                else:
                    window.extend_layout(window['IR-IMG-COL'], await add_new_image(img, 'IR-IMG-UPLOAD'))
                    upload_image_status_ir = 1
            else:
                await show_message("File is not an image.", False)
        elif event == 'IC-FILENAME':
            filepath = values['IC-FILENAME']
            if is_image(filepath):
                img = auto_resize(filepath)
                if upload_image_status_ic == 1:
                    window['IC-IMG-UPLOAD'].update(source=img)
                else:
                    window.extend_layout(window['IC-IMG-COL'], await add_new_image(img, 'IC-IMG-UPLOAD'))
                    upload_image_status_ic = 1
            else:
                await show_message("File is not an image.", False)
        elif event == 'IR-W':
            width = values['IR-W']
            filepath = values['IR-FILENAME']
            if is_image(filepath):
                window['IR-H'].update(value=get_ratio_h(filepath, width))
            else:
                await show_message("Please load an image file first.", False)
    window.close()


if __name__ == '__main__':
    asyncio.run(main())
