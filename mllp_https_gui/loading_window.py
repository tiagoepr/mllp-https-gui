### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Dec 2022
import subprocess
import threading
import os
from time import sleep

import PySimpleGUI as sg


class LoadingWindow:
    def __init__(self):
        sg.theme('SystemDefault1')
        # Layout

        layout_header = [
            [sg.Image(os.path.abspath('../lib/site-packages/mllp_https_gui/doc/logo.png'))],
            [sg.Text('Tiago Rodrigues (Tiago.Rodrigues@sectra.com)', justification='c')],
        ]

        layout_body = [
            [sg.Text('Loading...')],
        ]

        layout_footer = []

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
            icon=os.path.abspath('../lib/site-packages/mllp_https_gui/doc/icon.ico'),
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
            subprocess.call('py -m pip install --upgrade pip --retries 1')

            # Install mllp-https
            subprocess.call('py -m pip install mllp-https --upgrade --retries 1')
        except subprocess.CalledProcessError as e:
            print('Could not upgrade pip and mllp-https modules.')
            print('Error: ', e)

        sleep(1)
        self.window.close()
