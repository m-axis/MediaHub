import PySimpleGUI as sg

file_browse_count = 0

BLANK_PDF = b'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'


def file_browser(key, **kwargs):
    global file_browse_count
    file_browse_count += 1
    return [[sg.Input('', key=key, readonly=True, visible=False, **kwargs)],
            [sg.FileBrowse(f'Open PDF {file_browse_count}', target=key, size=(40, 2))]]


def image(key, **kwargs):
    return [[sg.Frame('Selected', [[sg.Checkbox('', default=True, key=f"CHECK-{key}", enable_events=True),
                                    sg.Button(" ⥣ ", key=f"UP-{key}"),
                                    sg.Button(" ⥥ ", key=f"DOWN-{key}"),
                                    ], [sg.Image(key=key, **kwargs)]],
                      key=f"FRAME-{key}")]]


browser_columns = [
    [sg.Column([[sg.Input('', key="PF-FILENAME-0", readonly=True, visible=False, enable_events=True)],
                [sg.FileBrowse(f'Open PDF 1', key="BROWSE-PF-FILENAME-0", target="PF-FILENAME-0", size=(40, 2))]]),
     sg.Column([[sg.Input('', key="PF-FILENAME-1", readonly=True, visible=False, enable_events=True)],
                [sg.FileBrowse(f'Open PDF 2', key="BROWSE-PF-FILENAME-1", target="PF-FILENAME-1", size=(40, 2),
                               visible=False)]])
     ]
]

view_layout0 = [
    [sg.Image(source="", key="PF-IMAGE-PLACEHOLDER0")],
]
view_layout1 = [
    [sg.Image(source="", key="PF-IMAGE-PLACEHOLDER1")],
]

action_layout = [
    [sg.Frame('',
              [[sg.Button("Save PDF", key="PF-SAVE"),
                sg.Button("Preview", key="PF-PREVIEW")]
               ]
              , key="FRAME-PF-ACTION", vertical_alignment='c', visible=False)]
]

layout = [
    [sg.Frame('', browser_columns, vertical_alignment='t')],
    action_layout,
    [
        sg.Column(view_layout0, key="PF-VIEW-COLUMN-0", size=(320, 600), scrollable=True, vertical_scroll_only=True,
                  visible=False),
        sg.Column(view_layout1, key="PF-VIEW-COLUMN-1", size=(320, 600), scrollable=True, vertical_scroll_only=True,
                  visible=False)

    ],

]
