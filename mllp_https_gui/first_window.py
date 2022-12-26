### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Dec 2022
import os

import PySimpleGUI as sg


class FirstWindow:
    def __init__(self):
        sg.theme('SystemDefault1')
        # Layout

        layout_header = [
            [sg.Image(os.path.abspath('../lib/site-packages/mllp_https_gui/doc/logo.png'))],
            [sg.Text('Tiago Rodrigues (Tiago.Rodrigues@sectra.com)\nSECTRA - CO Iberia', justification='c')],
        ]

        layout_body = [
            [sg.Text('Choose Program to configure:')],
            [sg.Button('MLLP 2 HTTPS', size=(15, 5)), sg.Button('HTTPS 2 MLLP', size=(15, 5))],
        ]

        layout_footer = [
            [sg.Image(os.path.abspath('../lib/site-packages/mllp_https_gui/doc/sectra.png'))],
        ]

        layout = [
            [sg.Column(layout_header,
                       k='layout_header',
                       expand_x=True,
                       element_justification='c',
                       size=(500, 250))],
            [sg.Column(layout_body,
                       k='layout_body',
                       element_justification='c')],
            [sg.VSeparator(pad=(0, 20))],
            [sg.Stretch(), sg.Column(layout_footer,
                                     k='layout_footer',
                                     element_justification='right',
                                     vertical_alignment='b',
                                     size=(200, 100))]
        ]

        # Window
        self.firstwindow = sg.Window(
            'Choose Program',
            element_justification='c',
            icon=os.path.abspath('../lib/site-packages/mllp_https_gui/doc/icon.ico'),
        ).layout(layout)



    def open(self):
        # Get values from window
        self.button, self.values = self.firstwindow.Read()

        # print(self.button, self.values)
        if self.button == "MLLP 2 HTTPS":
            print("MLLP2HTTPS choosen")
            from mllp_https_gui.mllp2https_config_window import MLLPHTTPSConfigWindow
            config_window = MLLPHTTPSConfigWindow()
            self.firstwindow.close()
            config_window.open()

        if self.button == "HTTPS 2 MLLP":
            print("HTTPS2MLLP choosen")
            from mllp_https_gui.https2mllp_config_window import HTTPSMLLPConfigWindow
            config_window = HTTPSMLLPConfigWindow()
            self.firstwindow.close()
            config_window.open()
        else:
            pass

        # print(self.button)
