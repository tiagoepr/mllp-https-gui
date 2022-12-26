### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Dec 2022

import threading
import os
from time import sleep

import PySimpleGUI as sg


class LoadingWindow:
    def __init__(self):
        sg.theme('SystemDefault1')
        # Layout

        layout_header = [
            [sg.Image('../doc/logo.png')],
            [sg.Text('Tiago Rodrigues (Tiago.Rodrigues@sectra.com)\nSECTRA - CO Iberia', justification='c')],
        ]

        layout_body = [
            [sg.Text('Loading...')],
        ]

        layout_footer = [
            [sg.Image('../doc/sectra.png')],
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
        self.window = sg.Window(
            'Choose Program',
            element_justification='c',
            icon='../doc/icon.ico',
        ).layout(layout)

        # Get values from window
        # self.button, self.values = self.window.Read()



    def open(self):
        # Open loading window
        button, values = self.window.Read(timeout=0)

        x = threading.Thread(target=self.background_tasks(), daemon=True)
        x.start()

    def background_tasks(self):
        # Make sure that Pip is installed:
        try:
            # os.system('py -m pip --version')
            os.system('py -m pip install --upgrade pip')

            # Install mllp-https
            os.system('py -m pip install mllp-https')
        except:
            print('Could not update pip and mllp-https modules.')

        sleep(1)
        self.window.close()


