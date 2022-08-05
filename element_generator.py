import PySimpleGUI as sg
from common import *

file_browse_count = 0

BLANK_PDF = b'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'

VIEW_COL_SIZE = (320, 600)
P_VIEW_SIZE = (600, 600)
BROWSE_BTN_SIZE = (38, 2)
MAIN_WINDOW_SIZE = (800, 600)




def file_browser(key, **kwargs):
    global file_browse_count
    file_browse_count += 1
    return [[sg.Input('', key=key, readonly=True, visible=False, **kwargs)],
            [sg.FileBrowse(f'Open File {file_browse_count}', key=f"BROWSE-{key}", target=key, size=BROWSE_BTN_SIZE,
                           )]]


def add_image(key, **kwargs):
    return [[sg.Frame('Selected', [[sg.Checkbox('', default=True, key=f"CHECK-{key}", enable_events=True),
                                    sg.Text(" " * 10),
                                    sg.Text(f"Page {int(key.split('-')[-1]) + 1}", key=f"NUM-{key}"),
                                    sg.Button(sg.SYMBOL_UP_ARROWHEAD, key=f"UP-{key}", button_color=BUTTON_COLOR),
                                    sg.Button(sg.SYMBOL_DOWN_ARROWHEAD, key=f"DOWN-{key}", button_color=BUTTON_COLOR),
                                    ], [sg.Image(key=key, **kwargs)]],
                      key=f"FRAME-{key}", background_color=FRAME_COLOR)]]


def a_img_p(key, **kwargs):
    return [sg.Image(key=key, **kwargs)]


view_col_0 = [
    sg.Column([
        [sg.Image(source=BLANK_PDF, key="PF-IMAGE-PLACEHOLDER-0")]
    ], key="PF-VIEW-COLUMN-0", size=VIEW_COL_SIZE,
        scrollable=True, vertical_scroll_only=True, background_color=FRAME_COLOR, sbar_background_color=COLUMN_COLOR),
]

browse_file_0 = [sg.Input('', key="PF-FILENAME-0", readonly=True, visible=False, enable_events=True),
                 sg.FileBrowse(f'Load File 1', key="BROWSE-PF-FILENAME-0", target="PF-FILENAME-0",
                               size=BROWSE_BTN_SIZE, button_color=BUTTON_COLOR),
                 sg.Button('Clear', key="PF-CLEAR-COL-0", disabled=True, button_color=BUTTON_COLOR),
                 ]
browse_file_1 = [sg.Input('', key="PF-FILENAME-1", readonly=True, visible=False, enable_events=True),
                 sg.FileBrowse(f'Load File 2', key="BROWSE-PF-FILENAME-1", target="PF-FILENAME-1",
                               size=BROWSE_BTN_SIZE, disabled=True, button_color=BUTTON_COLOR),
                 sg.Button('Clear', key="PF-CLEAR-COL-1", disabled=True, button_color=BUTTON_COLOR)]

view_col_1 = [
    sg.Column([
        [sg.Image(source=BLANK_PDF, key="PF-IMAGE-PLACEHOLDER-1")
         ]
    ], key="PF-VIEW-COLUMN-1", size=VIEW_COL_SIZE,
        scrollable=True, vertical_scroll_only=True, background_color=FRAME_COLOR, sbar_background_color=COLUMN_COLOR),
]

action_layout = [
    [sg.Frame('',
              [[sg.InputText(visible=False, enable_events=True, key='PF-FILE-SAVE'),
                sg.FileSaveAs("Save PDF", key="PF-SAVE", disabled=True, file_types=(("PDF", "*.pdf"),),
                              button_color=BUTTON_COLOR),
                sg.Button("Preview", key="PF-PREVIEW", disabled=True, button_color=BUTTON_COLOR),
                ],
               ]
              , key="FRAME-PF-ACTION", vertical_alignment='c', size=(VIEW_COL_SIZE[0] * 2 + 66, 40),
              background_color=FRAME_COLOR)]
]

layout = [
    action_layout,
    [
        [sg.Frame('File 1', [browse_file_0, [sg.Text('', key='PF-PAGE-LOAD-0')], view_col_0],
                  background_color=FRAME_COLOR),
         sg.Frame('File 2', [browse_file_1, [sg.Text('', key='PF-PAGE-LOAD-1')], view_col_1],
                  background_color=FRAME_COLOR)],

    ],

]
